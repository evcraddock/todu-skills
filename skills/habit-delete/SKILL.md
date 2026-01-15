---
name: habit-delete
description: Delete habit templates. Use when user says "delete habit *", "remove habit *", "stop tracking *", or similar. (plugin:todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Delete Habit

This skill provides:
- Confirmation before permanent deletion
- Warning if habit is active
- Option to pause instead of delete

## Example Interactions

### Example 1: Delete by ID

**User**: "Delete habit 11"

**Skill**:

1. Runs `todu template show 11` to get details
2. Shows: "Habit: exercise (daily, active)"
3. Asks confirmation with options: "Yes, delete" / "Pause instead" / "Cancel"
4. User selects: "Yes, delete"
5. Calls `todu template delete 11 --force`
6. Shows: "Habit 'exercise' deleted."

### Example 2: Delete by name

**User**: "Remove my meditation habit"

**Skill**:

1. Runs `todu template list --type habit --format json` to find "meditation"
2. Finds habit id=12, shows details
3. Asks confirmation, user confirms
4. Calls `todu template delete 12 --force`

### Example 3: Multiple habits match

**User**: "Delete my exercise habit"

**Skill**:

1. Searches and finds multiple matches: #11 "exercise", #15 "exercise routine"
2. Asks user to choose which habit
3. Proceeds with confirmation and deletion

### Example 4: User chooses to pause

**User**: "Delete habit 11"

**Skill**:

1. Shows habit details (active)
2. User selects: "Pause instead"
3. Calls `todu template deactivate 11`
4. Shows: "Habit paused. Resume with 'resume habit 11'."

## CLI Interface

```bash
# Search by name
todu template list --type habit --format json

# Get details
todu template show <id>

# Delete (--force skips CLI confirmation since we handle it)
todu template delete <id> --force

# Pause instead
todu template deactivate <id>
```

## Confirmation Options

**Active habit**: "Yes, delete" / "Pause instead" / "Cancel"
**Inactive habit**: "Yes, delete" / "Cancel"

Only delete if user selects "Yes, delete".

## Error Handling

- **Habit not found**: Suggest listing habits
- **Multiple matches**: Ask user to choose

## Notes

- Deletion is permanent
- Offer "pause instead" for active habits
- Deleting a habit does NOT delete tasks already generated from it
