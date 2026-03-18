# Habit Check Skill Test

## Prerequisites

```bash
cd tests

todu habit create --project mytest --title "test-check-habit" \
  --schedule "FREQ=DAILY;INTERVAL=1" --start-date 2026-03-18 \
  --description $'## Check-in\n- What did you do?\n- How did it go?'
```

## Test

Prompt:

```text
mark habit 11 done
```

Expected:
- run `todu habit show 11 --format json`
- read the description
- ask the user for the response
- run `todu note add --habit 11 "<markdown response>" --format json`
- run `todu habit check 11`

Undo prompt:

```text
uncheck habit 11
```

Expected:
- run `todu habit uncheck 11`
