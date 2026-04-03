---
name: boardroom-agent-state
description: Enrich boardroom agent JSON-LD state files with legend-derived domain knowledge, skills, persona, and language from the boardroom-agents spec
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: boardroom
  role: agent-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# Boardroom Agent State Skill

**Role**: Boardroom Agent State Enrichment Specialist  
**Scope**: `boardroom/state/*.jsonld` — agent context and content layers  
**Version**: 1.0

## Purpose

Enrich the `context` layer of each boardroom agent JSON-LD file with the legend-derived
`domain_knowledge`, `skills`, `persona`, and `language` fields defined in the spec. Ensures
every agent embodies its legendary archetype in full rather than relying on a single-line
`core_logic` string.

## When to Use This Skill

Activate when:
- Adding a new agent to the boardroom roster
- Updating an agent's legend archetype
- Discovering thin or missing context enrichment fields
- Changing the archetype-to-agent mapping in `CXO_DOMAINS`

## Core Responsibilities

1. Read the boardroom-agents spec for the target agent
2. Update the `context.domain_knowledge`, `context.skills`, `context.persona`, and
   `context.language` fields in the agent's JSON-LD file
3. Validate the file loads correctly through `BoardroomStateManager`
4. Run the test suite to confirm no regressions

## Workflow

### 1. Read the spec

```bash
cat .github/specs/boardroom-agents.md
```

### 2. Identify the agent file

```bash
# JSON-LD files: boardroom/state/{agent_id}.jsonld
# JSONL files:   boardroom/state/{agent_id}.jsonl
ls boardroom/state/
```

### 3. Update context enrichment

Open the target file and add or update these four fields inside the `context` object:

```json
"domain_knowledge": ["<area 1>", "<area 2>", "<area 3>", "<area 4>", "<area 5>"],
"skills": ["<skill 1>", "<skill 2>", "<skill 3>", "<skill 4>", "<skill 5>"],
"persona": "<Rich 2–4 sentence identity description from the legend's perspective>",
"language": "<Vocabulary, idioms, and reasoning style — 2–3 sentences>"
```

All content comes directly from the agent's entry in `.github/specs/boardroom-agents.md`.

### 4. Validate

```bash
# Validate all agent states load correctly
PYTHONPATH=/tmp/aos_mock:src python -m pytest tests/ -q -k "boardroom"

# Spot-check context enrichment completeness
PYTHONPATH=/tmp/aos_mock:src python - <<'PY'
from business_infinity.boardroom import BoardroomStateManager
for agent_id in BoardroomStateManager.get_registered_agent_ids():
    ctx = BoardroomStateManager.load_agent_context(agent_id)
    for field in ("domain_knowledge", "skills", "persona", "language"):
        assert field in ctx, f"{agent_id} context missing '{field}'"
    print(f"✓ {agent_id}: {ctx['name']}")
PY
```

### 5. Run full test suite

```bash
PYTHONPATH=/tmp/aos_mock:src python -m pytest tests/ -q
```

## Context Layer Schema

The `context` object is **immutable** (read-only by `BoardroomStateManager`). Required fields:

| Field | Constraint |
|-------|-----------|
| `name` | Legend's full name (string) |
| `fixed_mandate` | Domain mandate (matches `CXO_DOMAINS[id]["domain"]`) |
| `core_logic` | Defining maxim — 1–3 sentences from the legend |
| `immutable_constraints` | List of 3 read-only guiding principles |

Enrichment fields (optional per schema validator, required per this spec):

| Field | Constraint |
|-------|-----------|
| `domain_knowledge` | List of 4–5 deep expertise areas |
| `skills` | List of 4–5 concrete capabilities |
| `persona` | 2–4 sentence identity description |
| `language` | 2–3 sentence vocabulary/style description |

## Content Layer Company/Product State Schema

The `content.company_state` and `content.product_state` objects are validated by
`BoardroomStateManager` against `_AGENT_PERSPECTIVE_KEYS` and require:

`entity_id`, `entity_name`, `perspective`, `domain_knowledge`, `skills`, `persona`,
`language`, `software_interfaces`, `current_signals`

→ See `src/business_infinity/boardroom.py` → `BoardroomStateManager._AGENT_PERSPECTIVE_KEYS`

## Tool Integration

```bash
# Run all tests
PYTHONPATH=/tmp/aos_mock:src python -m pytest tests/ -q

# Lint boardroom module
PYTHONPATH=/tmp/aos_mock:src python -m pylint src/business_infinity/boardroom.py --disable=C0114,C0115,C0116,E0401
```

## Related Documentation

→ **Spec**: `.github/specs/boardroom-agents.md` — Legend archetypes, domain knowledge, and JSON-LD schema
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`
→ **State files**: `boardroom/state/*.jsonld`
→ **MVP spec**: `.github/specs/mvp.md` — C-suite agent roster
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 1.0 — Initial legend-enrichment skill  
**Last Updated**: 2026-04-03
