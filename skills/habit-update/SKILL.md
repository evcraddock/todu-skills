---
name: habit-update
description: Update, pause, or resume habit templates. Use when user says "update habit *", "change habit *", "pause habit *", "resume habit *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Update Habit

Updates habits using `todu habit update`, `todu habit pause`, or `todu habit resume`.

## Natural Language Patterns

### Pause/Resume
- "pause habit 11" → `todu habit pause 11`
- "resume habit 11" → `todu habit resume 11`

### Update Fields
- "rename habit 11 to 'Morning exercise'" → `--title "Morning exercise"`
- "change habit 11 to weekly" → `--schedule "FREQ=WEEKLY;INTERVAL=1"`
- "change habit 11 to Mon/Wed/Fri" → `--schedule "FREQ=WEEKLY;BYDAY=MO,WE,FR"`
- "set the habit to end on 2026-12-31" → `--end-date 2026-12-31`
- "update the description for habit 11" → `--description "..."`

## Example Interactions

### Example 1: Pause a habit

**User**: "Pause my exercise habit"

1. Runs `todu habit list --format json` to find ID
2. Finds habit #11 "exercise"
3. Executes: `todu habit pause 11`
4. Shows: "Habit #11 (exercise) paused."

### Example 2: Change schedule

**User**: "Change habit 11 to Mon/Wed/Fri"

1. Runs `todu habit show 11` → title="exercise"
2. Converts: "Mon/Wed/Fri" → `FREQ=WEEKLY;BYDAY=MO,WE,FR`
3. Executes: `todu habit update 11 --schedule "FREQ=WEEKLY;BYDAY=MO,WE,FR"`
4. Shows: "Habit #11 updated: schedule changed to Mon, Wed, Fri"

### Example 3: Multiple updates

**User**: "Rename habit 11 to 'Morning workout' and end it on 2026-12-31"

1. Runs `todu habit show 11`
2. Executes: `todu habit update 11 --title "Morning workout" --end-date 2026-12-31`
3. Shows: "Habit #11 updated: title='Morning workout', end date=2026-12-31"

## CLI Commands

```bash
# Verify habit exists

todu habit show <id>

# Pause/Resume

todu habit pause <id>
todu habit resume <id>

# Update fields

todu habit update <id> --title "New name"
todu habit update <id> --schedule "FREQ=DAILY;INTERVAL=1"
todu habit update <id> --description "text"
todu habit update <id> --end-date 2026-12-31
todu habit update <id> --timezone America/Chicago

# Search by name

todu habit list --format json
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

- RRULE follows RFC 5545 standard
- The current CLI updates labels and priority on recurring tasks, not habits
- Description must be valid markdown
