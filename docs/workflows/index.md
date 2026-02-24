<!-- === DO_NOT_EDIT: pkg-ext header === -->
# workflows

<!-- === OK_EDIT: pkg-ext header === -->
<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`change_base`](#change_base_def)
- [`post_merge`](#post_merge_def)
- [`pre_change`](#pre_change_def)
- [`pre_commit`](#pre_commit_def)
<!-- === OK_EDIT: pkg-ext symbols === -->
<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->
<!-- === DO_NOT_EDIT: pkg-ext post_merge_def === -->
<a id="post_merge_def"></a>

### cli_command: `post_merge`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L127)
> **Since:** 0.1.0

```python
def post_merge(*, explicit_pr: int = 0, push: bool = False, skip_clean_old_entries: bool = False, force_reason: str = ''):
    ...
```

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--pr` | `int` | `0` | Use this if the HEAD commit is not a merge |
| `--push` | `bool` | `False` | Push commit and tag |
| `--skip-clean` | `bool` | `False` | Skip cleaning old entries |
| `--force-reason` | `str` | `''` | Force release with this reason (creates ChoreAction if no changelog entries) |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext post_merge_def === -->
<!-- === DO_NOT_EDIT: pkg-ext pre_change_def === -->
<a id="pre_change_def"></a>

### cli_command: `pre_change`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L203)
> **Since:** 0.1.0

```python
def pre_change(*, group: str | None = ..., git_changes_since: GitSince = <GitSince.DEFAULT: 'default'>, skip_fix_commits: bool = False, full: bool = False, skip_docs: bool = False, skip_open_in_editor: bool | None = ..., keep_private: bool = False):
    ...
```

Handle new symbols, update changelog, optionally sync files and docs.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `-g`, `--group` | `str | None` | *required* | Generate for specific group only |
| `--git-since` | `GitSince` | `<GitSince.DEFAULT: 'default'>` | Will use git log to look for 'fix' commits to include in the changelog [no_git_changes, last_git_tag, pr_base_branch, default] |
| `--skip-fix-commits` | `bool` | `False` | Skip prompts for fix commits in git history |
| `--full` | `bool` | `False` | Run pre-commit workflow after pre-change (sync + docs + diff) |
| `--skip-docs` | `bool` | `False` | Skip doc regeneration |
| `--skip-open` | `bool | None` | *required* | Skip opening files in editor |
| `--keep-private` | `bool` | `False` | Automatically keep all new symbols private without prompting |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext pre_change_def === -->
<!-- === DO_NOT_EDIT: pkg-ext pre_commit_def === -->
<a id="pre_commit_def"></a>

### cli_command: `pre_commit`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L237)
> **Since:** 0.1.0

```python
def pre_commit(*, git_changes_since: GitSince = <GitSince.DEFAULT: 'default'>, skip_docs: bool = False, skip_dirty_check: bool = False):
    ...
```

Update changelog and regenerate docs (bot mode, writes to -dev files).

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--git-since` | `GitSince` | `<GitSince.DEFAULT: 'default'>` | Will use git log to look for 'fix' commits to include in the changelog [no_git_changes, last_git_tag, pr_base_branch, default] |
| `--skip-docs` | `bool` | `False` | Skip doc regeneration |
| `--skip-dirty-check` | `bool` | `False` | Skip dirty file check (for tests) |

### Changes

| Version | Change |
|---------|--------|
| 0.1.0 | Made public |
<!-- === OK_EDIT: pkg-ext pre_commit_def === -->
<!-- === DO_NOT_EDIT: pkg-ext change_base_def === -->
<a id="change_base_def"></a>

### cli_command: `change_base`
- [source](../../pkg_ext/_internal/cli/workflow_cmds.py#L283)
> **Since:** unreleased

```python
def change_base(*, new_base: str = ..., pr_number: int = 0):
    ...
```

Consolidate changelog files from closed PRs after re-targeting a stacked PR.

**CLI Options:**

| Flag | Type | Default | Description |
|---|---|---|---|
| `--new-base` | `str` | *required* | The new base branch (e.g., 'main') |
| `--pr` | `int` | `0` | Use this if the HEAD commit is not a merge |

### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext change_base_def === -->