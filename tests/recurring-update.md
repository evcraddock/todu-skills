# Recurring Update Skill Test

Test the recurring-update skill with these prompts:

## Setup

Create a test recurring task:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template create --project mytest --title "Test task" \
  --recurrence "FREQ=WEEKLY;BYDAY=FR" --start-date 2025-11-28 --type task
```

## Test 1: Pause (deactivate) recurring task

```text
pause recurring task #<id>
```

Expected: Run `todu template deactivate <id>`. Show "deactivated" or "paused"
confirmation.

## Test 2: Resume (activate) recurring task

```text
resume recurring task #<id>
```

Expected: Run `todu template activate <id>`. Show "activated" or "resumed"
confirmation.

## Test 3: Change schedule to daily

```text
change recurring task #<id> to daily
```

Expected: Run `todu template update <id> --recurrence "FREQ=DAILY;INTERVAL=1"`.
Show updated schedule.

## Test 4: Change schedule to specific days

```text
change schedule of recurring task #<id> to Mon/Wed/Fri
```

Expected: Run `todu template update <id> --recurrence "FREQ=WEEKLY;BYDAY=MO,WE,FR"`.

## Test 5: Update title

```text
rename recurring task #<id> to "Morning standup"
```

Expected: Run `todu template update <id> --title "Morning standup"`.

## Test 6: Update priority

```text
set priority high on recurring task #<id>
```

Expected: Run `todu template update <id> --priority high`.

## Test 7: Multiple updates

```text
update recurring task #<id>: change to weekly and set priority low
```

Expected: Run `todu template update <id> --recurrence "FREQ=WEEKLY;INTERVAL=1"
--priority low`.

## Test 8: Generic update request

```text
update recurring task #<id>
```

Expected: Ask what to update (title, schedule, priority, pause/deactivate).

## Test 9: Deactivate with "stop"

```text
stop recurring task #<id>
```

Expected: Run `todu template deactivate <id>`.

## Test 10: Activate with "start"

```text
start recurring task #<id>
```

Expected: Run `todu template activate <id>`.

## Test 11: Error - template not found

```text
pause recurring task #99999
```

Expected: Display "Recurring task #99999 not found" or similar error.

## CLI Verification Commands

Run from tests/ directory:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template update <id> --title "New title"
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template deactivate <id>
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template activate <id>
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template show <id>
```

## Cleanup

Delete test template after testing:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
echo "y" | todu template delete <id>
```
