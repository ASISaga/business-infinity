---
applyTo: ".github/specs/*.md"
description: "Standards for specification files in .github/specs/ including spec-driven development (SDD) workflow"
---

# Specification Files Standards

## Purpose

Specification files in `.github/specs/` contain **detailed patterns and frameworks** that instruction files reference. They define the "what" and "how" of systems.

Specifications are created and updated using the **Spec Manager Agent** (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`).

→ **SDD workflow**: `.github/specs/spec-driven-development.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`

## Spec-Driven Development (SDD) Workflow

New specifications for this repository use the speckit commands:

```bash
# Create a new specification
/speckit.specify <plain-language description>

# Generate implementation plan from spec
/speckit.plan <optional technical hints>

# Derive executable task list from plan
/speckit.tasks
```

All specs created via speckit are placed in `specs/<NNN>-<slug>/`. Specs in `.github/specs/` document the agent intelligence system itself and follow the standard format below.

## File Naming

- Use kebab-case: `system-name.md`
- Be descriptive: `ontological-design-system.md` not `ontology.md`
- Include version if needed: `agent-framework-v2.md`

## Content Structure

```markdown
# Specification Title

**Version**: X.Y.Z  
**Status**: Draft | Active | Deprecated  
**Last Updated**: YYYY-MM-DD

## Overview
[Brief description of what this specifies]

## Scope
[What's included and excluded]

## Specification
[Detailed patterns, frameworks, requirements]

## Examples
[Code examples and use cases]

## Validation
[How to verify compliance]

## References
[Related specs and docs]
```

## Content Guidelines

✅ **DO Include:**
- Detailed technical specifications
- Complete frameworks and patterns
- Code examples and templates
- Architecture diagrams
- Validation criteria

❌ **DON'T Include:**
- Step-by-step tutorials (belong in `.github/docs/`)
- Path-specific coding standards (belong in `.github/instructions/`)
- Project-specific implementations (reference from specs)

## Cross-References

Specs should be:
- **Referenced from**: Instruction files, documentation files, copilot-instructions.md
- **Never duplicated in**: Instruction files or copilot-instructions.md

## Validation

Before committing:
1. Follows naming convention
2. Has proper version/status/date
3. Clear scope and specification sections
4. Examples are correct and tested
5. No duplication with docs or instructions

## Related Documentation

→ **SDD spec**: `.github/specs/spec-driven-development.md` - Spec-driven workflow and speckit commands
→ **Agent framework**: `.github/specs/agent-intelligence-framework.md` - Complete system specification
→ **Architecture**: `/docs/specifications/architecture.md` - System architecture and organization
→ **Self-learning system**: `/docs/specifications/agent-self-learning-system.md` - Dogfooding and Ouroboros
→ **Agent guidelines**: `/docs/specifications/github-copilot-agent-guidelines.md` - Standards and best practices

---

**Version**: 1.2 - Added SDD workflow and speckit commands
**Last Updated**: 2026-03-07
