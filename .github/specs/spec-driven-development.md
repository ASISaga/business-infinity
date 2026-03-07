# Specification-Driven Development (SDD)

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2026-03-07

## Overview

Specification-Driven Development (SDD) inverts the traditional relationship between specs and code: specifications are the primary artifact; code is their generated expression. This spec defines how SDD is practiced in this repository through structured commands, templates, and constitutional principles.

→ **Full methodology**: `.github/docs/spec-driven.md`

## Scope

- SDD workflow for the `.github/specs/` directory
- speckit command definitions (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`)
- Specification templates, constitutional gates, and validation rules
- Integration with the GitHub Copilot agent intelligence system

## The Three speckit Commands

### `/speckit.specify <description>`

Transforms a feature description into a complete, structured specification:

1. **Auto-number**: Scan `specs/` for the next feature number (e.g., `001`, `002`)
2. **Branch**: Generate a semantic branch name and create it (`git checkout -b <NNN>-<slug>`)
3. **Directory**: Create `specs/<NNN>-<slug>/`
4. **Template**: Copy `.github/templates/spec.md` → `specs/<NNN>-<slug>/spec.md` and populate
5. **Clarify**: Mark ambiguities with `[NEEDS CLARIFICATION: <question>]`

### `/speckit.plan <hints>`

Reads `spec.md` and produces a full implementation plan:

1. **Parse spec**: Extract user stories, acceptance criteria, constraints
2. **Constitutional gates** (Phase -1): Check Articles VII, VIII, IX
3. **Generate plan**: Create `specs/<NNN>-<slug>/plan.md` from `.github/templates/plan.md`
4. **Supporting docs**: Create `data-model.md`, `research.md`, `contracts/`, `quickstart.md`

### `/speckit.tasks`

Reads `plan.md` (and optional `data-model.md`, `contracts/`, `research.md`) → writes `tasks.md`:

1. **Derive tasks**: Convert contracts, entities, and scenarios into specific tasks
2. **Parallelise**: Mark independent tasks `[P]` and group safe parallel clusters
3. **Output**: `specs/<NNN>-<slug>/tasks.md` ready for a Task agent

## Feature Directory Structure

```
specs/
└── NNN-feature-slug/
    ├── spec.md                      ← Feature specification (from /speckit.specify)
    ├── plan.md                      ← Implementation plan (from /speckit.plan)
    ├── research.md                  ← Library/API research (from /speckit.plan)
    ├── data-model.md                ← Entity schemas (from /speckit.plan)
    ├── contracts/                   ← API/event contracts (from /speckit.plan)
    │   └── api.md
    ├── quickstart.md                ← Key validation scenarios (from /speckit.plan)
    ├── tasks.md                     ← Executable task list (from /speckit.tasks)
    └── implementation-details/      ← Detailed technical content extracted from plan.md
        └── [component]-details.md
```

## Specification Templates

| Template | Purpose | Command |
|----------|---------|---------|
| `.github/templates/spec.md` | Feature specification | `/speckit.specify` |
| `.github/templates/plan.md` | Implementation plan | `/speckit.plan` |
| `.github/templates/tasks.md` | Task list | `/speckit.tasks` |
| `.github/templates/research.md` | Research document | `/speckit.plan` |
| `.github/templates/data-model.md` | Data model | `/speckit.plan` |

## Constitutional Principles (Nine Articles)

These articles are enforced through Phase -1 gates in the implementation plan template.

| Article | Principle | Enforcement |
|---------|-----------|-------------|
| I | Library-First: every feature starts as a standalone library | Spec checklist |
| II | CLI Interface: every library exposes a CLI (stdin→stdout, JSON) | Plan gate |
| III | Test-First: tests written and approved before any implementation code | Phase -1 gate |
| VII | Simplicity: ≤3 projects for initial implementation | Simplicity gate |
| VIII | Anti-Abstraction: use framework directly; single model representation | Anti-abstraction gate |
| IX | Integration-First: real DBs/services over mocks; contract tests before implementation | Integration gate |

## Clarification Markers

All ambiguities **must** be surfaced with:

```
[NEEDS CLARIFICATION: <specific question about the missing or ambiguous detail>]
```

**Never guess**. If the prompt doesn't specify something, mark it. The spec is blocked until all markers are resolved.

## Spec Quality Gates

A spec is ready to proceed to planning when:

- [ ] No `[NEEDS CLARIFICATION]` markers remain
- [ ] All user stories follow `As a <role>, I want <goal>, so that <benefit>`
- [ ] Acceptance criteria are measurable and testable
- [ ] Non-functional requirements (performance, security, reliability) are explicit
- [ ] No implementation details (no tech stack, APIs, or code structure in spec.md)
- [ ] No speculative or "might need" features

## Validation

```bash
# Validate a spec file for completeness
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/spec.md

# List all feature specs and their status
./.github/skills/spec-manager/scripts/list-specs.sh

# Create a feature branch and directory for a new spec
./.github/skills/spec-manager/scripts/create-feature-branch.sh "<description>"
```

## References

→ **Full SDD methodology**: `.github/docs/spec-driven.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`
→ **speckit.specify prompt**: `.github/prompts/speckit.specify.prompt.md`
→ **speckit.plan prompt**: `.github/prompts/speckit.plan.prompt.md`
→ **speckit.tasks prompt**: `.github/prompts/speckit.tasks.prompt.md`
→ **Agent framework**: `.github/specs/agent-intelligence-framework.md`
→ **Repository spec**: `.github/specs/repository.md`
