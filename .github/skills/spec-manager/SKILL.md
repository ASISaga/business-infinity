---
name: spec-manager
description: Manage specification-driven development workflow for .github/specs/. Create, validate, and update feature specifications, implementation plans, and task lists using speckit commands. Use when executing /speckit.specify, /speckit.plan, or /speckit.tasks to produce structured, executable specifications.
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: specification
  role: specification-engineer
allowed-tools: Bash(git:*) Bash(mkdir:*) Bash(cp:*) Read Edit Create
---

# Spec Manager

**Role**: Specification Engineer for SDD Workflow
**Scope**: `specs/`, `.github/specs/`, `.github/templates/`
**Version**: 1.0

## Purpose

Implement the Specification-Driven Development (SDD) workflow through three speckit commands that transform plain-language descriptions into structured, executable specifications.

→ **Complete methodology**: `.github/docs/spec-driven.md`
→ **SDD spec**: `.github/specs/spec-driven-development.md`

## When to Use This Skill

Activate when:
- User runs `/speckit.specify` to create a new feature spec
- User runs `/speckit.plan` to generate an implementation plan
- User runs `/speckit.tasks` to produce an executable task list
- Validating spec completeness before planning
- Listing existing specs to determine next feature number

## Core Principles

**Spec-First**: Specifications drive code, not the reverse
**Clarify, Don't Guess**: Mark all ambiguities with `[NEEDS CLARIFICATION]`
**Constitutional Gates**: Enforce Articles III, VII, VIII, IX before planning
**Test-First Ordering**: Contract tests → integration tests → implementation

## Validation Scripts

### 1. Spec Validation

```bash
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/spec.md

# Checks:
# - No [NEEDS CLARIFICATION] markers remain
# - Required sections are present
# - User stories have role/goal/benefit
# - Acceptance criteria are measurable
```

### 2. List Specs

```bash
./.github/skills/spec-manager/scripts/list-specs.sh

# Shows:
# - All feature directories in specs/
# - Status of spec.md, plan.md, tasks.md
# - Next available feature number
```

### 3. Create Feature Branch

```bash
./.github/skills/spec-manager/scripts/create-feature-branch.sh "<description>"

# Creates:
# - git branch NNN-kebab-slug
# - specs/NNN-kebab-slug/ directory
```

## speckit Workflow

```bash
# Step 1: Create specification (5 minutes)
/speckit.specify Real-time agent status dashboard

# Step 2: Generate implementation plan (5 minutes)
/speckit.plan use WebSocket, Azure Functions, Service Bus

# Step 3: Generate task list (5 minutes)
/speckit.tasks
```

## Templates

| Template | Used By |
|----------|---------|
| `.github/templates/spec.md` | `/speckit.specify` |
| `.github/templates/plan.md` | `/speckit.plan` |
| `.github/templates/tasks.md` | `/speckit.tasks` |
| `.github/templates/research.md` | `/speckit.plan` |
| `.github/templates/data-model.md` | `/speckit.plan` |

## Validation

**Before committing spec changes:**

```bash
# Validate spec completeness
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/spec.md

# List all specs
./.github/skills/spec-manager/scripts/list-specs.sh
```

## Resources

→ `.github/specs/spec-driven-development.md` — SDD workflow and principles
→ `.github/docs/spec-driven.md` — Full SDD methodology
→ `.github/agents/spec-manager.agent.md` — Agent definition
→ `.github/prompts/speckit.specify.prompt.md` — Specify command
→ `.github/prompts/speckit.plan.prompt.md` — Plan command
→ `.github/prompts/speckit.tasks.prompt.md` — Tasks command

---

**Version History**:
- **v1.0** (2026-03-07): Initial spec manager skill
