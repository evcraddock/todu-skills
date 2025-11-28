# Habit List Skill Test

Test the habit-list skill with these prompts:

## Setup

Create test habits:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template create --project mytest --title "exercise" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit && \
todu template create --project mytest --title "meditate" \
  --recurrence "FREQ=DAILY;INTERVAL=1" --start-date 2025-11-28 --type habit
```

## Test 1: List all habits

```text
show me my habits
```

Expected: Run `todu template list --type habit` and display all habits.

## Test 2: Filter by project

```text
list habits in mytest
```

Expected: Run `todu template list --type habit --project mytest`.

## Test 3: Show active only

```text
show active habits
```

Expected: Run `todu template list --type habit --active true`.

## Test 4: Show paused habits

```text
show paused habits
```

Expected: Run `todu template list --type habit --active false`.

## Test 5: Show specific habit

```text
show details of habit #<id>
```

Expected: Run `todu template show <id>` and display full details.

## Test 6: What habits am I tracking

```text
what habits am I tracking?
```

Expected: Run `todu template list --type habit` and display all.

## Test 7: No results

```text
list habits in nonexistent-project
```

Expected: Display "No habits found" or project not found error.

## CLI Verification Commands

Run from tests/ directory:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type habit
```

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template show <id>
```

## Cleanup

Delete test habits after testing:

```bash
cd /Users/erik/code/github/evcraddock/todu-skills/tests && \
todu template list --type habit --format json | \
jq -r '.[].id' | xargs -I {} sh -c 'echo "y" | todu template delete {}'
```
