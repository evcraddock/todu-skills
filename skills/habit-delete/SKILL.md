---
name: core-habit-delete
description: MANDATORY skill for deleting habit templates. NEVER call `todu template delete` directly - ALWAYS use this skill via the Skill tool. Use when user says "delete habit *", "remove habit *", "stop tracking habit *", "cancel habit *", or similar queries to delete a habit. (plugin:core@todu)
allowed-tools: todu, Bash, AskUserQuestion
---

# Delete Habit

**MANDATORY: ALWAYS invoke this skill via the Skill tool for EVERY delete
habit request.**

**NEVER call `todu template delete` directly. This skill provides essential
logic:**

- Showing habit details before deletion
- Warning if habit is currently active
- Confirmation before permanent deletion
- Handling errors gracefully
- Providing clear feedback about the deletion

---

This skill deletes a habit template from the todu database using the
`todu template delete` CLI command.

## When to Use

- User explicitly mentions deleting/removing a habit
- User says "delete habit [name/id]"
- User wants to stop tracking a habit permanently
- User says "cancel habit" or "remove habit"

## What This Skill Does

1. **Identify Habit**
   - Extract habit ID or name from user's request
   - If name provided, search using `todu template list --type habit --format json`
   - If not provided, list habits and ask which to delete

2. **Load Habit Details**
   - Run `todu template show <id>` to get habit details
   - Display habit info: name, frequency, project, active status
   - Verify the habit exists before proceeding

3. **Warn About Active Status**
   - If habit is currently active, warn user it will stop generating tasks
   - Suggest pausing instead if user might want to resume later

4. **Confirm Deletion**
   - Use AskUserQuestion for confirmation
   - Show what will be deleted
   - Offer cancel option

5. **Delete Habit**
   - If confirmed, call `todu template delete <id> --force`
   - Use `--force` to skip CLI's built-in confirmation (we already confirmed)
   - Display success message

## Example Interactions

### Example 1: Delete by ID

**User**: "Delete habit 11"

**Skill**:

1. Runs `todu template show 11` to get details
2. Shows habit details:

   ```text
   Habit to delete:
   - ID: 11
   - Name: exercise
   - Frequency: Daily
   - Project: mytest
   - Status: active
   ```

3. Warns: "This habit is currently active. Deleting it will permanently stop
   task generation."
4. Asks confirmation:
   - Question: "Delete habit 'exercise'?"
   - Options:
     - "Yes, delete" - Permanently remove this habit
     - "Pause instead" - Deactivate but keep the habit
     - "Cancel" - Keep the habit
5. User selects: "Yes, delete"
6. Calls `todu template delete 11 --force`
7. Shows: "Habit 'exercise' (ID: 11) deleted successfully."

### Example 2: Delete by name

**User**: "Remove my meditation habit"

**Skill**:

1. Runs `todu template list --type habit --format json` to find "meditation"
2. Finds habit with id=12, title="meditation"
3. Shows habit details
4. Asks confirmation
5. User confirms
6. Calls `todu template delete 12 --force`
7. Shows: "Habit 'meditation' (ID: 12) deleted successfully."

### Example 3: Delete inactive habit

**User**: "Delete habit 13"

**Skill**:

1. Runs `todu template show 13` to get details
2. Shows habit details (status: inactive)
3. Note: No active warning needed since habit is already paused
4. Asks confirmation:
   - Question: "Delete habit 'read'?"
   - Options:
     - "Yes, delete" - Permanently remove this habit
     - "Cancel" - Keep the habit
5. User confirms
6. Calls `todu template delete 13 --force`
7. Shows: "Habit 'read' (ID: 13) deleted successfully."

### Example 4: Multiple habits match name

**User**: "Delete my exercise habit"

**Skill**:

1. Runs `todu template list --type habit --format json` to find "exercise"
2. Finds multiple matches: #11 "exercise", #15 "exercise routine"
3. Asks user to choose:
   - Question: "Which habit do you want to delete?"
   - Options:
     - "#11: exercise (daily)"
     - "#15: exercise routine (Mon/Wed/Fri)"
4. User selects one
5. Proceeds with confirmation and deletion

### Example 5: Habit not found

**User**: "Delete habit 99999"

**Skill**:

1. Runs `todu template show 99999`
2. Returns error: habit not found
3. Shows: "Habit #99999 not found. Use 'list habits' to see available habits."

### Example 6: Stop tracking phrasing

**User**: "Stop tracking my water habit"

**Skill**:

1. Interprets "stop tracking" as delete request
2. Searches for habit matching "water"
3. Shows details, asks confirmation
4. Proceeds with deletion if confirmed

### Example 7: User chooses to pause instead

**User**: "Delete habit 11"

**Skill**:

1. Shows habit details (active)
2. Asks confirmation with pause option
3. User selects: "Pause instead"
4. Calls `todu template deactivate 11`
5. Shows: "Habit 'exercise' (ID: 11) has been paused. You can resume it later
   with 'resume habit 11'."

## CLI Interface

**Search for habit by name:**

```bash
todu template list --type habit --format json
# Parse JSON to find matching habit by title
```

**Get habit details:**

```bash
todu template show <id>
```

**Delete habit:**

```bash
todu template delete <id> --force
```

**Flags:**

- `--force` or `-f`: Skip the CLI's built-in confirmation prompt (we handle
  confirmation ourselves)

**Success output:**

```text
Template deleted successfully
```

## Confirmation Flow

Use AskUserQuestion for confirmation. Options vary based on habit status:

### If habit is ACTIVE

Question: "Delete habit '{name}'? (currently active)"
Header: "Delete"
Options:

- **Yes, delete**: Permanently remove this habit and stop task generation
- **Pause instead**: Keep habit but deactivate it (can resume later)
- **Cancel**: Keep the habit as is

### If habit is INACTIVE

Question: "Delete habit '{name}'?"
Header: "Delete"
Options:

- **Yes, delete**: Permanently remove this habit
- **Cancel**: Keep the habit

Only proceed with deletion if user selects "Yes, delete".
If user selects "Pause instead", call `todu template deactivate <id>` instead.

## Search Patterns

Natural language queries the skill should understand:

- "delete habit [name/id]" → delete specific habit
- "remove habit [name/id]" → delete specific habit
- "stop tracking [name]" → delete specific habit
- "cancel habit [name/id]" → delete specific habit
- "get rid of [name] habit" → delete specific habit
- "delete my [name] habit" → delete specific habit

## Error Handling

- **Habit not found**: Show message and suggest listing habits
- **No habits registered**: Inform user no habits exist
- **Multiple matches**: Ask user to choose which habit
- **Delete failed**: Parse CLI error output and show message
- **CLI errors**: Check exit code and parse error output

## Future Considerations

When todu adds streak tracking for habits:

- Warn user about losing streak history
- Show current streak before deletion
- Consider offering to export streak data

## Notes

- Deletion is permanent - habit cannot be recovered
- Always show habit details before confirming deletion
- Offer "pause instead" option for active habits (user might want to resume)
- Use `--force` flag to skip CLI's built-in confirmation (we handle it)
- Search by name is case-insensitive
- If multiple habits match a name, ask user to choose
- Deleting a habit does NOT delete tasks already generated from it
