---
name: habit-update
description: Update, pause, or resume habit templates. Use when user says "update habit *", "change habit *", "pause habit *", "resume habit *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Update Habit

Updates habit templates using `todu template update`, `activate`, or `deactivate`.

## Natural Language Patterns

### Activate/Deactivate
- "pause habit 11" → `todu template deactivate 11`
- "resume habit 11" → `todu template activate 11`

### Update Fields
- "rename habit 11 to 'Morning exercise'" → `--title "Morning exercise"`
- "change habit 11 to weekly" → `--recurrence "FREQ=WEEKLY;INTERVAL=1"`
- "change habit 11 to Mon/Wed/Fri" → `--recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"`
- "set habit 11 to high priority" → `--priority high`
- "add label health to habit 11" → `--label health`

## Example Interactions

### Example 1: Pause a habit

**User**: "Pause my exercise habit"

1. Runs `todu template list --type habit --format json` to find ID
2. Finds habit #11 "exercise"
3. Executes: `todu template deactivate 11`
4. Shows: "Habit #11 (exercise) paused."

### Example 2: Change schedule

**User**: "Change habit 11 to Mon/Wed/Fri"

1. Runs `todu template show 11` → title="exercise"
2. Converts: "Mon/Wed/Fri" → `FREQ=WEEKLY;BYDAY=MO,WE,FR`
3. Executes: `todu template update 11 --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"`
4. Shows: "Habit #11 updated: schedule changed to Mon, Wed, Fri"

### Example 3: Multiple updates

**User**: "Rename habit 11 to 'Morning workout' and set high priority"

1. Runs `todu template show 11`
2. Executes: `todu template update 11 --title "Morning workout" --priority high`
3. Shows: "Habit #11 updated: title='Morning workout', priority=high"

## CLI Commands

```bash
# Verify habit exists
todu template show <id>

# Pause/Resume
todu template deactivate <id>
todu template activate <id>

# Update fields
todu template update <id> --title "New name"
todu template update <id> --recurrence "FREQ=DAILY;INTERVAL=1"
todu template update <id> --priority high
todu template update <id> --label health --label fitness
todu template update <id> --assignee alice
todu template update <id> --end-date 2025-12-31

# Search by name
todu template list --type habit --format json
```

## Natural Language to RRULE

| User Says            | RRULE                              |
|----------------------|------------------------------------|
| "daily"              | `FREQ=DAILY;INTERVAL=1`            |
| "every weekday"      | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "Mon/Wed/Fri"        | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "weekly"             | `FREQ=WEEKLY;INTERVAL=1`           |

## Error Handling

- **Habit not found**: Show available habits
- **Multiple matches**: Ask user to choose

## Notes

- "pause"/"resume" are aliases for deactivate/activate
- `--label` and `--assignee` replace all existing values
- RRULE follows RFC 5545 standard
- Description must be valid markdown
