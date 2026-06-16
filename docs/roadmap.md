# ScatterPath Build Roadmap

## Purpose

This roadmap defines the intended build order for the MVP.

The goal is to build the domain spine first, then layer on AI, auth, limits, and UI.

Do not treat this as a rigid long-term product roadmap.

## Guiding Rule

Build the smallest working slice of the core loop before adding polish.

Core loop:

```txt
Create goal
→ generate mock plan
→ fetch today's task
→ complete or skip task
→ create AI proposal
→ apply or discard proposal
```

## Phase 1: Project Foundation

Goal:

Create a working backend skeleton.

Includes:

- FastAPI app structure
- health check endpoint
- basic config
- local run command
- initial test setup if practical

Done when:

- backend starts locally
- `GET /health` returns a successful response

Do not add:

- database models
- auth
- OpenAI
- frontend integration

## Phase 2: Core Domain Models

Goal:

Define the first database schema.

Includes:

- UserProfile
- Goal
- Plan
- Milestone
- WeekPlan
- Task
- ParkingLotItem
- AIProposal
- AIUsageLog

Done when:

- models are defined
- relationships are reasonable
- migrations can be created/applied
- schema matches `docs/data-model.md`

Do not add:

- complex task dependencies
- tags
- multiple active goals
- plan revision history

## Phase 3: Goal Creation

Goal:

Allow a user to create and fetch an active goal.

Includes:

- create goal endpoint
- get active goal endpoint
- placeholder user support if auth is not ready
- service-layer goal logic

Done when:

- a goal can be created
- active goal can be fetched
- MVP rule of one active goal per user is respected

Do not add:

- auth complexity
- multiple active goals
- goal templates

## Phase 4: Mock Plan Generation

Goal:

Generate a usable fake plan without calling OpenAI.

Includes:

- mock AI provider
- plan service
- plan creation from goal
- milestones
- one week plan
- tasks
- today’s active task

Done when:

- a goal can produce a mock plan
- plan data is persisted
- today task can be identified

Do not add:

- OpenAI integration
- prompt engineering
- real AI cost tracking

## Phase 5: Today Task Flow

Goal:

Support the main execution loop.

Includes:

- get today task endpoint
- complete today task endpoint
- skip today task endpoint
- task status updates
- basic next-task selection

Done when:

- today task can be fetched
- task can be completed
- task can be skipped
- app can select or expose the next task

Do not add:

- timers
- streaks
- scoring
- habit tracking

## Phase 6: AI Proposal Flow

Goal:

Support AI-style changes without direct mutation.

Includes:

- AIProposal model usage
- mock adjust proposal
- apply proposal endpoint
- discard proposal endpoint
- proposal validation
- payload handling

Done when:

- a mock proposal can be created
- pending proposal can be applied
- pending proposal can be discarded
- applied proposal mutates state only after approval

Do not add:

- full chat
- chat history
- streaming responses

## Phase 7: Parking Lot

Goal:

Support saving future ideas without disrupting the active plan.

Includes:

- create parking lot item
- list parking lot items
- support manual source
- support AI-suggested source later

Done when:

- user can add an idea
- user can view parked ideas
- parking lot items stay connected to the active goal/user

Do not add:

- categories
- reminders
- prioritization
- scheduling

## Phase 8: Usage Logging and Limits

Goal:

Protect hosted AI usage and user-provided API key usage.

Includes:

- AIUsageLog
- action-level budgets
- free trial counters
- basic cooldown/rate limit strategy
- global hosted AI cap strategy

Done when:

- AI calls can be logged
- hosted free usage can be counted
- action budgets are represented in code

Do not add:

- billing
- paid plans
- admin dashboard
- complex analytics

## Phase 9: Auth

Goal:

Connect user data to real authenticated users.

Preferred direction:

- Supabase Auth or Clerk
- managed auth
- local UserProfile mapping

Done when:

- authenticated user can own goals/plans/tasks
- placeholder user logic is replaced or isolated
- user cannot access another user’s data

Do not add:

- teams
- organizations
- roles
- invites

## Phase 10: OpenAI Provider

Goal:

Replace mock AI behavior with real structured AI calls.

Includes:

- OpenAI provider
- structured response schemas
- response validation
- action-level context builders
- usage logging
- free trial hosted key path
- BYOK session key path

Done when:

- generate_plan works with OpenAI
- adjust/simplify/recover actions can produce validated proposals
- usage is logged
- limits are enforced

Do not add:

- multiple providers
- full chat
- persistent API key storage

## Phase 11: Frontend MVP

Goal:

Build the minimum React UI around the working backend.

Includes:

- landing/public demo
- goal intake
- today view
- week view
- roadmap view
- parking lot
- adjust plan panel
- proposal apply/discard

Done when:

- user can experience the core product loop through the UI
- UI consumes real backend APIs
- public demo works without real AI cost

Do not add:

- mobile app
- dashboards
- complex settings
- calendar integrations
- notifications

## Phase 12: Polish and Portfolio Readiness

Goal:

Make the MVP presentable.

Includes:

- basic responsive layout
- loading/error states
- empty states
- README
- architecture notes
- demo script
- deployment
- screenshots/video walkthrough

Done when:

- project can be shown to employers
- README explains product and architecture
- demo flow is reliable
- deployed app works

## Current Priority

Start with Phase 1.

Do not skip ahead to OpenAI or frontend polish before the backend domain spine works.
