---
name: habit-update
description: MANDATORY skill for updating habit templates. NEVER call update scripts directly - ALWAYS use this skill via the Skill tool. Use when user says "update habit *", "change habit *", "modify habit *", "pause habit *", "resume habit *", "activate habit *", "deactivate habit *", or similar queries to modify a habit. (plugin:core@todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Update Habit

**MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY habit update
request.**

**NEVER call `todu template update`, `todu template activate`, or
`todu template deactivate` directly. This skill provides essential logic:**

- Natural language parsing ("pause my exercise habit", "change habit 11 to
  weekly")
- Field extraction (title, recurrence, priority, labels, assignees, etc.)
- Habit verification before updating
- Command selection (update vs activate vs deactivate)
- Validation of values
- Providing clear feedback about changes

---

This skill updates properties of habit templates using `todu template update`,
`todu template activate`, and `todu template deactivate` CLI commands.

## When to Use

- User wants to update/modify/change a habit property
- User wants to pause or deactivate a habit
- User wants to resume or activate a habit
- User wants to change habit schedule/frequency
- User wants to add or change labels, priority, or assignees
- User provides ANY update instruction for a habit

## What This Skill Does

1. **Parse Update Request**
   - Extract habit ID from user's request
   - If no habit ID, search by name using `todu template list --type habit`
   - Parse what to update (title, recurrence, priority, labels, etc.)
   - Detect activate/deactivate requests

2. **Verify Habit and Show Context**
   - Run `todu template show <id>` to verify habit exists
   - Display habit title so user confirms they're updating the right one
   - Example: "Updating habit #11: exercise"

3. **Determine CLI Command**
   - "pause" / "deactivate" / "stop" → `todu template deactivate <id>`
   - "resume" / "activate" / "unpause" → `todu template activate <id>`
   - All other updates → `todu template update <id> [flags]`

4. **Build CLI Command**
   - Add appropriate flags based on parsed updates:
     - `--title <new title>`
     - `--description <new description>`
     - `--recurrence <RRULE>`
     - `--priority <priority>` (low, medium, high)
     - `--label <label>` (replaces all labels)
     - `--assignee <user>` (replaces all assignees)
     - `--end-date <YYYY-MM-DD>`
     - `--timezone <IANA timezone>`

5. **Execute Command**
   - Run the CLI command
   - Capture output

6. **Report Results**
   - Show what was updated
   - Confirm the changes
   - Display updated habit details

## Natural Language Patterns

The skill understands these natural language patterns:

### Activate/Deactivate

- "pause habit 11" → `todu template deactivate 11`
- "pause my exercise habit" → find ID, then deactivate
- "deactivate habit 11" → `todu template deactivate 11`
- "stop habit 11" → `todu template deactivate 11`
- "resume habit 11" → `todu template activate 11`
- "activate habit 11" → `todu template activate 11`
- "unpause habit 11" → `todu template activate 11`
- "start habit 11 again" → `todu template activate 11`

### Title

- "rename habit 11 to 'Morning exercise'" →
  `todu template update 11 --title "Morning exercise"`
- "change habit 11 name to 'Workout'" →
  `todu template update 11 --title "Workout"`

### Recurrence/Schedule

- "change habit 11 to weekly" →
  `todu template update 11 --recurrence "FREQ=WEEKLY;INTERVAL=1"`
- "update habit 11 to Mon/Wed/Fri" →
  `todu template update 11 --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"`
- "make habit 11 daily" →
  `todu template update 11 --recurrence "FREQ=DAILY;INTERVAL=1"`

### Priority

- "set habit 11 to high priority" → `todu template update 11 --priority high`
- "make habit 11 low priority" → `todu template update 11 --priority low`

### Labels

- "add label health to habit 11" → `todu template update 11 --label health`
- "set labels on habit 11 to fitness and wellness" →
  `todu template update 11 --label fitness --label wellness`

### Assignees

- "assign habit 11 to alice" → `todu template update 11 --assignee alice`

### End Date

- "set end date on habit 11 to 2025-12-31" →
  `todu template update 11 --end-date 2025-12-31`

## Example Interactions

### Example 1: Pause a habit

**User**: "Pause my exercise habit"

**Skill**:

1. Parses: action=pause, habit name="exercise"
2. Runs: `todu template list --type habit --format json` to find ID
3. Finds: habit #11 "exercise"
4. Confirms: "I found habit #11: exercise. Pausing..."
5. Executes: `todu template deactivate 11`
6. Shows: "Habit #11 (exercise) has been paused. It will no longer generate
   tasks until reactivated."

### Example 2: Resume a habit

**User**: "Resume habit 11"

**Skill**:

1. Parses: ID=11, action=resume
2. Runs: `todu template show 11` → title="exercise"
3. Shows: "Resuming habit #11: exercise"
4. Executes: `todu template activate 11`
5. Shows: "Habit #11 (exercise) is now active"

### Example 3: Change schedule

**User**: "Change habit 11 to Mon/Wed/Fri"

**Skill**:

1. Parses: ID=11, update=recurrence:"Mon/Wed/Fri"
2. Runs: `todu template show 11` → title="exercise"
3. Converts: "Mon/Wed/Fri" → `FREQ=WEEKLY;BYDAY=MO,WE,FR`
4. Shows: "Updating habit #11: exercise"
5. Executes: `todu template update 11 --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"`
6. Shows: "Habit #11 updated: schedule changed to Mon, Wed, Fri"

### Example 4: Update title and priority

**User**: "Rename habit 11 to 'Morning workout' and set high priority"

**Skill**:

1. Parses: ID=11, updates=[title:"Morning workout", priority:high]
2. Runs: `todu template show 11` → current title="exercise"
3. Shows: "Updating habit #11: exercise"
4. Executes:
   `todu template update 11 --title "Morning workout" --priority high`
5. Shows: "Habit #11 updated: title='Morning workout', priority=high"

### Example 5: No habit ID provided

**User**: "Pause my meditation habit"

**Skill**:

1. Parses: action=pause, habit name="meditation"
2. Runs: `todu template list --type habit --format json`
3. Searches for habits matching "meditation"
4. If one match: proceed with that ID
5. If multiple matches: ask user to choose
6. If no matches: "No habit found matching 'meditation'. Here are your habits:"

### Example 6: Update by ID

**User**: "Update habit 11 to daily"

**Skill**:

1. Parses: ID=11, update=recurrence:daily
2. Runs: `todu template show 11` → title="exercise"
3. Converts: "daily" → `FREQ=DAILY;INTERVAL=1`
4. Shows: "Updating habit #11: exercise"
5. Executes: `todu template update 11 --recurrence "FREQ=DAILY;INTERVAL=1"`
6. Shows: "Habit #11 updated: schedule changed to daily"

## CLI Command Reference

**Verify habit exists:**

```bash
todu template show <id>
```

**Activate a habit (resume):**

```bash
todu template activate <id>
```

**Deactivate a habit (pause):**

```bash
todu template deactivate <id>
```

**Update habit fields:**

```bash
# Update title
todu template update <id> --title "New habit name"

# Update recurrence
todu template update <id> --recurrence "FREQ=DAILY;INTERVAL=1"
todu template update <id> --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"

# Update priority
todu template update <id> --priority low
todu template update <id> --priority medium
todu template update <id> --priority high

# Update description
todu template update <id> --description "New description"

# Update end date
todu template update <id> --end-date 2025-12-31

# Update timezone
todu template update <id> --timezone "America/New_York"

# Replace labels (multiple flags = multiple labels)
todu template update <id> --label health --label fitness

# Replace assignees (multiple flags = multiple assignees)
todu template update <id> --assignee alice --assignee bob

# Combine multiple updates
todu template update <id> --title "Morning workout" --priority high \
  --recurrence "FREQ=DAILY;INTERVAL=1"
```

**Search for habit by name:**

```bash
todu template list --type habit --format json
# Parse JSON to find matching habit by title
```

## Natural Language to RRULE Conversion

| User Says            | RRULE                              |
|----------------------|------------------------------------|
| "daily"              | `FREQ=DAILY;INTERVAL=1`            |
| "every day"          | `FREQ=DAILY;INTERVAL=1`            |
| "every weekday"      | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "weekdays"           | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| "every Monday"       | `FREQ=WEEKLY;BYDAY=MO`             |
| "Mon/Wed/Fri"        | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "Tue/Thu"            | `FREQ=WEEKLY;BYDAY=TU,TH`          |
| "3 times a week"     | `FREQ=WEEKLY;BYDAY=MO,WE,FR`       |
| "twice a week"       | `FREQ=WEEKLY;BYDAY=TU,TH`          |
| "weekly"             | `FREQ=WEEKLY;INTERVAL=1`           |
| "every week"         | `FREQ=WEEKLY;INTERVAL=1`           |

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

## Valid Values

### Priority Values

- `low` - Low priority
- `medium` - Normal priority
- `high` - High priority

### Recurrence Values

Must be valid RRULE format following RFC 5545 (iCalendar) standard.

### Date Format

Must be in YYYY-MM-DD format.

### Timezone Values

Must be valid IANA timezone (e.g., "America/New_York", "Europe/London", "UTC").

## Natural Language Parsing Guide

When parsing user requests:

1. **Extract Habit ID**
   - Look for numbers: "habit 11", "#11", "habit #11"
   - If not found: search by name in template list
   - If multiple matches: ask user to choose
   - If no matches: show available habits

2. **Detect Action**
   - "pause", "deactivate", "stop" → use `todu template deactivate`
   - "resume", "activate", "unpause", "start again" →
     use `todu template activate`
   - Everything else → use `todu template update`

3. **Extract Updates**
   - Title: "rename to X", "change name to X", "change title to X"
   - Recurrence: "change to daily", "make it weekly", "set to Mon/Wed/Fri"
   - Priority: "priority high", "make it high priority", "set priority low"
   - Labels: "add label X", "set labels to X and Y"
   - Assignees: "assign to X", "set assignee to X"
   - End date: "set end date to X", "end on X"
   - Description: "update description to X"
   - Timezone: "set timezone to X", "change timezone to X"

4. **Handle Multiple Updates**
   - Combine all flags in a single command
   - Example: "--title 'New name' --priority high --recurrence 'FREQ=DAILY'"

## Error Handling

- **Habit ID missing**: Search by name or ask user
- **Habit not found**: "Habit #X not found. Please check the habit ID."
- **Invalid priority**: "Invalid priority. Use: low, medium, or high"
- **Invalid date format**: "Date must be in YYYY-MM-DD format"
- **Invalid RRULE**: Help user build valid recurrence pattern
- **No habits match search**: Show list of available habits
- **CLI errors**: Display the error message from the CLI

## Notes

- "pause" and "resume" are user-friendly aliases for deactivate/activate
- Deactivating a habit stops task generation but preserves the habit
- Activating a habit resumes task generation
- Labels and assignees use `--label` and `--assignee` flags (replaces all)
- Unlike task-update, there's no `--add-label` or `--remove-label`
- Title is a direct replacement
- Always verify habit exists before updating to show context to user
- Convert natural language frequencies to RRULE format
- Show human-readable schedule in confirmations (not raw RRULE)
