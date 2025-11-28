# Habit Delete Skill Test

Test the habit-delete skill with these prompts:

## Prerequisites

Create test habits before running delete tests:

```bash
cd tests
todu template create --project mytest --title "test-delete-habit" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit
todu template create --project mytest --title "test-delete-inactive" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit
# Deactivate the second one
todu template deactivate <second-id>
```

Note the returned habit IDs for use in tests below.

## Test 1: Delete by ID (active habit)

```text
delete habit 11
```

Expected: Show habit details, warn it's active, offer "Yes delete" / "Pause
instead" / "Cancel" options. If confirmed, run `todu template delete 11 --force`.

## Test 2: Delete by name

```text
remove my test-delete-habit
```

Expected: Search habits for "test-delete-habit", find matching habit, show
details, ask confirmation, delete if confirmed.

## Test 3: Delete inactive habit

```text
delete habit 13
```

Expected: Show habit details (inactive), no active warning needed, offer only
"Yes delete" / "Cancel" options (no pause option since already inactive).

## Test 4: Stop tracking phrasing

```text
stop tracking my exercise habit
```

Expected: Interpret as delete request, search for "exercise", show details,
confirm, delete.

## Test 5: Cancel habit phrasing

```text
cancel habit 11
```

Expected: Same as delete - show details, confirm, delete.

## Test 6: User chooses to pause instead

```text
delete habit 11
```

Expected: Show details, user selects "Pause instead", run
`todu template deactivate 11`, show "Habit paused. Resume with 'resume habit 11'".

## Test 7: User cancels deletion

```text
delete habit 11
```

Expected: Show details, user selects "Cancel", show "No changes made."

## Test 8: Habit not found

```text
delete habit 99999
```

Expected: Show "Habit #99999 not found. Use 'list habits' to see available
habits."

## Test 9: Delete by name - no match

```text
delete my nonexistent habit
```

Expected: Search habits, find no matches, show "No habit found matching
'nonexistent'. Here are your habits: ..."

## Test 10: Delete by name - multiple matches

Create two habits with similar names first:

```bash
todu template create --project mytest --title "morning exercise" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit
todu template create --project mytest --title "exercise routine" \
  --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR" --start-date 2025-11-28 --type habit
```

```text
delete my exercise habit
```

Expected: Find multiple matches, ask user "Which habit do you want to delete?"
with options for each matching habit.

## Test 11: Get rid of phrasing

```text
get rid of my reading habit
```

Expected: Interpret as delete, search for "reading", proceed with confirmation.

## Test 12: No ID or name provided

```text
delete a habit
```

Expected: List habits, ask "Which habit do you want to delete?"

## Test 13: Confirm details shown before delete

```text
delete habit 11
```

Expected: Show all details before confirmation:

- ID
- Name
- Frequency (human-readable)
- Project
- Active/Inactive status

## CLI Verification Commands

Run from tests/ directory to verify habits:

```bash
todu template list --type habit
```

```bash
todu template show <id>
```

## Cleanup

The tests themselves are about deletion, so cleanup happens as part of testing.
If tests fail partway through:

```bash
echo "y" | todu template delete <id>
```
