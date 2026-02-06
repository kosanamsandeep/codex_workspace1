# One-Day Build Plan (Clean Architecture Study Planner)

This file is the shared checklist for all developers. We will mark items as done as we complete them.

## Use Case
Personal Study Planner (CLI, offline). Features: manage courses/topics, plan sessions, complete sessions, generate reports. No network or database usage.

## Team Assignments
- Dev A: Domain entities + value objects + type annotations
- Dev B: Application use cases
- Dev C: Repositories/adapters (in-memory + JSON file)
- Dev D: CLI + end-to-end tests

## TODO (One Day)
- [ ] Step 1: Finalize requirements + acceptance criteria
- [x] Step 2: Create `dev` branch + folder structure
- [x] Step 3: Create feature branches for each dev
- [x] Step 4: Implement Domain layer (Dev A)
- [x] Step 5: Implement Use Cases (Dev B)
- [x] Step 6: Implement Repositories/Adapters (Dev C)
- [x] Step 7: Implement CLI + E2E tests (Dev D)
- [ ] Step 8: Add unit + integration tests
- [ ] Step 9: Documentation updates (README + docstrings)
- [ ] Step 10: Run tests, merge into `dev`, PR to `main`

## PR Workflow
- Feature branches are created from `dev`
- Open PRs into `dev`
- Validate: unit + integration + e2e tests pass
- After `dev` is stable, open PR from `dev` into `main`

## Step 1: Requirements + Acceptance Criteria
### Scope
- Offline CLI application; no network calls, no external DB
- Local persistence via JSON file
- Clean Architecture + SOLID principles + type annotations
- Tests: unit, integration, end-to-end

### Core Features
- Courses: create/list/delete
- Topics: add/remove/list per course
- Sessions: plan (date, duration, topic), complete, list
- Reports: weekly summary, total time per course/topic, streaks

### Acceptance Criteria
- CLI supports all core features with clear commands
- Domain layer has no dependency on infrastructure or CLI
- Use cases depend on interfaces (ports), not concrete storage
- In-memory repository is used for unit tests
- JSON repository is used for integration and CLI
- Tests cover: domain, use cases, repository, and CLI flows
- Documentation includes architecture overview and usage examples
