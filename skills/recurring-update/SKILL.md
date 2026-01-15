---
name: recurring-update
description: Update, pause, or resume recurring task templates. Use when user says "update recurring task *", "pause recurring task *", "resume recurring task *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Update Recurring Task

Updates recurring task templates using `todu template update`, `activate`, or `deactivate`.

## Natural Language Patterns

### Activate/Deactivate
- "pause recurring task 14" → `todu template deactivate 14`
- "resume recurring task 14" → `todu template activate 14`

### Update Fields
- "rename recurring task 14 to 'Morning standup'" → `--title "Morning standup"`
- "change recurring task 14 to daily" → `--recurrence "FREQ=DAILY;INTERVAL=1"`
- "set priority high on recurring task 14" → `--priority high`

## Examples

### Pause/Resume

**User**: "Pause recurring task 14"

Runs: `todu template deactivate 14`

### Change schedule

**User**: "Change recurring task 14 to daily"

Runs: `todu template update 14 --recurrence "FREQ=DAILY;INTERVAL=1"`

### Multiple updates

**User**: "Update recurring task 14: change to weekly and set priority low"

Runs: `todu template update 14 --recurrence "FREQ=WEEKLY;INTERVAL=1" --priority low`

## CLI Commands

```bash
# Pause/Resume
todu template deactivate <id>
todu template activate <id>

# Update fields
todu template update <id> --title "New title"
todu template update <id> --recurrence "FREQ=DAILY;INTERVAL=1"
todu template update <id> --priority high
todu template update <id> --description "text"
todu template update <id> --label label1 --label label2
todu template update <id> --assignee user1
```

## RRULE Conversion

| User Says       | RRULE                              |
|-----------------|------------------------------------|
| "daily"         | `FREQ=DAILY;INTERVAL=1`            |
| "every weekday" | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "Mon/Wed/Fri"   | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "weekly"        | `FREQ=WEEKLY;INTERVAL=1`           |
| "monthly"       | `FREQ=MONTHLY;INTERVAL=1`          |

## Notes

- "pause"/"stop" → deactivate; "resume"/"start" → activate
- `--label` and `--assignee` replace all existing values
- RRULE follows RFC 5545 standard
- Description must be valid markdown
