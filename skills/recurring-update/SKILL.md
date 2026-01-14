---
name: core-recurring-update
description: Update, activate, or deactivate recurring task templates. Use when user says "update recurring task *", "change recurring task *", "modify recurring task *", "activate recurring task *", "deactivate recurring task *", "pause recurring task *", "resume recurring task *", "change schedule for *", or similar queries. (plugin:core@todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Update Recurring Task

This skill updates recurring task templates using `todu template update`,
`todu template activate`, and `todu template deactivate`.

## When to Use

- User wants to update a recurring task's properties
- User wants to change the schedule/recurrence
- User wants to pause (deactivate) a recurring task
- User wants to resume (activate) a recurring task
- User says "update recurring task", "change schedule", "pause", "resume", etc.

## What This Skill Does

1. **Parse Update Request**
   - Extract template ID from user's request
   - Parse what to update (title, recurrence, priority, etc.)
   - Detect activate/deactivate intent

2. **Determine CLI Command**
   - "pause" / "deactivate" / "stop" → `todu template deactivate <id>`
   - "resume" / "activate" / "start" → `todu template activate <id>`
   - Field updates → `todu template update <id> [flags]`

3. **Build CLI Command**
   - Add appropriate flags based on parsed updates
   - Execute command

4. **Display Results**
   - Show what was updated
   - Confirm the changes
   - Display updated template details

## CLI Commands

**Update template fields:**

```bash
todu template update <id> --title "New title"
todu template update <id> --recurrence "FREQ=DAILY;INTERVAL=1"
todu template update <id> --priority high
todu template update <id> --description "New description"
todu template update <id> --timezone "America/New_York"
todu template update <id> --end-date 2025-12-31
todu template update <id> --label label1 --label label2
todu template update <id> --assignee user1 --assignee user2
```

**Activate (resume) template:**

```bash
todu template activate <id>
```

**Deactivate (pause) template:**

```bash
todu template deactivate <id>
```

## Available Update Fields

| Field       | Flag            | Description                    |
|-------------|-----------------|--------------------------------|
| Title       | `--title`       | Update template title          |
| Description | `--description` | Update description             |
| Recurrence  | `--recurrence`  | Update RRULE recurrence        |
| End Date    | `--end-date`    | Update end date (YYYY-MM-DD)   |
| Priority    | `--priority`    | Update priority (low/med/high) |
| Timezone    | `--timezone`    | Update IANA timezone           |
| Labels      | `--label`       | Replace labels (repeatable)    |
| Assignees   | `--assignee`    | Replace assignees (repeatable) |

**Note**: Labels and assignees are replaced, not appended.

## Natural Language Parsing

| User says                              | Action                              |
|----------------------------------------|-------------------------------------|
| "update recurring task 5"              | Ask what to update                  |
| "change title of recurring task 5"     | `--title` (ask for new title)       |
| "rename recurring task 5 to X"         | `--title "X"`                       |
| "change schedule of task 5 to daily"   | `--recurrence "FREQ=DAILY;..."`     |
| "set recurring task 5 to weekly"       | `--recurrence "FREQ=WEEKLY;..."`    |
| "pause recurring task 5"               | `todu template deactivate 5`        |
| "deactivate recurring task 5"          | `todu template deactivate 5`        |
| "stop recurring task 5"                | `todu template deactivate 5`        |
| "resume recurring task 5"              | `todu template activate 5`          |
| "activate recurring task 5"            | `todu template activate 5`          |
| "start recurring task 5"               | `todu template activate 5`          |
| "set priority high on task 5"          | `--priority high`                   |
| "change timezone to America/New_York"  | `--timezone "America/New_York"`     |

## RRULE Conversion for Schedule Changes

When user wants to change the schedule, convert natural language:

| User Says            | RRULE                              |
|----------------------|------------------------------------|
| "daily"              | `FREQ=DAILY;INTERVAL=1`            |
| "every weekday"      | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "weekly"             | `FREQ=WEEKLY;INTERVAL=1`           |
| "every Monday"       | `FREQ=WEEKLY;BYDAY=MO`             |
| "Mon/Wed/Fri"        | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "monthly"            | `FREQ=MONTHLY;INTERVAL=1`          |
| "on the 1st"         | `FREQ=MONTHLY;BYMONTHDAY=1`        |

## Example Interactions

### Example 1: Pause recurring task

**User**: "Pause recurring task 14"

**Skill**:

1. Parses: id=14, action=deactivate
2. Executes: `todu template deactivate 14`
3. Shows: "Recurring task #14 paused (deactivated)"

### Example 2: Resume recurring task

**User**: "Resume recurring task 14"

**Skill**:

1. Parses: id=14, action=activate
2. Executes: `todu template activate 14`
3. Shows: "Recurring task #14 resumed (activated)"

### Example 3: Change schedule

**User**: "Change recurring task 14 to daily"

**Skill**:

1. Parses: id=14, update=recurrence, value="daily"
2. Converts to RRULE: `FREQ=DAILY;INTERVAL=1`
3. Executes: `todu template update 14 --recurrence "FREQ=DAILY;INTERVAL=1"`
4. Shows: "Recurring task #14 updated: schedule changed to daily"

### Example 4: Update title

**User**: "Rename recurring task 14 to 'Morning standup'"

**Skill**:

1. Parses: id=14, update=title, value="Morning standup"
2. Executes: `todu template update 14 --title "Morning standup"`
3. Shows: "Recurring task #14 updated: title changed"

### Example 5: Update priority

**User**: "Set priority high on recurring task 14"

**Skill**:

1. Parses: id=14, update=priority, value=high
2. Executes: `todu template update 14 --priority high`
3. Shows: "Recurring task #14 updated: priority=high"

### Example 6: Multiple updates

**User**: "Update recurring task 14: change to weekly and set priority low"

**Skill**:

1. Parses: id=14, updates=[recurrence:weekly, priority:low]
2. Executes: `todu template update 14 --recurrence "FREQ=WEEKLY;INTERVAL=1"
   --priority low`
3. Shows: "Recurring task #14 updated: schedule=weekly, priority=low"

### Example 7: Generic update request

**User**: "Update recurring task 14"

**Skill**:

1. Parses: id=14, no specific update mentioned
2. Asks: "What would you like to update?"
   - Title
   - Schedule/Recurrence
   - Priority
   - Pause/Deactivate
3. User selects and provides new value
4. Executes appropriate command

## Error Handling

- **Template not found**: "Recurring task #X not found"
- **Invalid ID**: "Please provide a valid template ID"
- **Invalid recurrence**: Help user build valid RRULE
- **Invalid priority**: "Priority must be: low, medium, or high"
- **Already active**: "Recurring task #X is already active"
- **Already inactive**: "Recurring task #X is already paused"
- **CLI errors**: Parse and display error message

## Notes

- Template ID is required for all update operations
- Use `todu template activate/deactivate` for status changes
- Use `todu template update` for field changes
- Labels and assignees are replaced entirely (not appended)
- Convert natural language schedules to RRULE format
- "pause", "stop", "deactivate" all mean deactivate
- "resume", "start", "activate" all mean activate
- Multiple fields can be updated in a single command
