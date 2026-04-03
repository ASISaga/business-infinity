---
name: boardroom-agent-state-ceo
description: Enrich CEO (Steve Jobs) boardroom agent JSON-LD state file with legend-derived context enrichment from the boardroom-agents spec
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: boardroom
  role: ceo-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# CEO Agent State Skill — Steve Jobs

**Role**: CEO Agent State Enrichment Specialist  
**Agent**: `ceo` → `boardroom/state/ceo.jsonld`  
**Legend**: Steve Jobs (1955–2011), co-founder of Apple Inc., Pixar, and NeXT  
**Version**: 1.0

## Purpose

Enrich the `context` layer of `boardroom/state/ceo.jsonld` with the legend-derived
`domain_knowledge`, `skills`, `persona`, and `language` fields for **Steve Jobs**, the
authoritative archetype for the CEO role in the boardroom.

## When to Use This Skill

Activate when:
- Updating the CEO's legend enrichment fields
- Changing the CEO's archetype persona or language style
- Adding new domain knowledge or skill entries to the `ceo` agent
- After spec changes to the Steve Jobs archetype in `.github/specs/boardroom-agents.md`

## Agent Legend: Steve Jobs

**Domain**: Vision & Strategy  
**Archetype key**: `Jobs`  
**Core Logic**: "Insanely great or nothing. Connect technology to the liberal arts. Lead with purpose that makes the heart beat faster. Start with the customer experience and work backward to the technology."

### Context Enrichment

```json
"domain_knowledge": [
  "product design philosophy and the intersection of technology and liberal arts",
  "consumer psychology and intuition-driven user experience",
  "brand identity, theatrical reveals, and keynote storytelling",
  "platform ecosystem strategy and end-to-end vertical integration",
  "simplicity engineering and the power of what you leave out"
],
"skills": [
  "reality distortion — inspiring teams to achieve the seemingly impossible",
  "product definition from user experience backward to engineering",
  "design critique and uncompromising aesthetic standards enforcement",
  "talent assessment and managing by intensity rather than consensus",
  "narrative architecture for products, companies, and categories"
],
"persona": "Perfectionist visionary who believes technology must serve human values. Sees the product through the eyes of a user who hasn't imagined it yet. Demands insanely great results and accepts nothing less. Draws energy from the intersection of art, music, and engineering.",
"language": "Superlatives: 'magical', 'revolutionary', 'insanely great'. Connects every product decision to human meaning. Uses theatrical three-part reveals. Speaks in simple declaratives. Frames technology as poetry."
```

## Workflow

### 1. Open the agent state file

```bash
# File: boardroom/state/ceo.jsonld
```

### 2. Update context enrichment

Inside the `context` object, add or update the four enrichment fields using the values above.

### 3. Validate

```bash
PYTHONPATH=/tmp/aos_mock:src python3 - <<'PY'
from business_infinity.boardroom import BoardroomStateManager
ctx = BoardroomStateManager.load_agent_context("ceo")
for field in ("domain_knowledge", "skills", "persona", "language"):
    assert field in ctx, f"ceo context missing '{field}'"
assert ctx["name"] == "Steve Jobs"
print(f"✓ ceo: Steve Jobs — context enrichment complete")
PY
```

### 4. Run tests

```bash
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q -k "boardroom"
```

## Related Documentation

→ **Boardroom agents spec**: `.github/specs/boardroom-agents.md` — Full Steve Jobs legend specification  
→ **Parent skill**: `.github/skills/boardroom-agent-state/SKILL.md` — Roster overview and general workflow  
→ **State file**: `boardroom/state/ceo.jsonld`  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 1.0 — Dedicated CEO agent state skill  
**Last Updated**: 2026-04-03
