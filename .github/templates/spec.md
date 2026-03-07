# Feature Specification: [FEATURE NAME]

**Feature Number**: [NNN]
**Branch**: [NNN-feature-slug]
**Status**: Draft | In Review | Approved | Implemented
**Created**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]

---

## Overview

> Describe what this feature does and why it matters to users. 2–4 sentences.
> Focus on WHAT and WHY, never HOW.

[NEEDS CLARIFICATION: Feature purpose and user value]

## User Stories

> Format: As a <role>, I want <goal>, so that <benefit>.
> Add one story per distinct user need. Mark ambiguous roles/goals.

- As a [NEEDS CLARIFICATION: user role], I want [NEEDS CLARIFICATION: goal], so that [NEEDS CLARIFICATION: benefit].

## Acceptance Criteria

> Each criterion must be measurable and testable. Use specific numbers, not adjectives.
> ✅ "Response time ≤ 200ms under 100 concurrent users"
> ❌ "The system should be fast"

### [First user story or area]

- [ ] [NEEDS CLARIFICATION: Define measurable acceptance criterion]

### [Second user story or area]

- [ ] [NEEDS CLARIFICATION: Define measurable acceptance criterion]

## Non-Functional Requirements

### Performance
- [NEEDS CLARIFICATION: Response time target under what load?]
- [NEEDS CLARIFICATION: Throughput requirement?]

### Security
- [NEEDS CLARIFICATION: Authentication required? Which method?]
- [NEEDS CLARIFICATION: Data classification? PII involved?]

### Reliability
- [NEEDS CLARIFICATION: Availability target (e.g., 99.9%)?]
- [NEEDS CLARIFICATION: Recovery time objective?]

### Scalability
- [NEEDS CLARIFICATION: Expected user/request volume?]
- [NEEDS CLARIFICATION: Growth projection?]

## Out of Scope

> Explicitly list what this feature does NOT include.
> This prevents scope creep and sets clear boundaries.

- [List what is explicitly excluded]
- [List adjacent features that will be handled separately]

## Dependencies

> List features, services, or data sources this feature depends on.

- [NEEDS CLARIFICATION: External services or APIs?]
- [NEEDS CLARIFICATION: Other features that must exist first?]

## Open Questions

> Questions that require human decision before this spec is complete.
> Remove this section once all questions are answered.

1. [NEEDS CLARIFICATION: Question requiring human decision]

---

## Requirement Completeness Checklist

Before proceeding to `/speckit.plan`, all items must be checked:

- [ ] No `[NEEDS CLARIFICATION]` markers remain
- [ ] Every user story has role, goal, and benefit
- [ ] All acceptance criteria are measurable (numbers, not adjectives)
- [ ] Non-functional requirements have specific targets
- [ ] Out of scope section lists ≥1 exclusion
- [ ] No technology choices made (no framework, database, or library names)
- [ ] No implementation details (no class names, API paths, or SQL)
- [ ] No speculative features without a backing user story
