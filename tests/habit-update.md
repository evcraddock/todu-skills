# Habit Update Skill Test

Test the habit-update skill with these prompts:

## Prerequisites

Create a test habit before running update tests:

```bash
cd tests
todu template create --project mytest --title "exercise" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit
```

Note the returned habit ID for use in tests below.

## Test 1: Pause a habit by ID

```text
pause habit 11
```

Expected: Verify habit exists, show "Pausing habit #11: exercise", run
`todu template deactivate 11`, confirm habit is paused.

## Test 2: Resume a habit by ID

```text
resume habit 11
```

Expected: Verify habit exists, show "Resuming habit #11: exercise", run
`todu template activate 11`, confirm habit is active.

## Test 3: Pause by name

```text
pause my exercise habit
```

Expected: Search habits for "exercise", find matching habit, confirm which one,
run `todu template deactivate <id>`, confirm paused.

## Test 4: Change schedule to specific days

```text
change habit 11 to Mon/Wed/Fri
```

Expected: Verify habit exists, convert to `FREQ=WEEKLY;BYDAY=MO,WE,FR`, run
`todu template update 11 --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"`, show
updated schedule.

## Test 5: Change to daily

```text
update habit 11 to daily
```

Expected: Verify habit exists, convert to `FREQ=DAILY;INTERVAL=1`, run
`todu template update 11 --recurrence "FREQ=DAILY;INTERVAL=1"`, confirm daily.

## Test 6: Change to weekly

```text
make habit 11 weekly
```

Expected: Verify habit exists, convert to `FREQ=WEEKLY;INTERVAL=1`, run
`todu template update 11 --recurrence "FREQ=WEEKLY;INTERVAL=1"`, confirm weekly.

## Test 7: Rename habit

```text
rename habit 11 to 'Morning workout'
```

Expected: Verify habit exists, run
`todu template update 11 --title "Morning workout"`, confirm new title.

## Test 8: Set priority

```text
set habit 11 to high priority
```

Expected: Verify habit exists, run `todu template update 11 --priority high`,
confirm priority.

## Test 9: Multiple updates

```text
rename habit 11 to 'Morning workout' and set high priority
```

Expected: Verify habit exists, run
`todu template update 11 --title "Morning workout" --priority high`, confirm
both changes.

## Test 10: Deactivate synonym

```text
deactivate habit 11
```

Expected: Same as pause - run `todu template deactivate 11`.

## Test 11: Activate synonym

```text
activate habit 11
```

Expected: Same as resume - run `todu template activate 11`.

## Test 12: Stop/start synonyms

```text
stop habit 11
```

Expected: Same as pause - run `todu template deactivate 11`.

```text
start habit 11 again
```

Expected: Same as resume - run `todu template activate 11`.

## Test 13: Change to weekdays

```text
change habit 11 to weekdays only
```

Expected: Convert to `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR`, update habit.

## Test 14: Set end date

```text
set end date on habit 11 to 2025-12-31
```

Expected: Run `todu template update 11 --end-date 2025-12-31`, confirm end date.

## Test 15: Update description

```text
update description of habit 11 to 'Morning exercise routine'
```

Expected: Run `todu template update 11 --description "Morning exercise routine"`,
confirm.

## Test 16: Add labels

```text
add label health to habit 11
```

Expected: Run `todu template update 11 --label health`, note that this replaces
all labels.

## Test 17: Assign to user

```text
assign habit 11 to alice
```

Expected: Run `todu template update 11 --assignee alice`, confirm.

## Test 18: Error - habit not found

```text
pause habit 99999
```

Expected: Show "Habit #99999 not found. Please check the habit ID."

## Test 19: Error - no matching habit name

```text
pause my nonexistent habit
```

Expected: Search habits, find no matches, show available habits.

## Test 20: Invalid priority

```text
set habit 11 to critical priority
```

Expected: Show "Invalid priority. Use: low, medium, or high"

## CLI Verification Commands

Run from tests/ directory to verify updates:

```bash
todu template show <id>
```

```bash
todu template list --type habit
```

## Cleanup

Delete test habits after testing:

```bash
echo "y" | todu template delete <id>
```
