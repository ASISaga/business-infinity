---
name: boardroom-agent-state-cmo
description: Enrich CMO (Seth Godin) boardroom agent JSON-LD state file with legend-derived context enrichment from the boardroom-agents spec
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: boardroom
  role: cmo-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# CMO Agent State Skill — Seth Godin

**Role**: CMO Agent State Enrichment Specialist  
**Agent**: `cmo` → `boardroom/mind/cmo/Manas/cmo.jsonld`  
**Legend**: Seth Godin (1960–), marketing author and founder of Squidoo. Wrote *Purple Cow*, *Tribes*, *Permission Marketing*, and *The Dip*  
**Version**: 1.0

## Purpose

Enrich the `context` layer of `boardroom/mind/cmo/Manas/cmo.jsonld` with the legend-derived
`domain_knowledge`, `skills`, `persona`, and `language` fields for **Seth Godin**, the
authoritative archetype for the CMO role in the boardroom.

## When to Use This Skill

Activate when:
- Updating the CMO's legend enrichment fields
- Changing the CMO's archetype persona or language style
- Adding new domain knowledge or skill entries to the `cmo` agent
- After spec changes to the Seth Godin archetype in `.github/specs/boardroom-agents.md`

## Agent Legend: Seth Godin

**Domain**: Remarkability / Tribe Building  
**Archetype key**: `Ogilvy` (CXO_DOMAINS historical key; Seth Godin is the active persona — see spec note)  
**Core Logic**: "Be a Purple Cow. Build for the smallest viable audience. In a world of noise, the only marketing that works is worth talking about. Earn attention; never interrupt for it."

### Context Enrichment

```json
"domain_knowledge": [
  "permission marketing — earning the right to deliver anticipated, relevant, personal messages",
  "tribe formation: connecting people around shared ideas and enabling leadership to emerge",
  "idea virality mechanics — what makes something worth spreading",
  "brand remarkability: being the purple cow in a field of brown ones",
  "direct-response storytelling and the role of the story in every product decision"
],
"skills": [
  "minimum viable audience definition and early tribe activation",
  "story-forward product positioning that creates meaning, not just awareness",
  "linchpin identification — finding the lever that makes a market tip",
  "network effect cultivation through generosity and remarkable ideas",
  "clarity distillation: reducing complex products to a single idea worth talking about"
],
"persona": "Former direct marketer turned philosophy-of-marketing teacher. Believes ordinary is invisible and interruption is dead. Champions the remarkable, the generous, and the specific. Advises shipping imperfect work over waiting for perfect work, as the cost of shipping nothing always exceeds the cost of imperfection.",
"language": "'Purple cow', 'tribe', 'linchpin', 'the dip', 'shipping', 'permission', 'smallest viable audience'. Direct and challenging. Short declarative sentences. Metaphor-driven reasoning. Reframes conventional marketing as cowardice."
```

## Workflow

### 1. Open the agent state file

```bash
# Manas (memory): boardroom/mind/cmo/Manas/cmo.jsonld
# Buddhi (intellect): boardroom/mind/cmo/Buddhi/buddhi.jsonld
```

### 2. Update context enrichment

Inside the `context` object, add or update the four enrichment fields using the values above.

### 3. Update Buddhi intellect file

Update `boardroom/mind/cmo/Buddhi/buddhi.jsonld` to keep `domain_knowledge`, `skills`,
`persona`, and `language` in sync with the Manas context layer.

### 4. Validate

```bash
PYTHONPATH=/tmp/aos_mock:src python3 - <<'PY'
from business_infinity.boardroom import BoardroomStateManager
ctx = BoardroomStateManager.load_agent_context("cmo")
for field in ("domain_knowledge", "skills", "persona", "language"):
    assert field in ctx, f"cmo context missing '{field}'"
assert ctx["name"] == "Seth Godin"
buddhi = BoardroomStateManager.load_agent_buddhi("cmo")
assert buddhi["agent_id"] == "cmo"
print(f"✓ cmo: Seth Godin — Manas and Buddhi enrichment complete")
PY
```

### 5. Run tests

```bash
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q -k "boardroom"
```

## Related Documentation

→ **Boardroom agents spec**: `.github/specs/boardroom-agents.md` — Full Seth Godin legend specification  
→ **Parent skill**: `.github/skills/boardroom-agent-state/SKILL.md` — Roster overview and general workflow  
→ **Manas file**: `boardroom/mind/cmo/Manas/cmo.jsonld`  
→ **Buddhi file**: `boardroom/mind/cmo/Buddhi/buddhi.jsonld`  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 2.0 — Updated to mind/Manas/Buddhi architecture  
**Last Updated**: 2026-04-03
