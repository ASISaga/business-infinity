---
description: "Derives an executable task list from an implementation plan: reads plan.md and supporting docs, parallelises independent tasks, and writes tasks.md ready for a Task agent"
name: "speckit_tasks"
agent: "agent"
model: "Auto"
tools: ['*']
---

# /speckit.tasks — Task List Command

**Version**: 1.0.0
**Last Updated**: 2026-03-07

## Role

Analyse an implementation plan and its supporting documents to produce a concrete, executable task list. Tasks must be precise enough for a Task agent or developer to execute without further clarification. Independent tasks are marked for parallelisation.

## Input

`/speckit.tasks`

Must be run inside a feature branch. Requires `plan.md`. Uses `data-model.md`, `contracts/`, and `research.md` if present.

## Pre-condition Check

Verify:
1. `specs/<NNN>-<slug>/plan.md` exists
2. Constitutional gates were passed in plan.md (check Phase -1 section)
3. `contracts/` directory exists with at least one contract file

If `plan.md` is missing, stop and direct the user to run `/speckit.plan` first.

## Workflow

### Step 1: Parse Inputs

Read all available documents:

| File | Purpose |
|------|---------|
| `plan.md` | Primary input: phases, technical decisions, implementation approach |
| `data-model.md` | Entity definitions → model/schema tasks |
| `contracts/api.md` | API contracts → endpoint/handler tasks |
| `research.md` | Library choices → dependency setup tasks |
| `quickstart.md` | Validation scenarios → test tasks |

### Step 2: Derive Tasks

Convert each document into tasks:

**From contracts/**:
- One task per API endpoint or event handler
- One contract test task per endpoint

**From data-model.md**:
- One task per entity (schema/model creation)
- One migration task if DB changes are needed

**From plan.md phases**:
- One task per implementation phase item
- Setup and configuration tasks from Phase 0
- Integration tasks from final phases

**Always include**:
- Dependency installation task (from research.md)
- Contract tests before implementation tasks
- Integration test tasks
- End-to-end validation task (from quickstart.md)

### Step 3: Apply Test-First Ordering (Article III)

Tasks must follow this order within each feature area:

```
1. [contract tests] Define and write contract tests
2. [integration tests] Write integration tests
3. [implementation] Write source code to pass tests
4. [e2e tests] Write end-to-end tests
5. [validation] Run full test suite
```

### Step 4: Parallelisation Analysis

Mark tasks that have no dependencies on each other with `[P]`:

```
## Parallel Group A
- [P] task-A1: Create User entity schema
- [P] task-A2: Create Order entity schema
- [P] task-A3: Install dependencies

## Sequential (depends on Group A)
- task-B1: Create database migrations (depends on A1, A2)
```

Rules:
- Tasks in the same parallel group have zero dependencies on each other
- A task can only be in one group
- Groups are ordered by dependency chain

### Step 5: Populate tasks.md

Copy `.github/templates/tasks.md` and populate with all derived tasks.

Each task entry:
```markdown
- [ ] [P] task-NNN: <verb> <object> — <brief rationale linking to spec/plan>
  - Input: <what is needed>
  - Output: <what is produced>
  - Test: <how to verify completion>
```

### Step 6: Validate

```bash
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/tasks.md
```

## Output

```
specs/<NNN>-<slug>/
└── tasks.md   ← Executable task list with parallel groups
```

Confirm to the user:
- Total tasks generated
- Parallel groups identified
- Estimated sequential depth (critical path length)
- Next step: review tasks.md and begin execution

## Task Quality Standards

Every task must be:
- **Atomic**: Single, verifiable deliverable
- **Traceable**: Links back to spec user story or plan phase
- **Testable**: Has explicit verification step
- **Sized**: Completable in ≤4 hours by one person

Reject vague tasks like "implement the feature" — break them down.

## Related Documentation

→ **SDD spec**: `.github/specs/spec-driven-development.md`
→ **Full methodology**: `.github/docs/spec-driven.md`
→ **Tasks template**: `.github/templates/tasks.md`
→ **Specify command**: `.github/prompts/speckit.specify.prompt.md`
→ **Plan command**: `.github/prompts/speckit.plan.prompt.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`
