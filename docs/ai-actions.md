# ScatterPath AI Actions

## Overview

ScatterPath uses AI as a planning partner, not as a general chatbot.

AI should help the user:

- create plans
- adjust plans
- simplify tasks
- recover from missed time
- park distracting ideas
- clarify confusing work

AI output should be structured, validated, and converted into application state only through controlled flows.

## Core Rule

AI must not directly mutate saved plan state.

The normal flow is:

```txt id="cza3pn"
User request
  → AI action
  → structured proposal
  → backend validation
  → user applies or discards
  → database update
```

## MVP AI Actions

MVP supports these actions:

```txt id="5zjxe8"
generate_plan
adjust_plan
simplify_today
recover_plan
park_idea
clarify_task
```

## Action: generate_plan

Creates an initial structured plan from goal intake.

### Input

```txt id="xjlmci"
goal_title
goal_description
target_date
timeframe
available_minutes_per_day
available_days_per_week
current_situation
constraints
experience_level
```

### Output

The AI should return:

```txt id="mwh5hp"
goal_summary
plan_summary
milestones
week_plan
today_task
optional_parking_lot_items
```

### Notes

- This is usually the largest AI call.
- Output must be structured.
- Do not return a long markdown essay.
- The generated plan should be realistic for the user's stated time and constraints.
- MVP should avoid generating too many tasks at once.

### Suggested limits

```txt id="fq1ufd"
max_input_chars: 1200
max_output_tokens: 1800
max_milestones: 6
max_week_tasks: 7
```

## Action: adjust_plan

Updates part of the plan when the user says something changed.

Example user requests:

```txt id="crekgv"
I only have 20 minutes today.
This task is too hard.
Move interview prep earlier.
Make this week lighter.
I need to focus more on portfolio work.
```

### Input

```txt id="k8l9gw"
goal_summary
current_plan_summary
current_week
today_task
user_request
relevant_constraints
```

### Output

The AI should return an `AIProposal`.

Possible proposal changes:

```txt id="1ohxma"
update_today_task
update_week_tasks
move_task
reduce_scope
increase_scope
park_item
clarify_task
```

### Notes

- Prefer the smallest useful change.
- Do not regenerate the whole plan unless necessary.
- Explain what changed briefly.
- The user must apply or discard the proposal.

### Suggested limits

```txt id="s7y92s"
max_input_chars: 900
max_output_tokens: 900
```

## Action: simplify_today

Reduces the current task to something easier to start.

This powers the "I'm Overwhelmed" feature.

Example user requests:

```txt id="5c98cw"
I'm overwhelmed.
Make this smaller.
I can't handle this today.
Give me a 20-minute version.
```

### Input

```txt id="u7u48c"
goal_summary
today_task
available_minutes
user_energy_context
```

### Output

The AI should return a proposal containing:

```txt id="uwt034"
simplified_task
reasoning_summary
what_to_ignore
```

### Notes

- This action should be aggressive about reducing scope.
- The result should be concrete and immediately doable.
- Do not shame the user.
- Do not create a motivational speech.
- The goal is momentum.

### Suggested limits

```txt id="5zyj1d"
max_input_chars: 600
max_output_tokens: 500
```

## Action: recover_plan

Helps the user resume after missing time.

Example user requests:

```txt id="m0jstl"
I missed three days.
I haven't opened this in two weeks.
This week got wrecked.
I'm behind.
```

### Input

```txt id="aq927y"
goal_summary
plan_summary
current_week
missed_tasks
target_date
updated_availability
user_request
```

### Output

The AI should return a proposal containing:

```txt id="4tiarc"
recovery_summary
updated_today_task
updated_week_tasks
tasks_to_drop_or_move
```

### Notes

- No guilt.
- No punishment.
- Assume life happened.
- Preserve momentum over perfect catch-up.
- Do not simply pile missed tasks onto the user.

### Suggested limits

```txt id="lmxezh"
max_input_chars: 1000
max_output_tokens: 1000
```

## Action: park_idea

Moves distracting or future ideas into the Parking Lot.

Example user requests:

```txt id="gqad9q"
I also want to learn Rust.
Maybe I should build a game.
I have an idea for a YouTube channel.
Save this for later.
```

### Input

```txt id="am9g0n"
goal_summary
current_week_focus
idea
```

### Output

The AI should return a proposal containing:

```txt id="o62c7h"
parking_lot_item
reason_parked
```

### Notes

- Parking an idea is not rejection.
- The purpose is to protect the active goal.
- The response should be short and reassuring.

### Suggested limits

```txt id="h7v1en"
max_input_chars: 400
max_output_tokens: 300
```

## Action: clarify_task

Explains a task or makes it more actionable without changing the plan.

Example user requests:

```txt id="v2k4uo"
What does this mean?
How do I start this?
Break this down a little.
What is done supposed to look like?
```

### Input

```txt id="xkefbz"
goal_summary
today_task
user_question
```

### Output

The AI should return:

```txt id="pq2buz"
clarification
suggested_first_step
done_definition
```

### Notes

- This may not need a proposal if it does not change saved state.
- Keep the explanation practical.
- Avoid long tutorials unless requested.
- Help the user start.

### Suggested limits

```txt id="o2qrl8"
max_input_chars: 600
max_output_tokens: 500
```

## Proposal Shape

Most AI actions should return a proposal with this general structure:

```txt id="u48vt6"
type
summary
changes
payload
```

Where:

```txt id="hmfw9h"
type: proposal type
summary: short human-readable explanation
changes: before/after change descriptions
payload: structured data needed to apply the proposal
```

Example proposal types:

```txt id="vj4xml"
generate_plan
adjust_plan
simplify_today
recover_plan
park_idea
clarify_task
```

## Proposal Statuses

AI proposals can have these statuses:

```txt id="2fzx3k"
pending
applied
discarded
expired
```

## Validation Rules

Before a proposal can be applied:

- proposal must belong to the current user
- proposal must match the active goal/plan
- proposal status must be pending
- payload must match the expected schema for the proposal type
- proposal must not exceed MVP scope
- proposal must not create unrelated features or structures

## Cost and Token Rules

All AI calls should have action-level budgets.

Do not send the full user history unless required.

Prefer narrow context:

- current goal summary
- current week
- today task
- relevant constraints
- user request

Avoid sending:

- all past plans
- all previous AI outputs
- entire chat logs
- unrelated parking lot items
- large raw markdown blobs

## AI Response Tone

Default AI communication should be:

- calm
- practical
- direct
- supportive
- non-judgmental

The AI should avoid:

- guilt
- shame
- fake enthusiasm
- long motivational speeches
- vague advice
- excessive explanation

## MVP Implementation Order

Implement AI behavior in this order:

1. Mock provider
2. Structured generate_plan response
3. Mock adjust proposal
4. Apply/discard proposal flow
5. Usage logging
6. Usage limits
7. OpenAI provider
8. Real structured response validation

Do not start with OpenAI.

The mock provider should prove the application flow first.
