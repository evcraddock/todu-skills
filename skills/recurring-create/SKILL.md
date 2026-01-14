---
name: core-recurring-create
description: Create recurring tasks that repeat on a schedule. Use when user says "create a recurring task", "set up a weekly task", "make this repeat every *", "schedule a daily task", "create a task that repeats", "add a recurring task", "set up a monthly task", "create a task every *", "schedule recurring *", or similar queries. (plugin:core@todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Create Recurring Task

This skill creates recurring task templates using `todu template create --type
task`. Recurring tasks automatically generate new task instances based on a
schedule (daily, weekly, monthly, etc.).

## When to Use

- User wants to create a task that repeats on a schedule
- User says "create a recurring task", "set up a weekly task", etc.
- User wants to schedule something that happens regularly
- User mentions frequency like "daily", "every Monday", "monthly"

## What This Skill Does

1. **Parse Request for Details**
   - Extract project name if provided
   - Extract title if provided
   - Extract frequency/schedule (daily, weekly, specific days, monthly, etc.)
   - Extract start date if provided
   - Extract other optional fields if mentioned

2. **Identify Project**
   - If parsed from request: use it
   - If not provided: check for default project via `todu config show`
   - If default project exists: use it (inform user)
   - If no default: run `todu project list --format json` and ask user

3. **Gather Required Fields**
   - **Title** (required): Only ask if not parsed from request
   - **Recurrence** (required): Convert natural language to RRULE or ask user
   - **Start Date** (required): Default to today if not specified

4. **Build RRULE from Natural Language**
   - Convert user-friendly frequency to RRULE format
   - See conversion table below

5. **Create Template**
   - Build CLI command with all gathered fields
   - Use `--type task` and `--format json`
   - Execute command

6. **Display Confirmation**
   - Show created template details (ID, title, schedule)
   - Show next occurrence date
   - Show success message

## Natural Language to RRULE Conversion

| User Says            | RRULE                              |
|----------------------|------------------------------------|
| "daily"              | `FREQ=DAILY;INTERVAL=1`            |
| "every day"          | `FREQ=DAILY;INTERVAL=1`            |
| "every 2 days"       | `FREQ=DAILY;INTERVAL=2`            |
| "every 3 days"       | `FREQ=DAILY;INTERVAL=3`            |
| "weekly"             | `FREQ=WEEKLY;INTERVAL=1`           |
| "every week"         | `FREQ=WEEKLY;INTERVAL=1`           |
| "every Monday"       | `FREQ=WEEKLY;BYDAY=MO`             |
| "every Tuesday"      | `FREQ=WEEKLY;BYDAY=TU`             |
| "every Wednesday"    | `FREQ=WEEKLY;BYDAY=WE`             |
| "every Thursday"     | `FREQ=WEEKLY;BYDAY=TH`             |
| "every Friday"       | `FREQ=WEEKLY;BYDAY=FR`             |
| "every Saturday"     | `FREQ=WEEKLY;BYDAY=SA`             |
| "every Sunday"       | `FREQ=WEEKLY;BYDAY=SU`             |
| "every weekday"      | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "weekdays"           | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "Mon/Wed/Fri"        | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "Tue/Thu"            | `FREQ=WEEKLY;BYDAY=TU,TH`          |
| "every 2 weeks"      | `FREQ=WEEKLY;INTERVAL=2`           |
| "biweekly"           | `FREQ=WEEKLY;INTERVAL=2`           |
| "monthly"            | `FREQ=MONTHLY;INTERVAL=1`          |
| "every month"        | `FREQ=MONTHLY;INTERVAL=1`          |
| "on the 1st"         | `FREQ=MONTHLY;BYMONTHDAY=1`        |
| "on the 15th"        | `FREQ=MONTHLY;BYMONTHDAY=15`       |
| "first of the month" | `FREQ=MONTHLY;BYMONTHDAY=1`        |
| "last day of month"  | `FREQ=MONTHLY;BYMONTHDAY=-1`       |
| "yearly"             | `FREQ=YEARLY;INTERVAL=1`           |
| "every year"         | `FREQ=YEARLY;INTERVAL=1`           |
| "annually"           | `FREQ=YEARLY;INTERVAL=1`           |

For complex patterns not in this table, ask the user to clarify or help them
build the RRULE.

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

### Example 1: Full details in request

**User**: "Create a recurring task in todu-skills: Weekly review, every Friday"

**Skill**:

1. Parses: project="todu-skills", title="Weekly review", frequency="every Friday"
2. Converts frequency: `FREQ=WEEKLY;BYDAY=FR`
3. Uses today as start date
4. Executes: `todu template create --project todu-skills --title "Weekly review"
   --recurrence "FREQ=WEEKLY;BYDAY=FR" --start-date 2025-11-28 --type task
   --format json`
5. Shows: "Created recurring task: Weekly review (every Friday)"

### Example 2: Daily task with default project

**User**: "Set up a daily standup reminder"

**Skill**:

1. Parses: title="daily standup reminder", frequency="daily"
2. Runs `todu config show` → default project is "Inbox"
3. Shows: "Using default project: Inbox"
4. Converts frequency: `FREQ=DAILY;INTERVAL=1`
5. Uses today as start date
6. Executes: `todu template create --project Inbox --title "daily standup
   reminder" --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28
   --type task --format json`
7. Shows: "Created recurring task: daily standup reminder (daily)"

### Example 3: Weekday task

**User**: "Create a recurring task: Check emails every weekday"

**Skill**:

1. Parses: title="Check emails", frequency="every weekday"
2. Checks for default project or asks user
3. Converts frequency: `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR`
4. Executes with appropriate flags
5. Shows: "Created recurring task: Check emails (Mon-Fri)"

### Example 4: Monthly task

**User**: "Schedule a monthly review on the 1st"

**Skill**:

1. Parses: title="monthly review", frequency="monthly on the 1st"
2. Converts frequency: `FREQ=MONTHLY;BYMONTHDAY=1`
3. Asks for project if needed
4. Executes with appropriate flags
5. Shows: "Created recurring task: monthly review (1st of each month)"

### Example 5: Minimal request

**User**: "Create a recurring task"

**Skill**:

1. No details parsed
2. Asks for title: "What should this recurring task be called?"
3. Asks for frequency: "How often should it repeat?"
   - Daily
   - Weekly
   - Specific days (Mon, Wed, Fri, etc.)
   - Monthly
   - Custom
4. Asks for project if no default
5. Creates template with gathered info

## Direct Parsing Patterns

Parse these patterns from user requests:

| User says                   | Parsed fields                            |
|-----------------------------|------------------------------------------|
| "recurring task in PROJECT" | project = PROJECT                        |
| "called 'TITLE'"            | title = TITLE                            |
| "recurring task: TITLE"     | title = TITLE                            |
| "every day/daily"           | recurrence = FREQ=DAILY                  |
| "every Monday"              | recurrence = FREQ=WEEKLY;BYDAY=MO        |
| "every weekday"             | recurrence = FREQ=WEEKLY;BYDAY=MO,TU,... |
| "weekly on DAY"             | recurrence = FREQ=WEEKLY;BYDAY=XX        |
| "monthly"                   | recurrence = FREQ=MONTHLY                |
| "starting DATE"             | start_date = DATE                        |
| "high priority"             | priority = high                          |
| "with description 'TEXT'"   | description = TEXT                       |

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

**Create recurring task template:**

```bash
# Required flags
todu template create \
  --project <name> \
  --title <title> \
  --recurrence <RRULE> \
  --start-date <YYYY-MM-DD> \
  --type task \
  --format json

# With all optional flags
todu template create \
  --project <name> \
  --title <title> \
  --recurrence <RRULE> \
  --start-date <YYYY-MM-DD> \
  --type task \
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
| Recurrence  | `--recurrence`  | Yes      | RRULE format           | -       |
| Start Date  | `--start-date`  | Yes      | YYYY-MM-DD             | today   |
| Type        | `--type`        | Yes      | task                   | task    |
| Description | `--description` | No       | Any text               | empty   |
| Priority    | `--priority`    | No       | low, medium, high      | medium  |
| End Date    | `--end-date`    | No       | YYYY-MM-DD             | none    |
| Timezone    | `--timezone`    | No       | IANA timezone          | UTC     |
| Labels      | `--label`       | No       | Any text (repeatable)  | none    |
| Assignees   | `--assignee`    | No       | Username (repeatable)  | none    |

## Prompting Strategy

**Key principle**: Parse as much as possible from request. Only ask for missing
required fields.

1. **Project**:
   - If in request: use it
   - If default exists: use it (tell user)
   - Otherwise: ask user to select

2. **Title**:
   - If in request: use it
   - Otherwise: ask user

3. **Recurrence**:
   - If frequency mentioned: convert to RRULE
   - Otherwise: ask with common options (daily, weekly, specific days, monthly)

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

## Notes

- Always use `--type task` for recurring tasks (not habits)
- Start date defaults to today if not specified
- Timezone defaults to UTC; consider asking if user mentions specific times
- The RRULE format follows RFC 5545 (iCalendar) standard
- Labels and assignees are repeatable flags
- Parse natural language frequencies to make it easy for users
- Show human-readable schedule in confirmation (not raw RRULE)
