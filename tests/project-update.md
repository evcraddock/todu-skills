# Project Update Skill Test

Test the project-update skill with these prompts:

## Test 1: Update project description

```text
update the todu-tests project description to "Updated test description"
```

## Test 2: Rename a project

```text
rename the todu-tests project to my-test-project
```

## Test 3: Update project status

```text
mark the todu-tests project as done
```

## Test 4: Update multiple fields

```text
update the todu-tests project - change the name to updated-tests and
set status to done
```

## Test 5: Change sync strategy

```text
change the todu-tests sync strategy to pull only
```

## Test 6: Interactive field selection

```text
update the todu-tests project
```

Expected: Should prompt user to select which fields to update

## Test 7: Alternative phrasing

```text
modify the todu-tests project
```

## Test 8: Cancel a project

```text
cancel the todu-tests project
```

## Test 9: Fix project info

```text
fix the todu-tests project information
```

## Test 10: Error handling - non-existent project

```text
update the nonexistent-project description
```

Expected: Should list available projects and suggest correct name

## Test 11: Attempt to update system (should fail gracefully)

```text
change the todu-tests system to github
```

Expected: Should inform user that system cannot be changed and suggest
delete + re-add
