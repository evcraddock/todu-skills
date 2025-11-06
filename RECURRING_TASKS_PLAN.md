# Implementation Plan: Recurring Task Completion History

**Issue:** #30
**Started:** 2025-11-04
**Status:** In Progress

## Overview

Implement a system-agnostic solution for tracking completion history of
recurring tasks across all systems (GitHub, Forgejo, Todoist).

## Core Concept

When a recurring task is completed:

1. Create a NEW completion record with a new todu ID (status: `done`)
2. Update the ORIGINAL task with next occurrence info (keeps original
   todu ID)
3. Both records share the same `systemData` identifier to link them

## Stage 1: Schema and Core Utilities

**Goal**: Add recurring object support to the issue.json schema and create
core utility functions.

**Success Criteria**:

- JSON schema supports optional `recurring` object
- Utility module created for recurring task operations
- Functions to detect, create, and query recurring tasks

**Tests**:

- Test recurring object validation
- Test completion record creation
- Test linking via systemData

**Status**: Not Started

**Implementation**:

1. Document the extended schema in a schema file or docs
2. Create `core/scripts/recurring.py` with:
   - `is_recurring(task_data)` - Check if task has recurring object
   - `create_completion_record(task_data)` - Create completion record with new ID
   - `update_recurring_task(task_data, next_due)` - Update original task for
     next occurrence
   - `get_completion_history(system, systemData)` - Query all completions

## Stage 2: Todoist Integration

**Goal**: Add recurring task support to Todoist sync script.

**Success Criteria**:

- Todoist recurring tasks detected during sync
- Completion records created when recurring tasks are completed
- Original task updated with next due date
- Completions tracked in `recurring.completions` array

**Tests**:

- Sync a Todoist recurring task
- Complete the task in Todoist
- Sync again - verify completion record exists
- Verify original task has updated due date

**Status**: Not Started

**Implementation**:

1. Update `todoist/scripts/sync-tasks.py`:
   - Detect `task.due.is_recurring` from Todoist API
   - Add `recurring` object when normalizing tasks
   - Handle completion of recurring tasks
   - Create completion records and update original

## Stage 3: GitHub/Forgejo Integration

**Goal**: Add recurring task support to GitHub and Forgejo sync scripts.

**Success Criteria**:

- Issues with `recurring:*` labels detected as recurring
- Manual completion workflow supported
- Completion records created appropriately

**Tests**:

- Create GitHub issue with `recurring:weekly` label
- Mark as complete
- Verify completion record created

**Status**: Not Started

**Implementation**:

1. Update `github/scripts/sync-issues.py`:
   - Detect `recurring:*` labels
   - Parse pattern from label (e.g., `recurring:weekly`)
   - Add `recurring` object during normalization
   - Handle completion workflow

2. Update `forgejo/scripts/sync-issues.py`:
   - Same as GitHub implementation

## Stage 4: Completion Record Management

**Goal**: Create tools to view and query completion history.

**Success Criteria**:

- Can query all completions for a recurring task
- Can filter completions by date range
- Task view shows completion history

**Tests**:

- View task with completion history
- Query completions for specific task
- Filter by date range

**Status**: Not Started

**Implementation**:

1. Update `core/scripts/resolve_task.py`:
   - Support querying by systemData to find all related records
2. Update view scripts to show completion history
3. Add completion history section to task view output

## Stage 5: Reporting Integration

**Goal**: Update reports to include recurring task completion history.

**Success Criteria**:

- Daily/weekly reports show completed recurring tasks
- Completion trends visible
- Reports distinguish between one-time and recurring completions

**Tests**:

- Generate daily report with recurring task completions
- Generate weekly report showing recurring patterns
- Verify completion counts accurate

**Status**: Not Started

**Implementation**:

1. Update `core/scripts/report.py`:
   - Group completions by systemData
   - Show completion streaks/patterns
   - Distinguish recurring vs one-time tasks

## Stage 6: Documentation and Testing

**Goal**: Comprehensive tests and documentation.

**Success Criteria**:

- All stages have passing tests
- User documentation updated
- Edge cases handled

**Tests**:

- End-to-end test: Create, complete, sync recurring task
- Test multiple completions of same task
- Test completion history queries
- Test all three systems (Todoist, GitHub, Forgejo)

**Status**: Not Started

**Implementation**:

1. Create test suite in `tests/` directory
2. Update README with recurring task documentation
3. Add troubleshooting guide

## Design Decisions

### Why Separate Completion Records?

- **Preserves history**: Each completion is a distinct event
- **Unique IDs**: Each completion can be referenced independently
- **System-agnostic**: Works for all task systems
- **Queryable**: Easy to find all completions for a task

### Schema Design

The `recurring` object is optional and only present on recurring tasks:

```json
{
  "recurring": {
    "pattern": "weekly",
    "interval": 1,
    "nextDue": "2025-11-15",
    "completions": [
      {
        "completedAt": "2025-11-08T14:30:00Z",
        "completionId": 123
      }
    ]
  }
}
```

### Completion Record Format

Completion records are full task objects with:

- New todu `id`
- Same `systemData` (links to original)
- Status: `done`
- `completedAt`: timestamp
- Snapshot of task at completion time

## Migration

- **Backward compatible**: Existing tasks work without changes
- **No data migration needed**: New field only on new recurring tasks
- **Gradual rollout**: Can be added per-system incrementally

## Notes

- Start with Todoist (has native recurring support)
- GitHub/Forgejo require label-based detection
- Completion records stored in same `issues/` directory
- Query by `systemData` to find all related records
