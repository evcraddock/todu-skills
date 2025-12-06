---
description: Generate a weekly review report with tasks organized by priority, saved to local file
---

# Weekly Review

Generate a weekly review report with 4 sections and save to a local file.

## Instructions

1. **Get configuration**
   - Run `todu config show`
   - Extract the local-reports path after "Local Reports:" (expand `~` to full path)

2. **Get today's date**
   - Use format YYYY-MM-DD for queries

3. **Run queries with `--format json`**

   **Waiting:**

   ```bash
   todu task list --status waiting --format json
   ```

   **Next** (high priority OR due today):

   ```bash
   todu task list --status active --priority high --format json
   todu task list --status active --due-before <today> --format json
   ```

   - Deduplicate by task ID (a task may appear in both queries)

   **Active** (medium priority OR no priority):

   ```bash
   todu task list --status active --priority medium --format json
   ```

   - Filter second query for tasks with no priority set
   - Deduplicate by task ID

   **Someday** (low priority):

   ```bash
   todu task list --status active --priority low --format json
   ```

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
   - Write to `<local-reports-path>/weekly-review.md`
   - Always overwrite the existing file
   - Confirm to the user: "Weekly review saved to `<path>`/weekly-review.md"

## Example Output File

```markdown
# Weekly Review

Generated: 2025-12-05 15:30

## Waiting

- #42 Waiting on client feedback (project-name)
- #98 Blocked by external API (todu-api)

2 tasks

## Next

- #218 Convert weekly-review skill (todu-skills) - Due: 2025-12-05
- #45 Review PR (Inbox)
- #312 Fix auth bug (todu-api)

3 tasks

## Active

- #100 Update documentation (todu-api)
- #156 Refactor login flow (todu-skills)

2 tasks

## Someday

0 tasks
```
