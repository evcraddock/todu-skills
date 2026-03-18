---
name: habit-check
description: Check in a habit for today or undo today's check-in. Use when user says "check off habit *", "mark habit * done", "I did habit *", "complete habit *", "undo habit check *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Habit Check

Use this flow:

1. Find the habit (`todu habit show <id>` or `todu habit list --format json`)
2. Read the description
3. If the description contains instructions or prompts, ask the user for the response
4. Save the response as a note with `todu note add --habit <id> "..." --format json`
5. Check in the habit with `todu habit check <id>`

For undo requests, run `todu habit uncheck <id>`.

## Examples

- "mark habit 11 done" → show habit, follow description instructions, add note, check habit
- "I did my meditation habit" → find habit, follow description instructions, add note, check habit
- "uncheck habit 11" → `todu habit uncheck 11`

## Commands

```bash
todu habit show <id> --format json
todu habit list --format json
todu note add --habit <id> "Note markdown" --format json
todu habit check <id>
todu habit uncheck <id>
```

## Notes

- Prefer a short markdown note that captures the user's response
- If the description has no actionable instructions, check the habit directly unless the user provides a reflection
- Ask the user to choose if multiple habits match
