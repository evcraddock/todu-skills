# Recurring List Skill Test

Test the recurring-list skill with these prompts:

## Setup

First, create some test recurring tasks:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template create --project mytest --title "Weekly review" \
  --recurrence "FREQ=WEEKLY;BYDAY=FR" --start-date 2025-11-28 --type task && \
todu template create --project mytest --title "Daily standup" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type task
```

## Test 1: List all recurring tasks

```text
show me my recurring tasks
```

Expected: Run `todu template list --type task` and display all recurring task
templates with ID, title, recurrence, project, status, and next occurrence.

## Test 2: Filter by project

```text
list recurring tasks in mytest
```

Expected: Run `todu template list --type task --project mytest` and display
only recurring tasks in the mytest project.

## Test 3: Show active only

```text
show active recurring tasks
```

Expected: Run `todu template list --type task --active true` and display only
active templates.

## Test 4: Show inactive/paused

```text
show paused recurring tasks
```

Expected: Run `todu template list --type task --active false` and display only
inactive templates.

## Test 5: Show specific template details

```text
show details of recurring task #<id>
```

Expected: Run `todu template show <id>` and display full details including
recurrence pattern, next 5 occurrences, timezone, and dates.

## Test 6: What recurring tasks do I have

```text
what recurring tasks do I have
```

Expected: Run `todu template list --type task` and display all recurring tasks.

## Test 7: No results

```text
list recurring tasks in nonexistent-project
```

Expected: Display "No recurring tasks found" or project not found error.

## Test 8: Combined filters

```text
show active recurring tasks in mytest
```

Expected: Run `todu template list --type task --project mytest --active true`

## CLI Verification Commands

Run from tests/ directory:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type task
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type task --project mytest
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template show <id>
```

## Cleanup

Delete test templates after testing:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type task --format json | \
jq -r '.[].id' | xargs -I {} sh -c 'echo "y" | todu template delete {}'
```
