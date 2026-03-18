---
name: recurring-update
description: Update, pause, or resume recurring task templates. Use when user says "update recurring task *", "pause recurring task *", "resume recurring task *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Update Recurring Task

Updates recurring task templates using `todu recurring update`,
`todu recurring pause`, or `todu recurring resume`.

## Natural Language Patterns

### Pause/Resume
- "pause recurring task 14" → `todu recurring pause 14`
- "resume recurring task 14" → `todu recurring resume 14`

### Update Fields
- "rename recurring task 14 to 'Morning standup'" → `--title "Morning standup"`
- "change recurring task 14 to daily" → `--schedule "FREQ=DAILY;INTERVAL=1"`
- "set priority high on recurring task 14" → `--priority high`
- "change the miss policy to roll forward" → `--miss-policy rollForward`

## Examples

### Pause/Resume

**User**: "Pause recurring task 14"

Runs: `todu recurring pause 14`

### Change schedule

**User**: "Change recurring task 14 to daily"

Runs: `todu recurring update 14 --schedule "FREQ=DAILY;INTERVAL=1"`

### Multiple updates

**User**: "Update recurring task 14: change to weekly and set priority low"

Runs: `todu recurring update 14 --schedule "FREQ=WEEKLY;INTERVAL=1" --priority low`

## CLI Commands

```bash
# Pause/Resume

todu recurring pause <id>
todu recurring resume <id>

# Update fields

todu recurring update <id> --title "New title"
todu recurring update <id> --schedule "FREQ=DAILY;INTERVAL=1"
todu recurring update <id> --priority high
todu recurring update <id> --description "text"
todu recurring update <id> --label label1 --label label2
todu recurring update <id> --miss-policy rollForward
todu recurring update <id> --project <project>
todu recurring update <id> --end-date 2026-12-31
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

- "pause" / "stop" map to `todu recurring pause`; "resume" / "start" map to `todu recurring resume`
- `--label` replaces the current label set
- RRULE follows RFC 5545 standard
- Description must be valid markdown
