---
description: "Generates a comprehensive implementation plan from an existing feature spec: runs constitutional gates, translates requirements to technical architecture, and produces supporting documents"
name: "speckit_plan"
agent: "agent"
model: "Auto"
tools: ['*']
---

# /speckit.plan — Implementation Plan Command

**Version**: 1.0.0
**Last Updated**: 2026-03-07

## Role

Read an existing `spec.md` and generate a full implementation plan that bridges business requirements and technical architecture. Every technical decision traces back to a specific requirement. You enforce the Nine Constitutional Articles through Phase -1 gates.

## Input

`/speckit.plan <optional hints>`

Must be run inside a feature branch with `specs/<NNN>-<slug>/spec.md` already present.

Example: `/speckit.plan use WebSocket for real-time, PostgreSQL for persistence`

## Pre-condition Check

Before planning, verify:

1. `spec.md` exists in the current feature directory
2. No `[NEEDS CLARIFICATION]` markers remain in `spec.md`
3. All acceptance criteria are measurable

If any condition fails, stop and report what must be resolved first.

## Workflow

### Phase -1: Constitutional Gates

Run all gates before writing any plan content. A failed gate must be documented in the Complexity Tracking section.

#### Simplicity Gate (Article VII)
- [ ] Using ≤3 projects for initial implementation?
- [ ] No future-proofing added beyond stated requirements?
- [ ] Complexity justified by specific user story?

#### Anti-Abstraction Gate (Article VIII)
- [ ] Using framework features directly rather than wrapping them?
- [ ] Single model representation (no DTO proliferation)?
- [ ] Each abstraction layer justified by concrete benefit?

#### Integration-First Gate (Article IX)
- [ ] Contracts defined before implementation?
- [ ] Contract tests will be written before source code?
- [ ] Real services preferred over mocks?

#### Test-First Gate (Article III)
- [ ] Tests will be written and approved before implementation code?
- [ ] Test scenarios derived from acceptance criteria?
- [ ] Red phase (failing tests) confirmed before implementation?

### Step 1: Read and Analyse Spec

Parse `specs/<NNN>-<slug>/spec.md`:
- Extract user stories with roles, goals, benefits
- Map each story to technical requirements
- Identify data entities, API surface, integration points
- Determine non-functional constraints

### Step 2: Generate research.md

Copy `.github/templates/research.md` and populate:
- Investigate library options for key technical decisions
- Document performance benchmarks if relevant
- Note security implications
- Record organizational constraints from the repository spec

### Step 3: Generate data-model.md

Copy `.github/templates/data-model.md` and populate:
- Define all entities with fields and types
- Document relationships
- Map entities to user stories

### Step 4: Generate contracts/api.md

Define all API contracts before implementation:
- REST endpoints or Azure Functions HTTP triggers
- Request/response schemas
- Error codes and messages
- WebSocket events (if applicable)

### Step 5: Populate plan.md

Copy `.github/templates/plan.md` and populate:
- Link every technical decision to a specific user story
- Document all technology choices with rationale
- Define implementation phases with clear prerequisites
- Extract complex details to `implementation-details/<component>-details.md` files
- Keep plan.md high-level and readable

### Step 6: Generate quickstart.md

Capture key validation scenarios:
- Happy path end-to-end scenario
- Critical error paths
- Performance validation approach

### Step 7: Validate

```bash
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/plan.md
```

## Output

```
specs/<NNN>-<slug>/
├── plan.md           ← Implementation plan (high-level)
├── research.md       ← Library/API research
├── data-model.md     ← Entity schemas
├── contracts/
│   └── api.md        ← API/event contracts
└── quickstart.md     ← Key validation scenarios
```

Confirm to the user:
- All files created
- Any constitutional gates that failed (and documented exceptions)
- Next step: review plan, then run `/speckit.tasks`

## Plan Quality Standards

The plan must remain high-level and readable. Detailed technical content belongs in separate files:

```
IMPORTANT: plan.md should remain navigable.
Any code samples, detailed algorithms, or extensive technical specifications
must be placed in implementation-details/ files.
```

## File Creation Order (Test-First)

1. Create `contracts/` with API specifications
2. Create test files: contract tests → integration tests → e2e → unit
3. Create source files to make tests pass

## Related Documentation

→ **SDD spec**: `.github/specs/spec-driven-development.md`
→ **Full methodology**: `.github/docs/spec-driven.md`
→ **Plan template**: `.github/templates/plan.md`
→ **Specify command**: `.github/prompts/speckit.specify.prompt.md`
→ **Tasks command**: `.github/prompts/speckit.tasks.prompt.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`
→ **Repository spec**: `.github/specs/repository.md`
