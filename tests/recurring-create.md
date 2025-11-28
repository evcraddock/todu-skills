# Recurring Create Skill Test

Test the recurring-create skill with these prompts:

## Test 1: Create recurring task with full details

```text
create a recurring task in todu-tests: Weekly review, every Friday
```

Expected: Parse project, title, and frequency. Convert "every Friday" to
RRULE `FREQ=WEEKLY;BYDAY=FR`. Use today as start date. Create template.

## Test 2: Create daily recurring task

```text
set up a daily standup reminder
```

Expected: Parse title and "daily" frequency. Check for default project or ask.
Convert to `FREQ=DAILY;INTERVAL=1`. Create template.

## Test 3: Create weekday recurring task

```text
create a recurring task: Check emails every weekday
```

Expected: Parse title and "every weekday". Convert to
`FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR`. Ask for project if needed.

## Test 4: Create monthly recurring task

```text
schedule a monthly review on the 1st
```

Expected: Parse title and "monthly on the 1st". Convert to
`FREQ=MONTHLY;BYMONTHDAY=1`. Ask for project if needed.

## Test 5: Minimal request - no details

```text
create a recurring task
```

Expected: Ask for title, ask for frequency (daily, weekly, specific days,
monthly, custom), ask for project if no default. Create template.

## Test 6: Specific days of week

```text
create a recurring task: Exercise on Mon/Wed/Fri
```

Expected: Parse title and days. Convert to `FREQ=WEEKLY;BYDAY=MO,WE,FR`.

## Test 7: Biweekly task

```text
set up a biweekly team sync
```

Expected: Parse title and "biweekly". Convert to `FREQ=WEEKLY;INTERVAL=2`.

## Test 8: With start date specified

```text
create a recurring task: Pay rent monthly starting 2025-01-01
```

Expected: Parse title, frequency, and start date. Use provided start date
instead of today.

## Test 9: With priority

```text
create a high priority recurring task: Daily backup check
```

Expected: Parse title, frequency (daily), and priority. Include --priority high.

## Test 10: Error - no projects exist

```text
create a recurring task
```

Expected: If no projects exist, inform user they need to register a project
first.

## Test 11: Complex request with multiple fields

```text
create a recurring task in todu-tests: Sprint planning every 2 weeks, high priority
```

Expected: Parse project, title, frequency (every 2 weeks = INTERVAL=2),
priority. Create template with all fields.

## Test 12: Yearly task

```text
schedule an annual review every year
```

Expected: Parse "every year" or "annual". Convert to `FREQ=YEARLY;INTERVAL=1`.

## CLI Verification Commands

Run from tests/ directory to verify templates were created:

```bash
cd tests && todu template list --type task --format json
```

```bash
cd tests && todu template show <id> --format json
```

## Cleanup

Delete test templates after testing:

```bash
cd tests && todu template delete <id>
```
