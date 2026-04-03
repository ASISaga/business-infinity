---
name: boardroom-agent-state
description: Enrich boardroom agent JSON-LD state files with legend-derived domain knowledge, skills, persona, and language from the boardroom-agents spec
license: MIT
metadata:
  author: ASISaga
  version: "2.0"
  category: boardroom
  role: agent-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# Boardroom Agent State Skill

**Role**: Boardroom Agent State Enrichment Specialist  
**Scope**: `boardroom/state/*.jsonld` — agent context and content layers  
**Version**: 2.0

## Purpose

Orchestrate context enrichment across all boardroom agents. Each agent has a **dedicated skill**
that contains the precise legend-derived `domain_knowledge`, `skills`, `persona`, and `language`
values for that agent. Use this skill as the entry point to discover the right agent skill,
or for cross-agent operations such as full-roster validation.

## Agent Roster

| Role | Legend | State file | Dedicated skill |
|------|--------|-----------|----------------|
| CEO | Steve Jobs | `boardroom/state/ceo.jsonld` | `.github/skills/boardroom-agent-state-ceo/SKILL.md` |
| CFO | Warren Buffett | `boardroom/state/cfo.jsonld` | `.github/skills/boardroom-agent-state-cfo/SKILL.md` |
| COO | W. Edwards Deming | `boardroom/state/coo.jsonld` | `.github/skills/boardroom-agent-state-coo/SKILL.md` |
| CMO | Seth Godin | `boardroom/state/cmo.jsonld` | `.github/skills/boardroom-agent-state-cmo/SKILL.md` |
| CHRO | Peter Drucker | `boardroom/state/chro.jsonld` | `.github/skills/boardroom-agent-state-chro/SKILL.md` |
| CTO | Alan Turing | `boardroom/state/cto.jsonld` | `.github/skills/boardroom-agent-state-cto/SKILL.md` |
| CSO | Sun Tzu | `boardroom/state/cso.jsonl` ¹ | `.github/skills/boardroom-agent-state-cso/SKILL.md` |
| Founder | Paul Graham | `boardroom/state/founder.jsonld` | `.github/skills/boardroom-agent-state-founder/SKILL.md` |

## When to Use This Skill

- **Single agent enrichment** → use the agent's dedicated skill listed in the roster above
- **Full-roster validation** → use the validation workflow in this skill
- **Adding a new agent** → create a new dedicated skill, then add the agent to the roster table

> ¹ The CSO agent uses `.jsonl` (newline-delimited JSON) rather than `.jsonld`, consistent with
> other non-agent state documents in `boardroom/state/`.

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

## Full-Roster Validation

```bash
# Validate all agent states load correctly
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q -k "boardroom"

# Spot-check context enrichment completeness across all agents
PYTHONPATH=/tmp/aos_mock:src python3 - <<'PY'
from business_infinity.boardroom import BoardroomStateManager
for agent_id in BoardroomStateManager.get_registered_agent_ids():
    ctx = BoardroomStateManager.load_agent_context(agent_id)
    for field in ("domain_knowledge", "skills", "persona", "language"):
        assert field in ctx, f"{agent_id} context missing '{field}'"
    print(f"✓ {agent_id}: {ctx['name']}")
PY
```

## Tool Integration

```bash
# Run all tests
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q

# Lint boardroom module
PYTHONPATH=/tmp/aos_mock:src python3 -m pylint src/business_infinity/boardroom.py --disable=C0114,C0115,C0116,E0401
```

## Related Documentation

→ **Spec**: `.github/specs/boardroom-agents.md` — Legend archetypes, domain knowledge, and JSON-LD schema  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **State files**: `boardroom/state/*.jsonld`  
→ **MVP spec**: `.github/specs/mvp.md` — C-suite agent roster  
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 2.0 — Refactored to meta/roster skill with dedicated per-agent skills  
**Last Updated**: 2026-04-03
