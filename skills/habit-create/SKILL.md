---
name: core-habit-create
description: Create habits to track and build over time. Use when user says "create a habit", "track a habit", "start tracking *", "I want to build a habit of *", "add a habit", "new habit", "track daily *", "create habit for *", or similar queries. (plugin:core@todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Create Habit

This skill creates habit tracking templates using `todu template create --type
habit`. Habits are recurring behaviors you want to build and track over time
(exercise, meditation, reading, etc.).

## When to Use

- User wants to create a habit to track
- User says "create a habit", "track a habit", "start tracking", etc.
- User wants to build a regular behavior or routine
- User mentions habit-related activities (exercise, meditate, read, etc.)

## What This Skill Does

1. **Parse Request for Details**
   - Extract project name if provided
   - Extract habit name/title if provided
   - Extract frequency (daily, specific days, etc.)
   - Extract start date if provided
   - Extract other optional fields if mentioned

2. **Identify Project**
   - If parsed from request: use it
   - If not provided: check for default project via `todu config show`
   - If default project exists: use it (inform user)
   - If no default: run `todu project list --format json` and ask user

3. **Gather Required Fields**
   - **Title** (required): The habit name - only ask if not parsed
   - **Recurrence** (required): Convert natural language to RRULE or ask user
   - **Start Date** (required): Default to today if not specified

4. **Build RRULE from Natural Language**
   - Convert user-friendly frequency to RRULE format
   - Default to daily if no frequency specified (most common for habits)
   - See conversion table below

5. **Create Template**
   - Build CLI command with all gathered fields
   - Use `--type habit` and `--format json`
   - Execute command

6. **Display Confirmation**
   - Show created habit details (ID, name, schedule)
   - Show next occurrence date
   - Show success message

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

## Day Abbreviations for RRULE

| Day       | Abbreviation |
|-----------|--------------|
| Monday    | MO           |
| Tuesday   | TU           |
| Wednesday | WE           |
| Thursday  | TH           |
| Friday    | FR           |
| Saturday  | SA           |
| Sunday    | SU           |

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

## Direct Parsing Patterns

Parse these patterns from user requests:

| User says                  | Parsed fields                            |
|----------------------------|------------------------------------------|
| "habit in PROJECT"         | project = PROJECT                        |
| "habit to ACTIVITY"        | title = ACTIVITY                         |
| "habit of ACTIVITY"        | title = ACTIVITY                         |
| "track ACTIVITY"           | title = ACTIVITY                         |
| "daily"                    | recurrence = FREQ=DAILY                  |
| "every day"                | recurrence = FREQ=DAILY                  |
| "every weekday"            | recurrence = FREQ=WEEKLY;BYDAY=MO,TU,... |
| "Mon/Wed/Fri"              | recurrence = FREQ=WEEKLY;BYDAY=MO,WE,FR  |
| "3 times a week"           | recurrence = FREQ=WEEKLY;BYDAY=MO,WE,FR  |
| "starting DATE"            | start_date = DATE                        |

## CLI Interface

**Get default project:**

```bash
todu config show
# Extract value after "Project:" in Defaults section
```

**List all projects** (if no default):

```bash
todu project list --format json
```

**Create habit template:**

```bash
# Required flags
todu template create \
  --project <name> \
  --title <habit-name> \
  --recurrence <RRULE> \
  --start-date <YYYY-MM-DD> \
  --type habit \
  --format json

# With all optional flags
todu template create \
  --project <name> \
  --title <habit-name> \
  --recurrence <RRULE> \
  --start-date <YYYY-MM-DD> \
  --type habit \
  --description <text> \
  --priority <low|medium|high> \
  --end-date <YYYY-MM-DD> \
  --timezone <IANA timezone> \
  --label <label1> --label <label2> \
  --assignee <user1> --assignee <user2> \
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

## Prompting Strategy

**Key principle**: Parse as much as possible from request. Default to daily if
no frequency specified.

1. **Project**:
   - If in request: use it
   - If default exists: use it (tell user)
   - Otherwise: ask user to select

2. **Title**:
   - If in request: use it
   - Otherwise: ask user "What habit do you want to track?"

3. **Recurrence**:
   - If frequency mentioned: convert to RRULE
   - If not specified: default to daily (most common for habits)
   - For "X times a week": suggest specific days or ask user

4. **Start Date**:
   - If in request: use it
   - Otherwise: default to today's date

5. **Optional Fields**:
   - Only use values provided in request
   - Don't prompt for optional fields unless mentioned but missing value

## Error Handling

- **No projects exist**: Inform user they need to register a project first
- **Project not found**: List available projects and suggest correct name
- **Invalid RRULE**: Help user build valid recurrence pattern
- **Invalid date format**: Explain YYYY-MM-DD format and ask again
- **CLI errors**: Parse error output and show meaningful message
- **Missing required fields**: Prompt for each missing field

## Future Considerations

When todu adds streak tracking for habits, this skill should be updated to:

- Show current streak count after creation
- Display streak statistics in confirmation
- Potentially add habit-specific fields (target count, reminder times, etc.)

## Notes

- Always use `--type habit` for habits (not task)
- Start date defaults to today if not specified
- **Default to daily** if no frequency is specified (unlike recurring-create)
- Timezone defaults to UTC; consider asking if user mentions specific times
- The RRULE format follows RFC 5545 (iCalendar) standard
- Labels and assignees are repeatable flags
- Parse natural language frequencies to make it easy for users
- Show human-readable schedule in confirmation (not raw RRULE)
- Habit names are often activities: "exercise", "meditate", "read", etc.
