# AGENTS.md

## Project

ScatterPath is an AI-assisted planning system that helps overwhelmed users turn vague goals into realistic daily action while preserving visibility into the bigger picture.

The core loop is:

Goal → AI-generated plan → today’s task → user executes → AI adjusts/replans when reality changes.

## Current MVP Focus

Build the backend foundation first.

The MVP should support:

- one active goal per user
- goal intake
- structured plan generation
- roadmap, week plan, and today task models
- parking lot items
- AI adjustment proposals
- apply/discard proposal flow
- usage limits and AI usage logging
- OpenAI integration later
- mock AI provider first

Do not build non-MVP features unless explicitly requested.

## Stack

Backend:

- Python
- FastAPI
- SQLModel
- Pydantic
- Alembic
- Postgres
- OpenAI SDK eventually

Frontend:

- React
- TypeScript
- Vite
- TanStack Query eventually
- Tailwind eventually

## Engineering Priorities

Favor:

- simple, readable code
- small focused changes
- clear domain models
- service-layer business logic
- typed request/response schemas
- explicit validation
- practical MVP decisions

Avoid:

- unnecessary abstractions
- premature optimization
- feature creep
- large unrelated refactors
- hidden magic
- direct AI state mutation
- building full chat behavior

## Architecture Rules

AI must not directly mutate saved plan state.

AI actions should return proposals.

The normal flow is:

User request → AI proposal → validation → user applies/discards → database update.

Route handlers should stay thin.

Business logic belongs in services.

Database models belong in `app/models`.

Request/response schemas belong in `app/schemas`.

AI provider logic belongs in `app/ai`.

API routes belong in `app/api`.

## AI Rules

The AI system should behave like a planning partner, not a chatbot.

Supported AI actions for MVP:

- generate_plan
- adjust_plan
- simplify_today
- recover_plan
- park_idea
- clarify_task

AI output should be structured and validated.

Do not return unstructured markdown blobs for app state.

## Scope Guardrails

Do not add these unless specifically requested:

- full chat
- multiple active goals
- teams
- collaboration
- social features
- gamification
- streaks
- calendar integration
- notifications
- mobile app
- multiple AI providers
- persistent encrypted API key storage
- task dependencies
- tags
- custom workflows

## Development Workflow

Before making changes:

1. Read the relevant docs in `/docs`.
2. Inspect existing code.
3. Make the smallest reasonable change.
4. Do not add unrelated features.
5. Keep the implementation aligned with the MVP.

For larger or ambiguous tasks, propose a plan before editing files.

## Definition of Done

A task is done when:

- the requested behavior works
- relevant code is typed and validated
- obvious edge cases are handled
- tests are added or updated when useful
- the app can still run
- no unrelated scope was added

## Local Commands

Backend commands should use `uv`.

Common backend commands:

```bash
cd backend
uv run fastapi dev main.py
```

Frontend commands:

```bash
cd frontend
npm run dev
```

Update this file as the project structure becomes more concrete.
