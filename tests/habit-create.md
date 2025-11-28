# Habit Create Skill Test

Test the habit-create skill with these prompts:

## Test 1: Simple daily habit

```text
create a habit to exercise daily
```

Expected: Parse title="exercise", frequency="daily". Convert to
`FREQ=DAILY;INTERVAL=1`. Ask for project if needed. Create habit.

## Test 2: Habit with specific days

```text
I want to build a habit of going to the gym Mon/Wed/Fri
```

Expected: Parse title and days. Convert to `FREQ=WEEKLY;BYDAY=MO,WE,FR`.
Create habit.

## Test 3: Habit without frequency (defaults to daily)

```text
track a meditation habit
```

Expected: Parse title="meditation". Default to daily since no frequency
specified. Create habit with `FREQ=DAILY;INTERVAL=1`.

## Test 4: Weekday habit

```text
create a habit to read every weekday
```

Expected: Parse title="read", frequency="every weekday". Convert to
`FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR`. Create habit.

## Test 5: Minimal request - no details

```text
create a habit
```

Expected: Ask "What habit do you want to track?", ask for frequency (daily,
specific days, weekdays, custom), ask for project if no default. Create habit.

## Test 6: "3 times a week"

```text
start tracking exercise 3 times a week
```

Expected: Parse title="exercise", frequency="3 times a week". Suggest Mon/Wed/Fri
or ask for specific days. Convert to `FREQ=WEEKLY;BYDAY=MO,WE,FR`.

## Test 7: Twice a week

```text
track a yoga habit twice a week
```

Expected: Parse title="yoga", frequency="twice a week". Suggest Tue/Thu or ask
for specific days. Convert to `FREQ=WEEKLY;BYDAY=TU,TH`.

## Test 8: With project specified

```text
create a habit in mytest: drink water daily
```

Expected: Parse project="mytest", title="drink water", frequency="daily".
Create habit without asking for project.

## Test 9: Every morning/night

```text
track a journaling habit every morning
```

Expected: Parse title="journaling", frequency="every morning". Convert to
`FREQ=DAILY;INTERVAL=1`. Create daily habit.

## Test 10: Error - no projects exist

```text
create a habit
```

Expected: If no projects exist, inform user they need to register a project
first.

## Test 11: Weekly habit

```text
create a habit for weekly meal prep
```

Expected: Parse title="meal prep", frequency="weekly". Convert to
`FREQ=WEEKLY;INTERVAL=1`. Create habit.

## Test 12: Build a habit phrasing

```text
I want to build a habit of drinking 8 glasses of water
```

Expected: Parse title="drinking 8 glasses of water". Default to daily.
Create habit.

## CLI Verification Commands

Run from tests/ directory to verify habits were created:

```bash
todu template list --type habit --format json
```

```bash
todu template show <id> --format json
```

## Cleanup

Delete test habits after testing:

```bash
echo "y" | todu template delete <id>
```
