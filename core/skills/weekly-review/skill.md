---
name: weekly-review
description: MANDATORY skill for generating weekly task reviews. NEVER call scripts/weekly-review.py directly - ALWAYS use this skill via the Skill tool. Use when user wants to view, show, or display a weekly review. (plugin:core@todu)
---

# Generate Weekly Task Review

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY
weekly review request.**

**NEVER EVER call `weekly-review.py` directly. This skill provides
essential logic beyond just running the script:**

- Validating cache freshness across all systems
- Suggesting sync if cache is stale
- Parsing optional output file path from user query
- Handling errors gracefully with helpful messages
- Providing clear summary of the week's work organized by status and
  priority

Even if you've invoked this skill before in the conversation, you MUST
invoke it again for each new weekly review request.

---

This skill generates a weekly task review by aggregating locally cached
tasks from all Task Management Systems (GitHub, Forgejo, Todoist),
organized by status and priority.

## When to Use

- User explicitly requests a "weekly review" or "weekly report"
- User asks to "show weekly review" or "display weekly review"
- User wants to see tasks organized by priority and status
- User wants a summary of the week's completed and cancelled work

## What This Skill Does

1. **Validate Cache**
   - Check last sync times for all systems
   - Warn if cache is stale (> 24 hours)
   - Suggest running sync before generating report

2. **Generate Report**
   - Call `$PLUGIN_DIR/scripts/weekly-review.py`
   - Aggregate data from all three systems
   - Filter by labels (status:waiting, priority:high/medium/low)
   - Filter completed/cancelled by calendar week boundaries
   - Apply timezone conversion for local dates
   - Format results as markdown

3. **Handle Output**
   - Save to specified file path if user provided one
   - Display report to user
   - Confirm file location if saved

## Report Sections

The weekly review includes:

- **Waiting**: Tasks with `status:waiting` label (blocked or waiting on
  external dependencies)
- **Next**: Tasks with `priority:high` label (high priority items to
  tackle soon)
- **Active**: Tasks with `priority:medium` label (currently active work
  items)
- **Backlog**: Tasks with `priority:low` label (lower priority items for
  later)
- **Completed This Week**: Tasks marked `done`/`closed` during the
  calendar week (Monday-Sunday)
- **Cancelled This Week**: Tasks marked `canceled` during the calendar week

## Example Interactions

**User**: "Show me the weekly review"
**Skill**:

```text
Checking cache freshness...
✓ GitHub: synced 2 hours ago
✓ Forgejo: synced 3 hours ago
✓ Todoist: synced 1 hour ago

# Weekly Review - Week of 2025-10-28

## Summary
- **Waiting**: 3 tasks
- **Next**: 5 tasks
- **Active**: 8 tasks
- **Backlog**: 12 tasks
- **Completed**: 15 tasks
- **Cancelled**: 2 tasks

[... rest of report ...]
```

**User**: "Generate weekly review and save to ~/Documents/weekly.md"
**Skill**:

- Parses: output=~/Documents/weekly.md
- Generates report for current week
- Saves to file
- Confirms: "Report saved to: /Users/erik/Documents/weekly.md"

**User**: "Generate weekly review for last week"
**Skill**:

- Calculates last week's Monday-Sunday range
- Generates report with `--week` flag
- Displays results

## Script Interface

```bash
# Weekly review to stdout (current week)
$PLUGIN_DIR/scripts/weekly-review.py

# Weekly review to file
$PLUGIN_DIR/scripts/weekly-review.py --output ~/weekly.md

# Weekly review for specific week
$PLUGIN_DIR/scripts/weekly-review.py --week 2025-10-21 \
  --output ~/weekly.md
```

## Example Output Format

```markdown
# Weekly Review: 10-28-2025 to 11-03-2025

*This is a read-only report. Checkboxes are for visual reference only
and are not interactive.*

## Summary
- **Waiting**: 3 tasks
- **Next**: 5 tasks
- **Active**: 8 tasks
- **Backlog**: 12 tasks
- **Completed**: 15 tasks
- **Cancelled**: 2 tasks

## 🔒 Waiting (3)

- [ ] **#15 - Waiting for API access**
  System: github • Project: todu • System ID: #42 • Priority: high •
  Due: 2025-11-05
  https://github.com/example/todu/issues/42

- [ ] **#22 - Blocked on design review**
  System: todoist • Project: marketing • System ID: abc12345
  https://todoist.com/showTask?id=abc12345

## 🔥 Next (5)

- [ ] **#8 - Fix authentication bug**
  System: github • Project: todu • System ID: #35 • Assignee: alice • Due: 2025-11-04
  https://github.com/example/todu/issues/35

- [ ] **#12 - Deploy to production**
  System: forgejo • Project: backend • System ID: #18 • Assignee: bob
  https://forgejo.example.com/team/backend/issues/18

## 🚧 Active (8)

- [ ] **#18 - Implement user dashboard**
  System: github • Project: frontend • System ID: #44 • Assignee: charlie
  https://github.com/example/frontend/issues/44

- [ ] **#25 - Write documentation**
  System: todoist • Project: docs • System ID: def45678 • Due: 2025-11-06
  https://todoist.com/showTask?id=def45678

## 📋 Backlog (12)

- [ ] **#30 - Refactor legacy code**
  System: github • Project: todu • System ID: #50
  https://github.com/example/todu/issues/50

- [ ] **#41 - Add dark mode**
  System: forgejo • Project: frontend • System ID: #22
  https://forgejo.example.com/team/frontend/issues/22

## ✅ Completed This Week (15)

- [x] **#10 - Write documentation**
  System: todoist • Completed: 2025-10-30 • Labels: docs
  https://todoist.com/showTask?id=xyz78901

- [x] **#23 - Fix authentication bug #123**
  System: github • Project: todu • System ID: #123 •
  Completed: 2025-10-29 • Labels: bug
  https://github.com/example/todu/issues/123

## ❌ Cancelled This Week (2)

**#35 - Review old feature**
  System: todoist • Cancelled: 2025-10-29 • Labels: wontfix
  https://todoist.com/showTask?id=old12345
```

## Technical Details

### Timezone Handling

- All timestamps stored in UTC with 'Z' suffix
- Reports use user's system timezone for date calculations
- Calendar week: Monday (start) to Sunday (end)
- Completion dates calculated in local time

### Priority Mapping

- Labels `priority:high/medium/low` recognized across all systems
- Todoist priority: 4=high, 3=medium, 2=low, 1=none
- Tasks without priority labels excluded from priority sections

### Status Labels

- `status:waiting` identifies blocked tasks
- Recognized across all systems via label standardization

### Week Calculation

- Default: Current calendar week (Monday-Sunday)
- `--week` flag: Specify any Monday to get that week's range
- Week boundaries calculated in user's local timezone

### Cache Location

- Unified cache: `~/.local/todu/sync.json` (sync metadata)
- GitHub: `~/.local/todu/github/issues/*.json`
- Forgejo: `~/.local/todu/forgejo/issues/*.json`
- Todoist: `~/.local/todu/todoist/tasks/*.json`

## Cache Freshness

Suggest syncing if any system hasn't synced in > 24 hours:

```bash
# Check sync metadata
cat ~/.local/todu/sync.json

# If stale, suggest:
"Your cache is stale. Run sync first for accurate results:
  todu sync github
  todu sync forgejo
  todu sync todoist
"
```

## Notes

- Reports are generated from local cache (no API calls)
- Fast and works offline
- All date/time calculations use user's system timezone
- Empty sections are omitted from output
- Completed/Canceled sections only show tasks from the calendar week
- Tasks must have explicit priority labels to appear in Next/Active/Backlog sections
