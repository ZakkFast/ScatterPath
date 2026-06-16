# ScatterPath Data Model

## Overview

The MVP data model supports one active goal per user and a structured plan made of milestones, weeks, tasks, parking lot items, and AI proposals.

The core domain shape is:

```txt
UserProfile
  → Goal
    → Plan
      → Milestone
      → WeekPlan
        → Task
    → ParkingLotItem
    → AIProposal
```

AI usage is tracked separately through `AIUsageLog`.

## Design Principles

- Keep the MVP schema simple.
- Support one active goal per user.
- Avoid task dependencies for MVP.
- Avoid nested subtasks for MVP.
- Avoid tags, labels, and custom workflows for MVP.
- Prefer explicit status fields over complex state machines.
- AI proposals should store proposed changes before they are applied.
- AI should not directly mutate plan state.

## Common Field Conventions

Most persisted records should include:

```txt
id
created_at
updated_at
```

Use UUID primary keys.

Use timezone-aware timestamps.

Use enums for constrained statuses where practical.

## UserProfile

Represents the local application profile for an authenticated user.

Auth itself should be handled by a managed provider such as Supabase Auth or Clerk.

Fields:

```txt
id
auth_provider_user_id
email
display_name
created_at
updated_at
```

Notes:

- `auth_provider_user_id` should map to the external auth provider.
- Early backend work may use a temporary placeholder user before auth is wired.

## Goal

Represents the user’s active objective.

MVP supports one active goal per user.

Fields:

```txt
id
user_id
title
description
target_date
timeframe
available_minutes_per_day
available_days_per_week
current_situation
constraints
status
created_at
updated_at
```

Suggested statuses:

```txt
active
completed
paused
archived
```

Notes:

- `target_date` may be nullable if the user gives a loose timeframe instead.
- `timeframe` can store human-readable input such as "60 days" or "8 weeks".
- `constraints` can be text for MVP.
- Do not add multiple active goals for MVP.

## Plan

Represents the AI-generated structure for achieving a goal.

Fields:

```txt
id
goal_id
summary
status
created_at
updated_at
```

Suggested statuses:

```txt
active
replaced
archived
```

Notes:

- A goal should have one active plan.
- Future versions may support plan revisions, but MVP can rely on proposals and usage logs first.

## Milestone

Represents a major phase or checkpoint in a plan.

Fields:

```txt
id
plan_id
title
description
sort_order
status
created_at
updated_at
```

Suggested statuses:

```txt
pending
active
completed
skipped
```

Notes:

- Milestones should stay high-level.
- Do not model complex dependencies for MVP.
- Task ordering and week grouping are enough for the first version.

## WeekPlan

Represents the current week or a planned week in the roadmap.

Fields:

```txt
id
plan_id
week_number
title
focus
starts_on
ends_on
status
created_at
updated_at
```

Suggested statuses:

```txt
pending
active
completed
skipped
```

Notes:

- `focus` is the plain-English purpose of the week.
- MVP can generate only the current detailed week plus high-level future milestones if needed.

## Task

Represents actionable work.

Tasks belong to a week plan and may optionally connect to a milestone.

Fields:

```txt
id
week_plan_id
milestone_id
title
description
estimated_minutes
why_it_matters
success_criteria
status
sort_order
created_at
updated_at
completed_at
skipped_at
```

Suggested statuses:

```txt
pending
active
completed
skipped
parked
```

Notes:

- `milestone_id` may be nullable.
- `success_criteria` should be stored as JSON.
- Only one task should normally be active as today's primary task.
- Avoid nested subtasks for MVP.
- Avoid dependencies for MVP.

## ParkingLotItem

Represents an idea or task intentionally saved for later.

Fields:

```txt
id
goal_id
user_id
title
description
reason_parked
source
status
created_at
updated_at
```

Suggested sources:

```txt
manual
ai_suggested
```

Suggested statuses:

```txt
active
converted
dismissed
archived
```

Notes:

- Parking lot items protect focus.
- They should not automatically become tasks.
- Converting a parking lot item into a goal or task can be manual for MVP.

## AIProposal

Represents a proposed AI-generated change that has not necessarily been applied.

Fields:

```txt
id
user_id
goal_id
plan_id
type
summary
payload
status
created_at
updated_at
applied_at
discarded_at
```

Suggested types:

```txt
generate_plan
adjust_plan
simplify_today
recover_plan
park_idea
clarify_task
```

Suggested statuses:

```txt
pending
applied
discarded
expired
```

Notes:

- `payload` should be JSON.
- The payload shape depends on proposal type.
- Proposals should be validated before they can be applied.
- AI should create proposals, not directly mutate saved plan state.

## AIUsageLog

Tracks AI usage for cost control, debugging, and abuse prevention.

Fields:

```txt
id
user_id
action_type
provider
used_hosted_key
input_tokens
output_tokens
estimated_cost
created_at
```

Suggested action types:

```txt
generate_plan
adjust_plan
simplify_today
recover_plan
park_idea
clarify_task
```

Notes:

- Do not store full prompts or responses by default.
- Store metadata needed for usage limits and debugging.
- If full prompt logging is ever added, it should be intentional and privacy-conscious.

## Suggested Relationships

```txt
UserProfile 1 → many Goal
UserProfile 1 → many ParkingLotItem
UserProfile 1 → many AIProposal
UserProfile 1 → many AIUsageLog

Goal 1 → many Plan
Goal 1 → many ParkingLotItem
Goal 1 → many AIProposal

Plan 1 → many Milestone
Plan 1 → many WeekPlan
Plan 1 → many AIProposal

WeekPlan 1 → many Task

Milestone 1 → many Task
```

## MVP Constraints

For MVP:

- one active goal per user
- one active plan per active goal
- one active week plan at a time
- one primary active task for Today
- AI changes go through proposals
- OpenAI integration comes after mock AI works

## Deferred Data Model Features

Do not add these yet:

- task dependencies
- nested subtasks
- labels
- tags
- recurring tasks
- recurring goals
- multiple workspaces
- team ownership
- plan version history
- notification schedules
- calendar event mappings
- persistent stored API keys
