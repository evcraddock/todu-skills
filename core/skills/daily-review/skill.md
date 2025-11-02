---
name: daily-review
description: MANDATORY skill for generating daily task reviews. NEVER call scripts/report.py directly - ALWAYS use this skill via the Skill tool. Use when user wants to view, show, or display a daily review. (plugin:core@todu)
---

# Generate Daily Task Review

**⚠️ MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY
daily review request.**

**NEVER EVER call `report.py` directly. This skill provides essential logic
beyond just running the script:**

- Validating cache freshness across all systems
- Suggesting sync if cache is stale
- Parsing optional output file path from user query
- Handling errors gracefully with helpful messages
- Providing clear summary of today's work

Even if you've invoked this skill before in the conversation, you MUST invoke
it again for each new daily review request.

---

This skill generates a daily task review by aggregating locally cached tasks
from all Task Management Systems (GitHub, Forgejo, Todoist).

## When to Use

- User explicitly requests a "daily review" or "daily report"
- User asks to "show daily review" or "display daily review"
- User wants to see what tasks need attention today
- User wants a summary of today's completed work

## What This Skill Does

1. **Validate Cache**
   - Check last sync times for all systems
   - Warn if cache is stale (> 24 hours)
   - Suggest running sync before generating report

2. **Generate Report**
   - Call `$PLUGIN_DIR/scripts/report.py --type daily`
   - Aggregate data from all three systems
   - Apply timezone conversion for local dates
   - Format results as markdown

3. **Handle Output**
   - Save to specified file path if user provided one
   - Display report to user
   - Confirm file location if saved

## Report Sections

The daily review includes:

- **In Progress**: Tasks with status `in-progress` or `open` with assignees
- **Overdue**: Tasks with due dates before today
- **Due Today**: Tasks with due dates equal to today
- **Coming Soon**: Tasks due in the next 3 days (excludes today and overdue)
- **High Priority**: Tasks with `priority:high` label or Todoist priority >= 3
- **Completed Today**: Tasks marked `done`/`closed` today
- **Canceled Today**: Tasks marked `canceled` today

## Example Interactions

**User**: "Show me the daily review"
**Skill**:

```text
Checking cache freshness...
✓ GitHub: synced 2 hours ago
✓ Forgejo: synced 3 hours ago
✓ Todoist: synced 1 hour ago

# Daily Task Review - 2025-10-31

## Summary
- **In Progress**: 0 tasks
- **Due**: 0 tasks
- **Coming Soon**: 2 tasks
- **High Priority**: 1 tasks
- **Completed Today**: 5 tasks
- **Canceled Today**: 2 tasks

[... rest of report ...]
```

**User**: "Generate daily review and save to ~/Documents/daily.md"
**Skill**:

- Parses: output=~/Documents/daily.md
- Generates report
- Saves to file
- Confirms: "Report saved to: /Users/erik/Documents/daily.md"

## Script Interface

```bash
# Daily report to stdout
$PLUGIN_DIR/scripts/report.py --type daily

# Daily report to file
$PLUGIN_DIR/scripts/report.py --type daily --output ~/daily.md
```

## Example Output Format

```markdown
# Daily Task Review - 2025-10-31

## Summary
- **In Progress**: 0 tasks
- **Due**: 0 tasks
- **Coming Soon**: 2 tasks
- **High Priority**: 1 tasks
- **Completed Today**: 5 tasks
- **Canceled Today**: 2 tasks

## 📆 Coming Soon (2)

**Update API documentation**
  System: github • Project: todu • ID: 42 • Due: 2025-11-03 (tomorrow)
  https://github.com/example/todu/issues/42

**Review pull request #15**
  System: forgejo • Project: vault • ID: 33 • Due: 2025-11-04 (in 2 days)
  https://forgejo.caradoc.com/example/vault/issues/33

## 🔥 High Priority (1)

**Create skill for downloading daily report**
  System: forgejo • Project: Vault • ID: 11
  https://forgejo.caradoc.com/erik/Vault/issues/11

## ✅ Completed Today (5)

**Consolidate task-search into core plugin**
  System: github • Project: todu • ID: 17 • Status: done
  https://github.com/evcraddock/todu/issues/17

[... more completed tasks ...]

## ❌ Canceled Today (2)

**testing out github issues**
  System: github • Project: rott • ID: 13 • Labels: priority:high
  https://github.com/evcraddock/rott/issues/13

[... more canceled tasks ...]
```

## Technical Details

### Timezone Handling

- All timestamps stored in UTC with 'Z' suffix
- Reports use user's system timezone for date calculations
- "Today", "overdue", "completed today" calculated in local time
- Report headers show dates in local timezone

### Priority Mapping

- Labels `priority:high/medium/low` recognized across all systems
- Todoist priority: 4=high, 3=medium, 2=low, 1=none
- Tasks without priority labels shown as "none"

### Due Date Handling

- Only Todoist has explicit due dates
- GitHub/Forgejo show "-" for due date
- Due date comparison uses local timezone dates
- Overdue = due date < today
- Due today = due date == today

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
- Completed/Canceled sections only show tasks from today
