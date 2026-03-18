---
name: recurring-create
description: Create recurring tasks that repeat on a schedule. Use when user says "create recurring task", "schedule a weekly/daily/monthly task", "task every *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Create Recurring Task

Creates recurring task templates using `todu recurring create`.

## Natural Language to RRULE Conversion

| User Says            | RRULE                              |
|----------------------|------------------------------------|
| "daily"              | `FREQ=DAILY;INTERVAL=1`            |
| "every 2 days"       | `FREQ=DAILY;INTERVAL=2`            |
| "weekly"             | `FREQ=WEEKLY;INTERVAL=1`           |
| "every Monday"       | `FREQ=WEEKLY;BYDAY=MO`             |
| "every weekday"      | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "Mon/Wed/Fri"        | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "biweekly"           | `FREQ=WEEKLY;INTERVAL=2`           |
| "monthly"            | `FREQ=MONTHLY;INTERVAL=1`          |
| "on the 1st"         | `FREQ=MONTHLY;BYMONTHDAY=1`        |
| "last day of month"  | `FREQ=MONTHLY;BYMONTHDAY=-1`       |
| "yearly"             | `FREQ=YEARLY;INTERVAL=1`           |

## Example Interactions

### Example 1: Full details

**User**: "Create a recurring task in todu-skills: Weekly review, every Friday"

1. Parses: project="todu-skills", title="Weekly review", frequency="every Friday"
2. Converts: `FREQ=WEEKLY;BYDAY=FR`
3. Runs: `todu recurring create --project todu-skills --title "Weekly review" --schedule "FREQ=WEEKLY;BYDAY=FR" --start-date 2026-03-18 --format json`

### Example 2: Monthly task

**User**: "Schedule a monthly review on the 1st"

1. Parses: title="monthly review", frequency="on the 1st"
2. Converts: `FREQ=MONTHLY;BYMONTHDAY=1`
3. Asks for project if no project is specified
4. Creates the recurring template

### Example 3: Minimal request

**User**: "Create a recurring task"

1. Asks for title
2. Asks for frequency (daily/weekly/specific days/monthly)
3. Asks for project
4. Creates the recurring template

## CLI Commands

```bash
# List projects when the user does not specify one

todu project list --format json

# Create recurring task

todu recurring create \
  --project <name> \
  --title <title> \
  --schedule <RRULE> \
  --start-date <YYYY-MM-DD> \
  --format json

# Optional flags
--description <text>
--priority <low|medium|high>
--end-date <YYYY-MM-DD>
--timezone <IANA timezone>
--miss-policy <accumulate|rollForward>
--label <label>
```

## Notes

- RRULE follows RFC 5545 (iCalendar) standard
- Start date defaults to today if omitted
- Ask for frequency if it is not specified (unlike habit-create, which defaults to daily)
- Description must be valid markdown
