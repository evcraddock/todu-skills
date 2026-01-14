---
description: Generate a weekly review report with tasks organized by priority
---

# Weekly Review

Generate a weekly review report. Optionally save to a local file.

## Instructions

1. **Check if user wants to save**
   - If the user includes "save" in their request, use the `--save` flag
   - Otherwise, just display the review

2. **Generate the weekly review**

   Display only:

   ```bash
   todu review weekly
   ```

   Save to file:

   ```bash
   todu review weekly --save
   ```

3. **Confirm to the user**
   - If saved: confirm the file was saved
   - If displayed: no confirmation needed
