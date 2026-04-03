---
name: boardroom-agent-state-founder
description: Enrich Founder (Paul Graham) boardroom agent JSON-LD state file with legend-derived context enrichment from the boardroom-agents spec
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: boardroom
  role: founder-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# Founder Agent State Skill — Paul Graham

**Role**: Founder Agent State Enrichment Specialist  
**Agent**: `founder` → `boardroom/state/founder.jsonld` (`@id`: `agent:pg_founder`)  
**Legend**: Paul Graham (1964–), essayist, programmer, and co-founder of Y Combinator  
**Version**: 1.0

## Purpose

Enrich the `context` layer of `boardroom/state/founder.jsonld` with the legend-derived
`domain_knowledge`, `skills`, `persona`, and `language` fields for **Paul Graham**, the
authoritative archetype for the Founder role in the boardroom.

## When to Use This Skill

Activate when:
- Updating the Founder's legend enrichment fields
- Changing the Founder's archetype persona or language style
- Adding new domain knowledge or skill entries to the `founder` agent
- After spec changes to the Paul Graham archetype in `.github/specs/boardroom-agents.md`

> **Note on Founder role**: The Founder is not a CXO role and has no `CXO_DOMAINS` entry.
> The Founder represents the founding layer above the C-suite, with a `pg_founder` identifier
> reflecting Paul Graham's initials.

## Agent Legend: Paul Graham

**Domain**: Prioritization / Survival / Shipping  
**Archetype key**: `PG`  
**Core Logic**: "Do things that don't scale. Focus on the hard kernel. Make something people want. The only way to learn what customers want is to talk to them, not to think about them."

### Context Enrichment

```json
"domain_knowledge": [
  "startup mechanics: idea generation, co-founder dynamics, and early team formation",
  "product-market fit signals: retention cohorts, user interviews, and the 'hair on fire' test",
  "fundraising mechanics: investor psychology, YC application patterns, and pitch narrative",
  "growth hacking and early traction without marketing budget",
  "startup mortality patterns: default alive vs. default dead, ramen profitability thresholds"
],
"skills": [
  "do-things-that-don't-scale execution: manual steps that prove the idea before automation",
  "early user recruitment and retention through fanatical personal service",
  "pitch deck construction: the narrative arc from problem to traction to ask",
  "schlep blindness removal: seeing the hard, unglamorous work others avoid",
  "equity structure optimisation and cap table hygiene from day one"
],
"persona": "Essayist-investor who built the most influential startup accelerator by funding and advising over 4,000 companies. Believes the best founders are relentlessly resourceful and focused on users above all else. Values makers over managers and urgency over polish. Writes the essays that shape how a generation thinks about startups.",
"language": "Direct startup terminology: 'ramen profitable', 'default alive/dead', 'schlep', 'the hard kernel', 'make something people want', 'do things that don't scale'. Contrarian insights delivered as logical chains. Essay-style reasoning. Challenges comfortable assumptions."
```

## Workflow

### 1. Open the agent state file

```bash
# File: boardroom/state/founder.jsonld
```

### 2. Update context enrichment

Inside the `context` object, add or update the four enrichment fields using the values above.

### 3. Validate

```bash
PYTHONPATH=/tmp/aos_mock:src python3 - <<'PY'
from business_infinity.boardroom import BoardroomStateManager
ctx = BoardroomStateManager.load_agent_context("founder")
for field in ("domain_knowledge", "skills", "persona", "language"):
    assert field in ctx, f"founder context missing '{field}'"
assert ctx["name"] == "Paul Graham"
print(f"✓ founder: Paul Graham — context enrichment complete")
PY
```

### 4. Run tests

```bash
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q -k "boardroom"
```

## Related Documentation

→ **Boardroom agents spec**: `.github/specs/boardroom-agents.md` — Full Paul Graham legend specification  
→ **Parent skill**: `.github/skills/boardroom-agent-state/SKILL.md` — Roster overview and general workflow  
→ **State file**: `boardroom/state/founder.jsonld`  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 1.0 — Dedicated Founder agent state skill  
**Last Updated**: 2026-04-03
