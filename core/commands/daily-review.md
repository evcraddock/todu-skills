---
description: Generate a daily review report with tasks and habits, saved to local file
---

# Daily Review

Generate a daily review report with 6 sections and save to a local file.

## Instructions

1. **Get configuration**
   - Run `todu config show`
   - Extract the local-reports path after "Local Reports:" (expand `~` to full path)
   - Extract the default project after "Project:" in Defaults section

2. **Get today's date**
   - Use format YYYY-MM-DD for queries
   - Calculate "soon" date (3 days from now) for Coming up Soon section

3. **Run queries with `--format json`**

   **In Progress:**
   ```bash
   todu task list --status inprogress --format json
   ```

   **Daily Goals** (habits scheduled for today):
   ```bash
   todu task list --scheduled-date <today> --format json
   ```
   - Filter for tasks that have a `template_id` (these are habit tasks)
   - Display as: `Habit Name : true` if status is "done", `Habit Name : false` otherwise

   **Coming up Soon** (due in next 3 days, excluding today):
   ```bash
   todu task list --status active --due-after <today> --due-before <soon> --format json
   ```

   **Next** (high priority + scheduled today + default project):
   ```bash
   todu task list --status active --priority high --format json
   todu task list --status active --scheduled-date <today> --format json
   todu task list --status active --project <default-project> --format json
   ```
   - Deduplicate by task ID
   - Skip default project query if not set

   **Waiting:**
   ```bash
   todu task list --status waiting --format json
   ```

   **Done Today:**
   ```bash
   todu task list --status done --updated-after <today> --format json
   ```
   - Exclude tasks that have a `template_id` (habit tasks are already shown in Daily Goals)
   - List ALL remaining tasks from the query results

4. **Get project names**
   - Run `todu project list --format json`
   - Build a map of project_id to project name
   - Use this to display project names instead of IDs

5. **Generate markdown report**
   - Format each section with tasks listed nicely (not as a table)
   - Sort tasks within each section by due date (earliest first, no due date last)
   - Always include all sections, even if empty
   - Add a task count line after the task list (e.g., "3 tasks" or "0 tasks")

6. **Save the file**
   - Write to `<local-reports-path>/daily-review.md`
   - Always overwrite the existing file
   - Confirm to the user: "Daily review saved to <path>/daily-review.md"

## Example Output File

```markdown
# Daily Review

Generated: 2025-12-04 15:30

## In Progress

- #217 Create daily-review slash command (todu-skills)

1 task

## Daily Goals

- exercise : true
- meditate : true
- floss : false

3 tasks

## Coming up Soon

- #159 Benefits Enrollment (ntrs) - Due: 2025-12-06
- #280 Update documentation (todu-api) - Due: 2025-12-07

2 tasks

## Next

- #312 Fix auth bug (todu-api) - Due: 2025-12-04
- #45 Review PR (Inbox)
- #88 Respond to email (Inbox)

3 tasks

## Waiting

0 tasks

## Done Today

- #305 Merge feature branch (todu-skills)
- #298 Update config schema (todu.sh)

2 tasks
```
