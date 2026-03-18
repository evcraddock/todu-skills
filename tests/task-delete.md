# Task Delete Skill Test

## Prerequisites

```bash
cd tests

todu task create --project mytest --title "delete-me-task"
```

## Test

Prompt:

```text
delete task 42
```

Expected:
- run `todu task show 42 --format json`
- ask for confirmation
- run `todu task delete 42`

Search prompt:

```text
remove the delete me task
```

Expected:
- run `todu task search "delete me task" --format json`
- ask for confirmation
- run `todu task delete <id>`
