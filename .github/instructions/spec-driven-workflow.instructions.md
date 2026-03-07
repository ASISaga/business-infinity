---
applyTo: "specs/**/*.md,.github/specs/*.md,.github/agents/*.agent.md,.github/prompts/*.prompt.md,.github/skills/*/SKILL.md,.github/instructions/*.instructions.md"
description: "Specification-Driven Development (SDD) workflow standards for specs, agents, prompts, skills, and instructions in the agent meta-intelligence system"
---

# Spec-Driven Workflow Instructions

## Overview

All feature specifications and agent-intelligence artefacts in this repository follow the **Specification-Driven Development (SDD)** methodology. Specifications are the primary artefact; code and agent configurations are their generated expression.

→ **Full SDD methodology**: `.github/specs/spec-driven-development.md`

## The Three SDD Stages

| Stage | Prompt | Output |
|-------|--------|--------|
| 1. Specify | `spec-create.prompt.md` | `specs/NNN-slug/spec.md` |
| 2. Plan | `spec-plan.prompt.md` | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` |
| 3. Tasks | `spec-tasks.prompt.md` | `specs/NNN-slug/tasks.md` |

## Spec Files (`specs/NNN-slug/`)

✅ **DO:**
- Focus on **WHAT** and **WHY** — never **HOW**
- Use `As a <role>, I want <goal>, so that <benefit>` for user stories
- Use measurable acceptance criteria (numbers, not adjectives)
- Mark every ambiguity: `[NEEDS CLARIFICATION: <question>]`
- Gate each stage: no unresolved markers before moving to Plan

❌ **DON'T:**
- Include technology names, API paths, or code structure in `spec.md`
- Add speculative features without a backing user story
- Proceed to Plan stage with unresolved `[NEEDS CLARIFICATION]` markers

## Agent Files (`.github/agents/*.agent.md`)

- Follow `.github/specs/agents.md` for format and required fields
- `name` must be kebab-case and match the file stem
- `prompt` must cover: role, responsibilities, activation triggers, workflows, validation scripts
- Corresponding prompt file: `.github/prompts/<name>.prompt.md`

## Prompt Files (`.github/prompts/*.prompt.md`)

- Follow `.github/specs/prompts.md` for format and required fields
- Use `kebab-case` for file name; `snake_case` for `name` field
- Body structure: role → responsibilities → activation → workflows → tool integration → related docs
- Reference SDD scripts for spec workflows:
  ```bash
  ./.github/skills/spec-manager/scripts/list-specs.sh
  ./.github/skills/spec-manager/scripts/create-feature-branch.sh "<description>"
  ./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/spec.md
  ```

## Skill Files (`.github/skills/*/SKILL.md`)

- Follow `.github/specs/skills.md` for format and required fields
- Keep `SKILL.md` lean: offload detailed specs to `references/`, scripts to `scripts/`
- All validation scripts must be executable (`chmod +x`) and return proper exit codes
- Reference existing project tools; never reimplement what a linter/validator already does

## Instruction Files (`.github/instructions/*.instructions.md`)

- Follow `.github/specs/instructions.md` for format and required fields
- `applyTo` glob must be specific and non-overlapping
- Keep content lean: reference `.github/specs/` and `.github/docs/` for details
- No duplication of content already in `copilot-instructions.md`

## SDD Validation Scripts

```bash
# List all feature specs and their status
./.github/skills/spec-manager/scripts/list-specs.sh

# Validate a spec or plan file for completeness
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/spec.md

# Agent quality audit
./.github/skills/agent-evolution-agent/scripts/audit-agent-quality.sh
```

## Quality Gates

A spec is ready to advance when:
- [ ] No `[NEEDS CLARIFICATION]` markers remain
- [ ] All user stories follow the standard format
- [ ] Acceptance criteria are measurable and testable
- [ ] Non-functional requirements have specific targets
- [ ] No implementation details in `spec.md`

## Related Documentation

→ **SDD spec**: `.github/specs/spec-driven-development.md`
→ **Full methodology**: `.github/docs/spec-driven.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`
→ **Agent spec**: `.github/specs/agents.md`
→ **Prompt spec**: `.github/specs/prompts.md`
→ **Skill spec**: `.github/specs/skills.md`
→ **Instruction spec**: `.github/specs/instructions.md`
→ **Agent framework**: `.github/specs/agent-intelligence-framework.md`
