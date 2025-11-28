# Recurring Delete Skill Test

Test the recurring-delete skill with these prompts:

## Setup

Create test recurring tasks:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template create --project mytest --title "Test delete 1" \
  --recurrence "FREQ=WEEKLY;BYDAY=FR" --start-date 2025-11-28 --type task && \
todu template create --project mytest --title "Test delete 2" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type task
```

## Test 1: Delete by ID with confirmation

```text
delete recurring task #<id>
```

Expected: Show template details (title, schedule, project, status). Ask for
confirmation. On confirm, run `todu template delete <id> --force`. Show success.

## Test 2: Delete inactive template

First deactivate, then delete:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template deactivate <id>
```

```text
delete recurring task #<id>
```

Expected: Show template details with "inactive (paused)" status. Confirm and
delete.

## Test 3: Cancel deletion

```text
delete recurring task #<id>
```

Expected: Show details, ask for confirmation. User selects "Cancel". Show
"Deletion cancelled. No changes made."

## Test 4: Template not found

```text
delete recurring task #99999
```

Expected: Show "Recurring task #99999 not found" or similar error.

## Test 5: No ID provided

```text
delete a recurring task
```

Expected: List available recurring tasks and ask which one to delete.

## Test 6: Delete with "remove" phrasing

```text
remove recurring task #<id>
```

Expected: Same as Test 1 - show details, confirm, delete.

## Test 7: Delete with "cancel" phrasing

```text
cancel recurring task #<id>
```

Expected: Same as Test 1 - permanently delete (not deactivate).

## CLI Verification Commands

Run from tests/ directory:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type task
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template show <id>
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
echo "y" | todu template delete <id>
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template delete <id> --force
```

## Cleanup

Any remaining test templates:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type task --format json | \
jq -r '.[].id' | xargs -I {} sh -c 'echo "y" | todu template delete {}'
```
