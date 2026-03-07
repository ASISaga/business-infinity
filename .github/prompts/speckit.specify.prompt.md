---
description: "Creates a structured feature specification from a plain-language description using the SDD methodology: auto-numbers, branches, and populates a spec template"
name: "speckit_specify"
agent: "agent"
model: "Auto"
tools: ['*']
---

# /speckit.specify — Feature Specification Command

**Version**: 1.0.0
**Last Updated**: 2026-03-07

## Role

Transform a plain-language feature description into a complete, structured specification using the SDD methodology. You act as a disciplined specification engineer, not a creative writer.

## Input

`/speckit.specify <feature description>`

Example: `/speckit.specify Real-time dashboard showing agent orchestration status`

## Workflow

### Step 1: Determine Feature Number

```bash
./.github/skills/spec-manager/scripts/list-specs.sh
```

Scan `specs/` for the highest existing feature number, then increment by 1. Use zero-padded three digits: `001`, `002`, `003`.

### Step 2: Create Branch and Directory

```bash
./.github/skills/spec-manager/scripts/create-feature-branch.sh "<description>"
```

This creates the branch `<NNN>-<kebab-slug>` and the directory `specs/<NNN>-<kebab-slug>/`.

Slug rules: lowercase, hyphens only, max 5 words, skip stop words (a, an, the, conjunctions, prepositions, common auxiliaries — see `create-feature-branch.sh` for full list).

### Step 3: Populate spec.md

Copy `.github/templates/spec.md` → `specs/<NNN>-<slug>/spec.md`.

Fill every section from the user description:

- **Feature Name**: Concise title derived from description
- **Feature Number**: The determined NNN
- **User Stories**: Extract from description; add `[NEEDS CLARIFICATION]` for missing roles/goals
- **Acceptance Criteria**: Measurable, testable conditions only
- **Non-Functional Requirements**: Performance, security, reliability; mark unknowns
- **Out of Scope**: Explicitly exclude adjacent concerns
- **Open Questions**: List anything that needs human decision

### Step 4: Apply Clarification Markers

For **every** ambiguity, add:

```
[NEEDS CLARIFICATION: <specific question>]
```

**Never guess**. Mark it if the description doesn't specify:
- Authentication method
- Data retention policy
- Performance targets
- Integration endpoints
- Error handling behaviour
- User roles

### Step 5: Spec Quality Self-Check

Before finishing, verify:
- [ ] Every user story has role, goal, and benefit
- [ ] Acceptance criteria are measurable (numbers, not adjectives)
- [ ] No technology choices made (no "use React", "use PostgreSQL")
- [ ] No implementation details (no class names, API paths, SQL)
- [ ] No speculative features without user story backing
- [ ] All ambiguities marked with `[NEEDS CLARIFICATION]`

### Step 6: Validate

```bash
./.github/skills/spec-manager/scripts/validate-spec.sh specs/<NNN>-<slug>/spec.md
```

## Output

```
specs/<NNN>-<slug>/
└── spec.md   ← Populated feature specification
```

Confirm to the user:
- Branch name created
- Location of `spec.md`
- Count of `[NEEDS CLARIFICATION]` markers requiring resolution
- Next step: resolve markers, then run `/speckit.plan`

## Template Constraints

The spec.md template enforces:

✅ Focus on **WHAT** users need and **WHY**
❌ Avoid **HOW** to implement (no tech stack, APIs, code structure)

This keeps specs stable even as implementation technologies change.

## Related Documentation

→ **SDD spec**: `.github/specs/spec-driven-development.md`
→ **Full methodology**: `.github/docs/spec-driven.md`
→ **Spec template**: `.github/templates/spec.md`
→ **Plan command**: `.github/prompts/speckit.plan.prompt.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`
