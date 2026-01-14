---
description: Generate a daily review report with tasks and habits
---

# Daily Review

Generate a daily review report. Optionally save to a local file.

## Instructions

1. **Check if user wants to save**
   - If the user includes "save" in their request, use the `--save` flag
   - Otherwise, just display the review

2. **Generate the daily review**

   Display only:

   ```bash
   todu review daily
   ```

   Save to file:

   ```bash
   todu review daily --save
   ```

3. **Confirm to the user**
   - If saved: confirm the file was saved
   - If displayed: no confirmation needed
