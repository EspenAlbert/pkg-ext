import logging

from ask_shell._internal.rich_progress import new_task

from pkg_ext._internal.changelog import DeleteAction, RenameAction
from pkg_ext._internal.context import pkg_ctx
from pkg_ext._internal.interactive import (
    confirm_create_alias,
    confirm_delete,
    select_multiple_ref_state,
    select_ref,
)
from pkg_ext._internal.models import RefState, RefStateWithSymbol

logger = logging.getLogger(__name__)


def process_reference_renames(
    active_refs: dict[str, RefStateWithSymbol],
    renames: list[tuple[str, RefState]],
    task: new_task,
    ctx: pkg_ctx,
) -> set[str]:
    """Process renames. Returns set of old names that were renamed."""
    renamed_names: set[str] = set()
    used_local_ids: set[str] = set()
    for group, ref in renames:
        rename_choices = [state for lid, state in active_refs.items() if lid not in used_local_ids]
        new_ref = select_ref(
            f"Select new name for the reference {ref.name} with type: {ref.type}",
            rename_choices,
        )
        used_local_ids.add(new_ref.symbol.local_id)
        if confirm_create_alias(ref, new_ref):
            raise NotImplementedError("Alias creation is not implemented yet")
        ctx.add_changelog_action(RenameAction(name=new_ref.name, group=group, old_name=ref.name))
        renamed_names.add(ref.name)
        task.update(advance=1)
    return renamed_names


def handle_removed_refs(ctx: pkg_ctx) -> None:
    tool_state = ctx.tool_state
    code_state = ctx.code_state
    removed_refs = tool_state.removed_refs(code_state)
    if not removed_refs:
        logger.info("No removed references found in the package")
        return
    # Extract just RefState for UI selection
    states_only = [state for _, state in removed_refs]
    if renames := select_multiple_ref_state("Select references that have been renamed (if any):", states_only):
        # Find the (group, state) pairs for the selected renames
        rename_pairs = [(g, s) for g, s in removed_refs if s in renames]
        with new_task("Renaming references", total=len(rename_pairs), log_updates=True) as task:
            renamed_names = process_reference_renames(code_state.named_refs, rename_pairs, task, ctx)
            removed_refs = [(g, s) for g, s in removed_refs if s.name not in renamed_names]
    delete_names = ", ".join(ref.name for _, ref in removed_refs)
    states_only = [state for _, state in removed_refs]
    if confirm_delete(states_only):
        for group, ref in removed_refs:
            ctx.add_changelog_action(DeleteAction(name=ref.name, group=group))
    else:
        assert False, f"Old references {delete_names} were not confirmed for deletion"
