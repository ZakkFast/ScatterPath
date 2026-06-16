# ScatterPath Product Context

## Product Summary

ScatterPath is an AI-assisted planning system that helps overwhelmed users turn vague goals into realistic daily action while preserving visibility into the bigger picture.

The app is not a general task manager.

The app is not a chatbot.

The app is a planning system where AI helps create, simplify, adjust, and recover plans.

## Core Product Loop

The core loop is:

1. User creates a goal.
2. AI generates a structured plan.
3. User sees what to do today.
4. User completes, skips, or adjusts the task.
5. AI proposes plan changes when reality changes.
6. User applies or discards the proposal.
7. The system keeps the user moving forward.

## Product Philosophy

ScatterPath should reduce decisions, preserve context, and maintain momentum.

The user should not need to behave like a project manager.

The default experience should answer:

"What should I do right now?"

The bigger picture should be available, but not overwhelming.

## Target Users

ScatterPath is for people who:

- feel overwhelmed
- have too many competing priorities
- struggle to start
- struggle to prioritize
- frequently abandon plans
- need help turning uncertainty into action

Examples include:

- software developers
- students
- career changers
- solo builders
- professionals managing multiple responsibilities
- people with ADHD or executive dysfunction

ScatterPath is not specifically an ADHD app, but it should work well for people with ADHD.

## MVP Goal

The MVP should prove that a user can:

1. Enter a meaningful goal.
2. Receive a useful AI-generated plan.
3. Understand what to do today.
4. Adjust the plan when life changes.
5. Avoid losing important future ideas.

## MVP Views

The MVP supports these product areas:

### Landing / Public Demo

A public, seeded demo that shows the product without requiring login or API keys.

This should not cost real AI tokens.

### Goal Intake

A guided flow where the user provides enough context for AI planning.

Required context:

- goal title
- goal description
- timeframe or target date
- available time
- current situation
- constraints

### Today

The primary execution view.

Shows:

- primary task
- estimated time
- why it matters
- success criteria
- complete action
- skip action
- simplify action
- adjust plan action

### Week

The current week view.

Shows:

- weekly focus
- current week tasks
- task statuses

### Roadmap

The high-level view.

Shows:

- goal
- milestones
- current progress
- where today's work fits

### Parking Lot

A place to save ideas that should not derail the active goal.

Examples:

- learn Rust
- build a game
- start a business
- write a book

The Parking Lot protects focus without losing ideas.

### Adjust Plan

A natural-language command panel.

This is not full chat.

The user can say things like:

- "I only have 20 minutes today."
- "This task is too hard."
- "I missed three days."
- "Make this week easier."
- "Park this idea for later."

The AI should return a structured proposal.

The user can apply or discard the proposal.

## User Modes

### Public Demo

No login required.

Uses seeded data and mock AI behavior.

Costs nothing.

### Free Signed-In User

Requires login.

Allows limited hosted AI usage:

- one AI-generated plan
- three AI actions

Strict limits should protect against token abuse.

### Full User

User provides their own OpenAI API key.

For MVP, user API keys should be session-only unless explicitly changed later.

Even with user-provided keys, the app should protect users with sensible input, output, and usage limits.

## MVP Includes

- public seeded demo
- user signup/login
- one active goal per user
- goal intake
- structured AI plan generation
- today task
- week plan
- roadmap/milestones
- parking lot
- AI adjustment proposals
- apply/discard proposal flow
- mock AI provider first
- OpenAI provider later
- basic usage limits
- AI usage logging

## MVP Excludes

Do not add these unless explicitly requested:

- full chatbot
- chat history
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
- complex analytics

## Product Rule

When making product or technical decisions, favor the option that makes it easier for the user to know what to do next.

If a feature adds management overhead without improving execution, it probably does not belong in the MVP.
