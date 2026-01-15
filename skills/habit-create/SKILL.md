---
name: habit-create
description: Create habits to track and build over time. Use when user says "create a habit", "track a habit", "start tracking *", "I want to build a habit of *", "add a habit", "new habit", "track daily *", "create habit for *", or similar queries. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Create Habit

This skill creates habit tracking templates using `todu template create --type
habit`. Habits are recurring behaviors you want to build and track over time
(exercise, meditation, reading, etc.).

## Natural Language to RRULE Conversion

| User Says            | RRULE                              |
|----------------------|------------------------------------|
| "daily"              | `FREQ=DAILY;INTERVAL=1`            |
| "every day"          | `FREQ=DAILY;INTERVAL=1`            |
| "every morning"      | `FREQ=DAILY;INTERVAL=1`            |
| "every night"        | `FREQ=DAILY;INTERVAL=1`            |
| "every weekday"      | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "weekdays"           | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "every Monday"       | `FREQ=WEEKLY;BYDAY=MO`             |
| "every Tuesday"      | `FREQ=WEEKLY;BYDAY=TU`             |
| "every Wednesday"    | `FREQ=WEEKLY;BYDAY=WE`             |
| "every Thursday"     | `FREQ=WEEKLY;BYDAY=TH`             |
| "every Friday"       | `FREQ=WEEKLY;BYDAY=FR`             |
| "every Saturday"     | `FREQ=WEEKLY;BYDAY=SA`             |
| "every Sunday"       | `FREQ=WEEKLY;BYDAY=SU`             |
| "Mon/Wed/Fri"        | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "Tue/Thu"            | `FREQ=WEEKLY;BYDAY=TU,TH`          |
| "3 times a week"     | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "twice a week"       | `FREQ=WEEKLY;BYDAY=TU,TH`          |
| "weekly"             | `FREQ=WEEKLY;INTERVAL=1`           |
| "every week"         | `FREQ=WEEKLY;INTERVAL=1`           |

**Default**: If no frequency is specified, default to daily (`FREQ=DAILY;INTERVAL=1`)
since most habits are daily activities.

## Example Interactions

### Example 1: Simple daily habit

**User**: "Create a habit to exercise daily"

**Skill**:

1. Parses: title="exercise", frequency="daily"
2. Checks for default project or asks user
3. Converts frequency: `FREQ=DAILY;INTERVAL=1`
4. Uses today as start date
5. Executes: `todu template create --project Inbox --title "exercise"
   --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit
   --format json`
6. Shows: "Created habit: exercise (daily)"

### Example 2: Habit with specific days

**User**: "I want to build a habit of going to the gym Mon/Wed/Fri"

**Skill**:

1. Parses: title="going to the gym", frequency="Mon/Wed/Fri"
2. Converts frequency: `FREQ=WEEKLY;BYDAY=MO,WE,FR`
3. Executes with appropriate flags
4. Shows: "Created habit: going to the gym (Mon, Wed, Fri)"

### Example 3: Habit without frequency (defaults to daily)

**User**: "Track a meditation habit"

**Skill**:

1. Parses: title="meditation", no frequency specified
2. Defaults to daily: `FREQ=DAILY;INTERVAL=1`
3. Executes with appropriate flags
4. Shows: "Created habit: meditation (daily)"

### Example 4: Weekday habit

**User**: "Create a habit to read every weekday"

**Skill**:

1. Parses: title="read", frequency="every weekday"
2. Converts frequency: `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR`
3. Executes with appropriate flags
4. Shows: "Created habit: read (Mon-Fri)"

### Example 5: Minimal request

**User**: "Create a habit"

**Skill**:

1. No details parsed
2. Asks for habit name: "What habit do you want to track?"
3. Asks for frequency: "How often?"
   - Daily
   - Specific days (Mon, Wed, Fri, etc.)
   - Weekdays only
   - Custom
4. Asks for project if no default
5. Creates habit with gathered info

### Example 6: "3 times a week"

**User**: "Start tracking exercise 3 times a week"

**Skill**:

1. Parses: title="exercise", frequency="3 times a week"
2. Suggests: "How about Mon, Wed, Fri?" or asks user to specify days
3. Converts to: `FREQ=WEEKLY;BYDAY=MO,WE,FR`
4. Creates habit

## CLI Interface

```bash
todu template create \
  --project <name> \
  --title <habit-name> \
  --recurrence <RRULE> \
  --start-date <YYYY-MM-DD> \
  --type habit \
  --format json
```

## Available Fields

| Field       | Flag            | Required | Valid Values           | Default |
|-------------|-----------------|----------|------------------------|---------|
| Project     | `--project`     | Yes      | Any registered project | -       |
| Title       | `--title`       | Yes      | Any text               | -       |
| Recurrence  | `--recurrence`  | Yes      | RRULE format           | daily   |
| Start Date  | `--start-date`  | Yes      | YYYY-MM-DD             | today   |
| Type        | `--type`        | Yes      | habit                  | habit   |
| Description | `--description` | No       | Any text               | empty   |
| Priority    | `--priority`    | No       | low, medium, high      | medium  |
| End Date    | `--end-date`    | No       | YYYY-MM-DD             | none    |
| Timezone    | `--timezone`    | No       | IANA timezone          | UTC     |
| Labels      | `--label`       | No       | Any text (repeatable)  | none    |
| Assignees   | `--assignee`    | No       | Username (repeatable)  | none    |

## Error Handling

- **No projects exist**: Inform user they need to register a project first
- **Invalid RRULE**: Help user build valid recurrence pattern

## Notes

- The RRULE format follows RFC 5545 (iCalendar) standard
- Consider asking for timezone if user mentions specific times
- Unlike recurring-create, this skill defaults to daily when no frequency is specified
- Description must be valid markdown
