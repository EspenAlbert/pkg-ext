<!-- === DO_NOT_EDIT: pkg-ext header === -->
# workflows

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`chore`](#chore_def)
- [`post_merge`](#post_merge_def)
- [`pre_change`](#pre_change_def)
- [`pre_commit`](#pre_commit_def)
- [`promote`](#promote_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->
<!-- === DO_NOT_EDIT: pkg-ext chore_def === -->
<a id="chore_def"></a>

### function: `chore`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L357)
> **Since:** unreleased

```python
def chore(ctx: Context, description: str = <typer.models.OptionInfo object at 0x105cf91d0>, pr_number: int = <typer.models.OptionInfo object at 0x105cf9450>):
    ...
```

Create a ChoreAction for internal changes that warrant a release.
<!-- === OK_EDIT: pkg-ext chore_def === -->
<!-- === DO_NOT_EDIT: pkg-ext post_merge_def === -->
<a id="post_merge_def"></a>

### function: `post_merge`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L195)
> **Since:** unreleased

```python
def post_merge(ctx: Context, explicit_pr: int = <typer.models.OptionInfo object at 0x105bf51d0>, push: bool = <typer.models.OptionInfo object at 0x105bf5090>, skip_clean_old_entries: bool = <typer.models.OptionInfo object at 0x105bf5a90>, force_reason: str = <typer.models.OptionInfo object at 0x105cf8f50>):
    ...
```
<!-- === OK_EDIT: pkg-ext post_merge_def === -->
<!-- === DO_NOT_EDIT: pkg-ext pre_change_def === -->
<a id="pre_change_def"></a>

### function: `pre_change`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L259)
> **Since:** unreleased

```python
def pre_change(ctx: Context, group: str | None = <typer.models.OptionInfo object at 0x105bf5310>, git_changes_since: GitSince = <typer.models.OptionInfo object at 0x105bf4b90>, skip_fix_commits: bool = <typer.models.OptionInfo object at 0x105bf5e50>, full: bool = <typer.models.OptionInfo object at 0x105bf5f90>, skip_docs: bool = <typer.models.OptionInfo object at 0x105bf5950>, skip_open_in_editor: bool | None = <typer.models.OptionInfo object at 0x105bf60d0>, keep_private: bool = <typer.models.OptionInfo object at 0x105bf6210>):
    ...
```

Handle new symbols then generate examples and tests.
<!-- === OK_EDIT: pkg-ext pre_change_def === -->
<!-- === DO_NOT_EDIT: pkg-ext pre_commit_def === -->
<a id="pre_commit_def"></a>

### function: `pre_commit`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L307)
> **Since:** unreleased

```python
def pre_commit(ctx: Context, git_changes_since: GitSince = <typer.models.OptionInfo object at 0x105bf4b90>, skip_docs: bool = <typer.models.OptionInfo object at 0x105bf5950>, skip_dirty_check: bool = <typer.models.OptionInfo object at 0x105bf5bd0>):
    ...
```

Update changelog and regenerate docs (bot mode, writes to -dev files).
<!-- === OK_EDIT: pkg-ext pre_commit_def === -->
<!-- === DO_NOT_EDIT: pkg-ext promote_def === -->
<a id="promote_def"></a>

### function: `promote`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L385)
> **Since:** unreleased

```python
def promote(ctx: Context, name: str | None = <typer.models.OptionInfo object at 0x105cf9590>, group: str | None = <typer.models.OptionInfo object at 0x105cf96d0>, module_filter: str | None = <typer.models.OptionInfo object at 0x105cf9810>, pattern: str | None = <typer.models.OptionInfo object at 0x105cf9950>, undecided: bool = <typer.models.OptionInfo object at 0x105cf9a90>, pr_number: int = <typer.models.OptionInfo object at 0x105cf9bd0>):
    ...
```

Promote symbols to public API (private or undecided).
<!-- === OK_EDIT: pkg-ext promote_def === -->