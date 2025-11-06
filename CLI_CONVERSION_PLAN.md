# Todu CLI Conversion Plan

## Current State Analysis

### Script Inventory

**Core Scripts** (14 files):

- `delete-project.py` - Delete registered project
- `git_context.py` - Git repository context detection
- `id_registry.py` - Unified ID management
- `list-items.py` - Search/list tasks across all systems
- `list-projects.py` - List registered projects
- `plugin_registry.py` - Plugin system management
- `recurring.py` - Recurring task logic
- `register-project.py` - Register new project
- `report.py` - Generate daily task report
- `resolve_task.py` - Resolve task by ID or reference
- `resolve-project.py` - Resolve project by nickname
- `sync_manager.py` - Orchestrate syncing across systems
- `update-project.py` - Update project settings
- `weekly-review.py` - Generate weekly report

**System-Specific Scripts** (18 files):

- **GitHub**: create-comment, create-issue, sync-issues, update-issue,
  view-issue, label_utils
- **Forgejo**: create-comment, create-issue, sync-issues, update-issue,
  view-issue, label_utils
- **Todoist**: create-comment, create-task, list-projects, sync-tasks,
  update-task, view-task

### Current Dependencies

- `PyGithub>=2.1.1` (GitHub integration)
- `todoist-api-python>=2.1.0` (Todoist integration)
- `requests>=2.31.0` (Forgejo HTTP API)
- Standard library (argparse, json, pathlib, datetime, etc.)

### Current Execution Model

- Standalone scripts with `#!/usr/bin/env -S uv run` shebang
- PEP 723 inline dependency metadata
- Each script run independently via full path
- Skills system wraps scripts with additional logic

## Proposed CLI Structure

### Command Hierarchy

```text
todu
├── project
│   ├── list                    # List registered projects
│   ├── register <type> <url>   # Register new project
│   ├── update <nickname>       # Update project settings
│   └── delete <nickname>       # Delete project
│
├── task
│   ├── search [filters]        # Search tasks (default: open)
│   ├── create <project> <title> # Create task/issue
│   ├── update <id> [changes]   # Update task/issue
│   ├── view <id>               # View task details
│   ├── comment <id> <text>     # Add comment
│   ├── resolve <ref>           # Resolve task reference to ID
│   └── sync [project]          # Sync tasks (default: all)
│
└── report
    ├── daily [date]            # Daily task report
    └── weekly [date]           # Weekly task report
```

### Example Usage

```bash
# Project management
todu project list
todu project register github https://github.com/user/repo
todu project register forgejo https://forgejo.caradoc.com/user/repo vault
todu project update vault --nickname my-vault
todu project delete old-project

# Task operations
todu task search                           # All open tasks
todu task search --status open --project vault
todu task search --labels bug,priority:high
todu task create vault "Fix authentication bug"
todu task update 42 --status done
todu task update 42 --add-label priority:high
todu task view 42
todu task comment 42 "Fixed in PR #123"
todu task sync                             # Sync all
todu task sync vault                       # Sync one project

# Reports
todu report daily
todu report daily 2025-11-01
todu report weekly
```

## Implementation Plan

### Phase 1: Project Setup (Day 1)

**Goal**: Create package structure and CLI framework

1. **Create package structure**

   ```text
   todu/
   ├── pyproject.toml
   ├── README.md
   ├── src/
   │   └── todu/
   │       ├── __init__.py
   │       ├── cli.py              # Main CLI entry point
   │       ├── commands/
   │       │   ├── __init__.py
   │       │   ├── project.py      # Project commands
   │       │   ├── task.py         # Task commands
   │       │   └── report.py       # Report commands
   │       └── lib/
   │           ├── __init__.py
   │           ├── github.py       # GitHub client
   │           ├── forgejo.py      # Forgejo client
   │           ├── todoist.py      # Todoist client
   │           ├── registry.py     # ID registry
   │           ├── projects.py     # Project registry
   │           ├── sync.py         # Sync manager
   │           └── reports.py      # Report generation
   ```

2. **Create `pyproject.toml`**

   ```toml
   [project]
   name = "todu"
   version = "0.1.0"
   description = "Unified task management across GitHub, Forgejo, and Todoist"
   requires-python = ">=3.9"
   dependencies = [
       "click>=8.0.0",
       "rich>=13.0.0",
       "PyGithub>=2.1.1",
       "todoist-api-python>=2.1.0",
       "requests>=2.31.0",
   ]

   [project.scripts]
   todu = "todu.cli:cli"

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   ```

3. **Create basic CLI structure with Click**

   Main entry point (`src/todu/cli.py`):

   ```python
   import click
   from todu.commands.project import project
   from todu.commands.task import task
   from todu.commands.report import report

   @click.group()
   @click.version_option(version='0.1.0')
   def cli():
       """Todu - Unified task management across GitHub, Forgejo, and Todoist"""
       pass

   cli.add_command(project)
   cli.add_command(task)
   cli.add_command(report)

   if __name__ == '__main__':
       cli()
   ```

   Command modules:
   - `src/todu/commands/project.py` - Stub project commands
   - `src/todu/commands/task.py` - Stub task commands
   - `src/todu/commands/report.py` - Stub report commands

4. **Install in development mode**

   ```bash
   cd /Users/erik/Private/code/todu
   uv pip install -e .
   # Now `todu` command is available
   ```

**Success Criteria**:

- `todu --help` shows command structure
- `todu project --help` works
- `todu task --help` works
- `todu report --help` works

### Phase 2: Extract Core Library (Days 2-3)

**Goal**: Refactor scripts into reusable library functions

1. **Extract project registry logic**
   - Move from `register-project.py`, `list-projects.py`, etc.
   - Create `src/todu/lib/projects.py`
   - Functions: `register_project()`, `list_projects()`, `update_project()`, `delete_project()`

2. **Extract ID registry logic**
   - Move from `id_registry.py`
   - Create `src/todu/lib/registry.py`
   - Functions: `allocate_id()`, `resolve_id()`, `get_next_id()`

3. **Extract API clients**
   - Move GitHub logic to `src/todu/lib/github.py`
   - Move Forgejo logic to `src/todu/lib/forgejo.py`
   - Move Todoist logic to `src/todu/lib/todoist.py`
   - Each client provides: `sync()`, `create()`, `update()`, `view()`, `add_comment()`

4. **Extract sync manager**
   - Move from `sync_manager.py`
   - Create `src/todu/lib/sync.py`
   - Function: `sync_projects(project_names: list[str] = None)`

5. **Extract report generator**
   - Move from `report.py`, `weekly-review.py`
   - Create `src/todu/lib/reports.py`
   - Functions: `generate_daily_report()`, `generate_weekly_report()`

6. **Extract utilities**
   - Git context detection (`git_context.py`)
   - Recurring task logic (`recurring.py`)
   - Task/project resolution (`resolve_task.py`, `resolve-project.py`)

**Success Criteria**:

- All library modules import cleanly
- Unit tests pass for extracted functions
- No circular dependencies

### Phase 3: Implement Commands (Days 4-5)

**Goal**: Wire up CLI commands to library functions

1. **Implement `todu project` commands**

   ```python
   # src/todu/commands/project.py
   import click
   from todu.lib import projects

   @click.group()
   def project():
       """Manage registered projects"""
       pass

   @project.command()
   def list():
       """List all registered projects"""
       projs = projects.list_projects()
       # Format and display with rich

   @project.command()
   @click.argument('system')
   @click.argument('url')
   @click.argument('nickname', required=False)
   def register(system, url, nickname):
       """Register a new project"""
       projects.register_project(system, url, nickname)

   # ... etc
   ```

2. **Implement `todu task` commands**

   ```python
   # src/todu/commands/task.py
   import click
   from todu.lib import sync, registry

   @click.group()
   def task():
       """Manage tasks and issues"""
       pass

   @task.command()
   @click.option('--status', default='open', help='Filter by status')
   @click.option('--project', help='Filter by project nickname')
   @click.option('--labels', help='Filter by labels (comma-separated)')
   def search(status, project, labels):
       """Search tasks across projects"""
       # Call list-items logic

   @task.command()
   @click.argument('project')
   @click.argument('title')
   def create(project, title):
       """Create a new task/issue"""
       # Resolve project, call appropriate client

   # ... etc
   ```

3. **Implement `todu report` commands**

   ```python
   # src/todu/commands/report.py
   import click
   from todu.lib import reports

   @click.group()
   def report():
       """Generate task reports"""
       pass

   @report.command()
   @click.argument('date', required=False)
   def daily(date):
       """Generate daily task report"""
       report_text = reports.generate_daily_report(date)
       click.echo(report_text)

   @report.command()
   @click.argument('date', required=False)
   def weekly(date):
       """Generate weekly task report"""
       report_text = reports.generate_weekly_report(date)
       click.echo(report_text)
   ```

**Success Criteria**:

- All commands execute without errors
- Commands produce same output as old scripts
- Rich formatting for better readability

### Phase 4: Migration & Testing (Day 6)

**Goal**: Ensure CLI works as well as old scripts

1. **Create integration tests**
   - Test full workflows (register → sync → search → update)
   - Test each system (GitHub, Forgejo, Todoist)
   - Test error handling

2. **Update skills to use new CLI**
   - Change from `/path/to/script.py [args]`
   - To `todu <command> [args]`
   - Much simpler and clearer

3. **Add migration guide**
   - Document old script → new command mapping
   - Provide examples for common operations

4. **Keep old scripts temporarily**
   - Mark as deprecated
   - Add warning message pointing to new CLI
   - Remove after 1-2 weeks of successful CLI usage

**Success Criteria**:

- Integration tests pass
- Skills work with new CLI
- All features from old scripts available
- Performance similar or better

### Phase 5: Enhancements (Day 7+)

**Goal**: Add CLI-specific improvements

1. **Better output formatting**
   - Rich tables for project/task listings
   - Color-coded status/priority
   - Progress bars for sync operations

2. **Interactive prompts**
   - `todu task create` with prompts for fields
   - Confirmation for destructive operations

3. **Shell completion**
   - Generate bash/zsh completions
   - Tab-complete project names, task IDs

4. **Configuration file**
   - `~/.config/todu/config.toml`
   - Default filters, output preferences
   - API tokens (encrypted)

5. **Batch operations**
   - `todu task update 42,43,44 --status done`
   - `todu task sync --all --parallel`

## Technical Decisions

### Why Click (over Typer)?

- Most widely used Python CLI framework (~424M downloads/month vs Typer's 84M)
- Mature and battle-tested (powers Flask, AWS CLI, and hundreds of others)
- **Direct and explicit** - no magic abstractions
- **One less dependency** - Typer is built on Click, so why add the wrapper?
- Excellent documentation and Stack Overflow support
- Composable command groups for clean structure
- Easy to debug - straightforward decorator pattern
- When something breaks, you only need to understand Click, not Click + Typer

### Why Rich?

- Beautiful terminal output
- Tables, progress bars, syntax highlighting
- Markdown rendering
- Better user experience
- Works seamlessly with Click

### Package Structure

- `src/` layout for modern Python packaging
- Separate `lib/` and `commands/` for clarity
- Minimal dependencies (just 5 packages)
- Click for CLI, no extra wrappers needed

### Backward Compatibility

- Keep cache structure (`~/.local/todu/`)
- Keep project registry format
- Keep ID allocation system
- Scripts can coexist during migration

## Migration Timeline

| Day | Phase | Deliverable |
|-----|-------|-------------|
| 1 | Setup | Package structure, CLI skeleton |
| 2-3 | Library | Extracted reusable functions |
| 4-5 | Commands | All CLI commands implemented |
| 6 | Testing | Tests pass, skills updated |
| 7+ | Polish | Rich output, completion, config |

## Risks & Mitigations

**Risk**: Breaking existing workflows
**Mitigation**: Keep old scripts working during migration

**Risk**: API token handling in new package
**Mitigation**: Reuse existing token storage, test thoroughly

**Risk**: Performance regression
**Mitigation**: Benchmark before/after, optimize if needed

**Risk**: Incomplete feature coverage
**Mitigation**: Create checklist mapping old scripts to new commands

## Success Metrics

- All 32 scripts replaced with ~15 CLI commands
- Installation via single `uv pip install -e .`
- Skills simplified to `todu <command>` invocations
- Help text automatically generated
- No loss of functionality
- Better error messages and user feedback

## Next Steps

1. Review and approve this plan
2. Begin Phase 1: Project setup
3. Create feature branch: `feature/cli-conversion`
4. Implement incrementally with commits per phase
5. Test thoroughly before replacing old scripts
