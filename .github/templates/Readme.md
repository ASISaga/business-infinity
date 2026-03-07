# Templates

Specification templates for the Spec-Driven Development (SDD) workflow. Used by the Spec Manager Agent via speckit commands.

→ **SDD workflow**: `.github/specs/spec-driven-development.md`
→ **Spec manager agent**: `.github/agents/spec-manager.agent.md`

## Available Templates

| Template | Command | Purpose |
|----------|---------|---------|
| `spec.md` | `/speckit.specify` | Feature specification: user stories, acceptance criteria, non-functional requirements |
| `plan.md` | `/speckit.plan` | Implementation plan: constitutional gates, technology choices, implementation phases |
| `tasks.md` | `/speckit.tasks` | Task list: atomic tasks with parallelisation groups and verification steps |
| `research.md` | `/speckit.plan` | Research document: library options, benchmarks, security considerations |
| `data-model.md` | `/speckit.plan` | Data model: entity schemas, relationships, validation rules |

## Usage

Templates are copied and populated by the Spec Manager Agent. Do not use them directly.

```bash
# The agent copies and populates templates automatically:
/speckit.specify <description>   → copies spec.md → specs/NNN-slug/spec.md
/speckit.plan <hints>            → copies plan.md, research.md, data-model.md
/speckit.tasks                   → copies tasks.md → specs/NNN-slug/tasks.md
```

## Template Design Principles

Templates enforce SDD constraints on the LLM:
- **Clarification markers** surface all ambiguities: `[NEEDS CLARIFICATION: <question>]`
- **Constitutional gates** enforce Articles III, VII, VIII, IX
- **Test-first ordering** ensures contracts precede implementation
- **Completeness checklists** act as self-review unit tests
- **Abstraction discipline** keeps spec.md technology-free
