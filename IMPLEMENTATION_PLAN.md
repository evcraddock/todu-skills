# Implementation Plan: Convert Skills to Use `todu` CLI

## Overview

This plan outlines the migration of all core skills from calling Python scripts directly to using the unified `todu` CLI application. Each skill will be updated to invoke appropriate `todu` commands instead of executing scripts via the plugin registry.

## Goals

1. Replace all Python script calls with `todu` CLI commands
2. Maintain existing skill interfaces and natural language parsing
3. Simplify skill implementation by leveraging CLI's built-in functionality
4. Ensure backward compatibility where possible
5. Identify gaps in CLI functionality that need to be addressed

## Current Architecture

**Before:**

- Skills call Python scripts directly via plugin registry
- Each skill manages argument building and output parsing
- Skills handle system-specific routing

**After:**

- Skills call `todu` CLI commands
- CLI handles all system routing, argument parsing, and formatting
- Skills focus on natural language parsing and user interaction

## Migration Mapping

### Project Management Skills

#### 1. project-register → `todu project add`

**Current Implementation:**

- Calls `register-project.py` with `--nickname`, `--system`, `--repo`, `--project-id`
- Handles nickname conflict resolution
- Validates project not already registered

**CLI Command:**

```bash
todu project add --name <nickname> --system <system> --external-id <repo-or-project-id>
```

**Changes Required:**

- Replace script call with `todu project add`
- Map `--nickname` → `--name`
- Map `--repo` or `--project-id` → `--external-id`
- Keep nickname conflict resolution logic
- Check if project exists using `todu project list --format json`
- Always use project name (not ID) in all CLI calls

**Status:** ✅ Direct mapping available

---

#### 2. project-list → `todu project list`

**Current Implementation:**

- Calls `list-projects.py` with `--format`, `--system`
- Displays projects grouped by system
- Shows nickname, repo/project-id, added date

**CLI Command:**

```bash
todu project list [--system <system>] [--format <table|json>]
```

**Changes Required:**

- Replace script call with `todu project list`
- Parse JSON output and format for display
- Maintain grouping by system in skill's display logic

**Status:** ✅ Direct mapping available

---

#### 3. project-update → `todu project update`

**Current Implementation:**

- Calls `update-project.py` with `--nickname`, `--new-nickname`, `--system`, `--repo`, `--project-id`
- Interactive field selection via AskUserQuestion
- Shows before/after comparison

**CLI Command:**

```bash
todu project update <name> [--name <new-name>] [--description <desc>] [--status <status>]
```

**Changes Required:**

- Replace script call with `todu project update`
- Use project name directly (CLI accepts name or ID)
- Map `--new-nickname` → `--name`
- Keep interactive field selection
- Note: CLI doesn't support changing system or external-id

**Status:** ⚠️ Partial mapping - system/external-id changes not supported

---

#### 4. project-delete → `todu project remove`

**Current Implementation:**

- Calls `delete-project.py` with `--nickname`
- Confirms deletion with AskUserQuestion
- Deletes cached issues by default
- Optional `--keep-issues` flag

**CLI Command:**

```bash
todu project remove <name> [--cascade] [--force]
```

**Changes Required:**

- Replace script call with `todu project remove`
- Use project name directly (CLI accepts name or ID)
- Map issue deletion behavior to `--cascade` flag
- Keep confirmation logic, skip `--force` unless user confirms

**Status:** ✅ Direct mapping available

---

### Task/Issue Management Skills

#### 5. task-create → `todu task create`

**Current Implementation:**

- Detects system from git remote or user input
- Calls project-register skill to ensure registration
- Extracts git context (branch, commits, files)
- Calls create script via plugin registry
- Prompts for title, description, labels, priority

**CLI Command:**

```bash
todu task create --project <project> --title <title> [--description <desc>] \
  [--label <label>]... [--priority <priority>] [--assignee <assignee>]... \
  [--due <YYYY-MM-DD>]
```

**Changes Required:**

- Replace script call with `todu task create`
- Keep git context extraction logic
- Use project name from git remote detection or user input
- Inject git context into `--description`
- Keep natural language prompting for fields
- Always use `--project <name>`, never use project ID

**Status:** ✅ Direct mapping available

---

#### 6. task-search → `todu task list`

**Current Implementation:**

- Calls `list-items.py` with filters: `--project`, `--status`, `--labels`, `--assignee`
- Searches local cache
- Groups results by project
- Displays unified todu ID format (#42)

**CLI Command:**

```bash
todu task list [--project <project>] [--status <status>] [--label <label>]... \
  [--assignee <assignee>] [--priority <priority>] [--search <text>] \
  [--due-before <date>] [--due-after <date>] [--limit <n>] [--format <text|json>]
```

**Changes Required:**

- Replace script call with `todu task list`
- Parse JSON output for custom formatting
- Maintain unified ID display format (#42)
- Keep grouping by project logic
- Map natural language to CLI filters

**Status:** ✅ Direct mapping available

---

#### 7. task-view → `todu task show`

**Current Implementation:**

- Parses task ID from user input
- Calls view script via plugin registry
- Fetches fresh data from API
- Displays title, description, status, labels, comments

**CLI Command:**

```bash
todu task show <id>
```

**Changes Required:**

- Replace script call with `todu task show`
- Pass task ID directly to CLI (no resolution needed)
- Parse and format CLI output
- Ensure comments are included

**Status:** ✅ Direct mapping available

---

#### 8. task-update → `todu task update` / `todu task close`

**Current Implementation:**

- Natural language parsing: "mark as done", "set priority high"
- Parses task ID from user input
- Calls update script via plugin registry
- Supports: status, priority, labels, assignees

**CLI Commands:**

```bash
# General update
todu task update <id> [--status <status>] [--priority <priority>] \
  [--add-label <label>]... [--remove-label <label>]... \
  [--add-assignee <user>]... [--remove-assignee <user>]... \
  [--title <title>] [--description <desc>] [--due <date>]

# Close shortcut
todu task close <id>
```

**Changes Required:**

- Replace script call with `todu task update` or `todu task close`
- Keep natural language parsing logic
- Map "mark as done" → `todu task close <id>`
- Map "set priority high" → `todu task update <id> --priority high`
- Pass task ID directly to CLI (no resolution needed)

**Status:** ✅ Direct mapping available

---

#### 9. task-comment-create → `todu task comment`

**Current Implementation:**

- Parses task ID from user input
- Prompts for comment body if not provided
- Calls comment script via plugin registry
- Supports markdown

**CLI Command:**

```bash
todu task comment <id> <text>
# or
todu task comment <id> --message <text>
```

**Changes Required:**

- Replace script call with `todu task comment`
- Pass task ID directly to CLI (no resolution needed)
- Keep comment body prompting
- Use `--message` flag or positional argument

**Status:** ✅ Direct mapping available

---

#### 10. task-sync → `todu sync`

**Current Implementation:**

- Detects system from git remote or nickname
- Calls project-register skill to ensure registration
- Calls sync script via plugin registry
- Reports: synced count, new, updated

**CLI Command:**

```bash
todu sync [--all] [--project <project>] [--system <system>] \
  [--dry-run] [--strategy <pull|push|bidirectional>]
```

**Changes Required:**

- Replace script call with `todu sync`
- Keep system/project detection from git
- Use project name directly with `--project <name>`
- Parse sync results from CLI output
- Note: May need to sync individual projects vs all

**Status:** ✅ Direct mapping available

---

### Reporting Skills

#### 11. task-report → `todu task list` (Multiple Calls)

**Current Implementation:**

- Calls `report.py` with `--type daily|weekly`
- Generates markdown reports
- Sections: In Progress, Due/Overdue, High Priority, Completed, Cancelled
- Uses local cache, no API calls

**CLI Commands:**

```bash
# Multiple calls to gather all needed data
todu task list --status active --format json
todu task list --due-before <today> --format json
todu task list --priority high --format json
# ... additional calls as needed
```

**Changes Required:**

- Replace single script call with multiple `todu task list` calls
- Use `--format json` to get structured data
- Calculate today's date in skill for date filtering
- Aggregate results from all calls
- Build markdown report from aggregated data
- Implement report generation logic in skill
- Support both daily and weekly report types
- Optional `--output` for saving to file

**CLI Calls Needed:**

**Daily Report:**

1. In Progress: `todu task list --status active --format json`
2. Overdue: `todu task list --due-before <yesterday> --format json`
3. Due Today: Calculate from due dates in all tasks
4. Coming Soon: `todu task list --due-after <today> --due-before <today+3days> --format json`
5. High Priority: `todu task list --priority high --format json`
6. Completed Today: Filter by updated date = today + status done/closed
7. Canceled Today: Filter by updated date = today + status canceled

**Weekly Report:**

1. Similar to daily but with week date ranges
2. Calculate week boundaries (Monday-Sunday)
3. Use `--due-before` and `--due-after` for date ranges

**Status:** ✅ Can be implemented with multiple CLI calls

---

#### 12. daily-review → `todu task list` (Multiple Calls)

**Current Implementation:**

- Calls `report.py --type daily`
- Validates cache freshness
- Sections: In Progress, Overdue, Due Today, Coming Soon, High Priority,
  Completed Today, Canceled Today

**CLI Commands:**

```bash
# Gather data with multiple todu task list calls
todu task list --status active --format json
todu task list --due-before <yesterday> --format json
todu task list --priority high --format json
todu task list --format json  # Get all tasks to filter by date ranges
```

**Changes Required:**

- Make 3-5 parallel `todu task list` calls with different filters
- Parse JSON output from each call
- Apply additional filtering in skill (dates, completion status)
- Check for `sync status` or sync metadata for cache freshness
- Build daily review markdown with proper sections
- Calculate "today", "overdue", "coming soon" in local timezone
- Group and format results

**Implementation Strategy:**

1. **Get all tasks once:** `todu task list --format json --limit 1000`
2. **Filter in skill logic:**
   - In Progress: Filter `status == "active"` or `status == "in-progress"`
   - Overdue: Filter `due_date < today` and `status != "done"`
   - Due Today: Filter `due_date == today`
   - Coming Soon: Filter `today < due_date <= today+3days`
   - High Priority: Filter `priority == "high"`
   - Completed Today: Filter `status == "done"` and `updated_at >= today`
   - Canceled Today: Filter `status == "canceled"` and `updated_at >= today`
3. **Format as markdown report**
4. **Optional:** Save to file if output path provided

**Status:** ✅ Direct implementation with CLI calls

---

#### 13. weekly-review → `todu task list` (Multiple Calls)

**Current Implementation:**

- Calls `weekly-review.py`
- Organizes by: Waiting, Next, Active, Backlog, Completed, Cancelled
- Uses label-based categorization (status:waiting, priority:high/medium/low)
- Filters completed/cancelled by calendar week

**CLI Commands:**

```bash
# Get all tasks and filter in skill
todu task list --format json --limit 1000

# Or use label filters if available
todu task list --label "status:waiting" --format json
todu task list --label "priority:high" --format json
todu task list --label "priority:medium" --format json
todu task list --label "priority:low" --format json
```

**Changes Required:**

- Call `todu task list --format json` once or multiple times with label filters
- Calculate calendar week boundaries (Monday-Sunday) in skill
- Filter tasks by labels in skill logic:
  - Waiting: `label includes "status:waiting"`
  - Next: `label includes "priority:high"`
  - Active: `label includes "priority:medium"`
  - Backlog: `label includes "priority:low"` or no priority label
  - Completed: `status == "done"` and `updated_at in current_week`
  - Canceled: `status == "canceled"` and `updated_at in current_week`
- Support `--week <YYYY-MM-DD>` parameter for specific week
- Build markdown report with sections
- Optional file output

**Implementation Strategy:**

1. **Calculate week range:**
   - Default: current week (Monday-Sunday)
   - If `--week` provided: use that Monday as start
2. **Get all tasks:** `todu task list --format json --limit 1000`
3. **Filter and categorize in skill:**
   - Parse labels array for priority/status
   - Parse updated_at timestamps for weekly completion
   - Group by category
4. **Format as markdown with checkboxes**
5. **Save to file if requested**

**Status:** ✅ Direct implementation with CLI calls

---

## Implementation Stages

### Stage 1: Convert All Skills (Skills 1-13)

**Goal:** Convert all skills to use `todu` CLI commands

**Tasks:**

**Project Management Skills:**

1. Update project-register skill to use `todu project add`
2. Update project-list skill to use `todu project list`
3. Update project-update skill to use `todu project update`
4. Update project-delete skill to use `todu project remove`

**Task Management Skills:**

1. Update task-create skill to use `todu task create`
2. Update task-search skill to use `todu task list`
3. Update task-view skill to use `todu task show`
4. Update task-update skill to use `todu task update`/`close`
5. Update task-comment-create skill to use `todu task comment`
6. Update task-sync skill to use `todu sync`

**Reporting Skills (Multiple CLI Calls):**

1. Update task-report skill to use multiple `todu task list` calls
2. Update daily-review skill to use multiple `todu task list` calls
3. Update weekly-review skill to use multiple `todu task list` calls

**Success Criteria:**

- All skills invoke `todu` CLI commands instead of Python scripts
- Natural language parsing preserved
- User interaction (AskUserQuestion) preserved
- Existing functionality maintained
- Reporting skills generate same output using aggregated CLI calls

**Tests Required:**

- Each skill end-to-end with various inputs
- Error handling for invalid inputs
- Edge cases (ambiguous tasks, missing projects, etc.)
- Report output validation (compare before/after)
- Performance testing for reporting skills (multiple CLI calls)

---

### Stage 2: Cleanup & Documentation

**Goal:** Clean up obsolete scripts and update documentation

**Tasks:**

1. Remove unused Python scripts from `core/scripts/`
2. Update skill documentation (SKILL.md files)
3. Update README files
4. Run `markdownlint-cli2 --fix "**/*.md"`
5. Test all skills end-to-end
6. Create migration guide for users

**Success Criteria:**

- No unused scripts remain
- Documentation accurate and current
- All tests passing
- Migration guide complete

---

## Breaking Changes & Considerations

### 1. Project Names (Not IDs)

**Issue:** Skills work with project nicknames/names, not numeric IDs

**Solution:**

- Always use project names when calling `todu` CLI commands
- CLI accepts either name or ID, so use names for consistency
- No need to look up project IDs
- Project names are more user-friendly and match existing skill behavior

### 2. External ID Changes Not Supported

**Issue:** `todu project update` doesn't support changing external-id or system

**Solution:**

- Document limitation in skill
- Suggest using `project remove` + `project add` for these changes
- Or keep Python script for this specific functionality

### 3. Task ID Handling

**Issue:** How to handle task IDs when calling CLI

**Solution:**

- Pass task IDs directly to `todu` CLI commands
- No need for `resolve_task()` - CLI handles system routing internally
- Skills can parse task IDs from user input (natural language)
- CLI takes care of mapping to correct system and external ID

### 4. Output Formatting

**Issue:** CLI has different output formats than Python scripts

**Solution:**

- Use `--format json` for all CLI calls
- Parse JSON and format for display in skills
- Maintain consistent user experience

### 5. Git Context Extraction

**Issue:** CLI doesn't extract git context automatically

**Solution:**

- Keep git context extraction in task-create skill
- Inject context into `--description` field
- Maintain current functionality

---

## Testing Strategy

### Unit Tests

- Test each skill's natural language parsing
- Test CLI command construction
- Test output parsing and formatting

### Integration Tests

- End-to-end tests for each skill
- Test with real todu CLI
- Test error conditions

### Regression Tests

- Ensure existing workflows still work
- Compare output before/after migration
- Test edge cases

---

## Rollback Plan

If migration causes issues:

1. Keep Python scripts temporarily
2. Add feature flag to switch between script and CLI
3. Allow gradual rollout per skill
4. Monitor for issues and revert if needed

---

## Timeline Estimates

### Stage 1: Convert All Skills (Skills 1-13)

**Duration:** 4-6 days

**Breakdown:**

- Project management skills (4 skills): 1 day
- Task management skills (6 skills): 2 days
- Reporting skills (3 skills): 1-2 days
  - More complex due to multiple CLI calls
  - Report generation logic in skill
  - Date filtering and aggregation
- Testing and validation: 1 day

### Stage 2: Cleanup & Documentation

**Duration:** 1-2 days

- Remove unused Python scripts
- Update documentation
- Run markdown linter
- Final end-to-end testing
- Create migration guide

**Total:** 5-8 days

---

## Dependencies

### Required Before Starting

- ✅ `todu` CLI installed and working
- ✅ All plugins registered in CLI
- ✅ Projects migrated to CLI's database
- ✅ `todu task list` supports all needed filters (--status, --priority, --label,
  --due-before, --due-after, --format json)

### External Dependencies

- None! All functionality can be implemented using existing CLI commands

---

## Success Metrics

1. **Code Reduction:** Reduce skill code by ~50-60%
   - No argument building for system-specific APIs
   - No plugin registry routing logic
   - No `resolve_task()` or ID mapping
   - No system detection/resolution code
2. **Maintainability:** Single source of truth in CLI for all operations
3. **Consistency:** All operations go through same code path
4. **Performance:** No degradation in skill response time
5. **Compatibility:** All existing workflows continue working
6. **Simplicity:** Skills focus purely on natural language → CLI command mapping

---

## Risks & Mitigation

### Risk 1: Performance of Multiple CLI Calls for Reports

**Issue:** Reporting skills need to make multiple `todu task list` calls, which
may be slower than single Python script execution

**Mitigation:**

- Use single `todu task list --format json --limit 1000` call to get all tasks
- Filter and aggregate in skill logic (in-memory operations are fast)
- Only make multiple calls if absolutely necessary for performance
- Benchmark before/after to measure actual impact
- Consider adding caching if needed

### Risk 2: Breaking Changes to User Workflows

**Mitigation:** Maintain skill interfaces, thorough testing

### Risk 3: Task ID Parsing from Natural Language

**Mitigation:**

- Keep natural language parsing in skills
- Extract task ID from user input ("issue 42", "task #15", etc.)
- Pass parsed ID directly to CLI
- CLI handles all system routing

### Risk 4: Date/Time Calculations in Skills

**Issue:** Skills need to handle timezone-aware date calculations for reports

**Mitigation:**

- Use skill's environment date/time functions
- Test with different timezones
- Document timezone handling clearly
- Match Python script behavior exactly

---

## Notes

- All skills should continue to use the Skill tool invocation pattern
- Skills maintain responsibility for natural language understanding
- CLI handles all system-specific implementation details
- Error messages should remain user-friendly
- Markdown formatting preserved throughout
- **IMPORTANT:** Always use project names (not IDs) in all `todu` CLI calls
  - The CLI accepts either name or ID
  - Project names are user-friendly and match current skill behavior
  - No need for ID lookup or mapping
- **Task IDs:** Pass directly to CLI - no `resolve_task()` needed
  - Skills only need to parse task ID from user's natural language input
  - CLI handles all system routing and external ID mapping
  - No need for ID registry or resolution logic

---

## Next Steps

1. Review this plan
2. Verify `todu` CLI has all required functionality:
   - `todu task list --format json` with filters
   - `todu project` commands accept names
   - `todu sync` accepts project names
3. Begin Stage 1 implementation:
   - Start with project management skills (simpler)
   - Move to task management skills
   - Finish with reporting skills (most complex)
4. Test thoroughly at each step
5. Document any CLI issues or missing features discovered
