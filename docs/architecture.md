# ScatterPath Architecture

## Overview

ScatterPath uses a React frontend, a Python FastAPI backend, a Postgres database, and OpenAI integration behind an internal AI service layer.

The backend should be built first around the core domain:

Goal → Plan → Week → Today Task → AI Proposal

The frontend should consume backend APIs and should not contain business-critical planning logic.

## High-Level System

```txt
React Frontend
  ↓
FastAPI Backend
  ↓
Services Layer
  ↓
Database / AI Provider
```

The backend owns:

- goal creation
- plan persistence
- task state
- AI proposal creation
- proposal application
- usage limits
- AI usage logging

The frontend owns:

- user interactions
- displaying Today / Week / Roadmap / Parking Lot
- submitting user requests
- showing AI proposals
- apply/discard actions

## Backend Stack

- Python
- FastAPI
- SQLModel
- Pydantic
- Alembic
- Postgres
- OpenAI SDK

## Frontend Stack

- React
- TypeScript
- Vite
- TanStack Query eventually
- Tailwind eventually

## Backend Project Shape

Preferred backend structure:

```txt
backend/
  app/
    api/
      routes/
    ai/
    core/
    db/
    models/
    schemas/
    services/
    tests/
  main.py
  pyproject.toml
```

## Layer Responsibilities

### API Layer

The API layer handles HTTP requests and responses.

Route handlers should stay thin.

Route handlers should:

- validate request input
- call services
- return response schemas

Route handlers should not contain heavy business logic.

### Services Layer

The services layer contains application behavior.

Examples:

- GoalService
- PlanService
- TodayService
- ProposalService
- UsageLimitService
- AIPlanningService

Services are responsible for coordinating models, database operations, validation, and AI calls.

### Models Layer

The models layer contains SQLModel database models.

Models should represent persisted state.

Examples:

- UserProfile
- Goal
- Plan
- Milestone
- WeekPlan
- Task
- ParkingLotItem
- AIProposal
- AIUsageLog

### Schemas Layer

The schemas layer contains request and response models.

Schemas should be explicit and typed.

Do not expose database models directly as public API contracts unless it is intentionally simple and safe.

### AI Layer

The AI layer hides provider-specific implementation details.

The app should call internal AI services, not OpenAI directly from route handlers.

Expected provider structure:

```txt
AIProvider
OpenAIProvider
MockAIProvider
```

The mock provider should be built first so the core product can be developed without spending tokens.

## AI Proposal Rule

AI must not directly mutate saved plan state.

The normal flow is:

```txt
User request
  → AI service creates proposal
  → backend validates proposal
  → user applies or discards proposal
  → backend mutates saved state only after approval
```

This protects the user from accidental AI changes and keeps application state understandable.

## Initial API Areas

MVP backend should eventually support:

```txt
GET    /health

POST   /goals
GET    /goals/active

POST   /plans/generate
GET    /plans/active

GET    /today
POST   /today/complete
POST   /today/skip

POST   /ai/adjust
POST   /ai/proposals/{proposal_id}/apply
POST   /ai/proposals/{proposal_id}/discard

GET    /parking-lot
POST   /parking-lot
```

Exact route names may evolve, but the responsibilities should stay focused.

## Auth Direction

MVP should use managed auth rather than custom auth.

Preferred direction:

- Supabase Auth or Clerk
- Backend stores local user profile records
- Backend associates goals/plans/tasks with the authenticated user

Do not build custom auth unless explicitly revisited.

Early backend work may use a temporary placeholder user while the domain model is being built.

## AI Usage and Cost Control

All AI requests should go through an AI gateway/service.

The gateway should eventually handle:

- user permission checks
- free trial usage limits
- IP/request limits
- action-level token budgets
- prompt/input length limits
- output token limits
- provider selection
- structured response validation
- AI usage logging

Do not scatter OpenAI calls throughout the codebase.

## Data Ownership

Each user owns their own goals, plans, tasks, proposals, and parking lot items.

MVP supports one active goal per user.

Multiple active goals are out of scope for MVP.

## Demo Strategy

The public demo should use seeded data and mock AI behavior.

The signed-in free trial may use hosted AI with strict limits.

Full users may provide their own OpenAI API key.

For MVP, user-provided OpenAI keys should be session-only unless persistent encrypted storage is explicitly added later.

## Development Order

Build in this order:

1. Backend project structure
2. Health check
3. Core domain models
4. Database setup and migrations
5. Goal creation
6. Mock plan generation
7. Today task retrieval and completion
8. AI proposal model
9. Mock adjust/apply/discard flow
10. Usage logging and limits
11. Auth
12. OpenAI provider
13. Frontend views

Do not start with OpenAI integration.

Do not start with polished UI.

Build the domain spine first.
