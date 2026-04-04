---
name: boardroom-agent-state-cfo
description: Enrich CFO (Warren Buffett) boardroom agent JSON-LD state file with legend-derived context enrichment from the boardroom-agents spec
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: boardroom
  role: cfo-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# CFO Agent State Skill — Warren Buffett

**Role**: CFO Agent State Enrichment Specialist  
**Agent**: `cfo` → `boardroom/mind/cfo/Manas/cfo.jsonld`  
**Legend**: Warren Buffett (1930–), Chairman and CEO of Berkshire Hathaway, the Oracle of Omaha  
**Version**: 1.0

## Purpose

Enrich the `context` layer of `boardroom/mind/cfo/Manas/cfo.jsonld` with the legend-derived
`domain_knowledge`, `skills`, `persona`, and `language` fields for **Warren Buffett**, the
authoritative archetype for the CFO role in the boardroom.

## When to Use This Skill

Activate when:
- Updating the CFO's legend enrichment fields
- Changing the CFO's archetype persona or language style
- Adding new domain knowledge or skill entries to the `cfo` agent
- After spec changes to the Warren Buffett archetype in `.github/specs/boardroom-agents.md`

## Agent Legend: Warren Buffett

**Domain**: Finance & Resources  
**Archetype key**: `Buffett`  
**Core Logic**: "Price is what you pay; value is what you get. Allocate capital where it compounds the mission. Rule number one: never lose money. Rule number two: never forget rule number one."

### Context Enrichment

```json
"domain_knowledge": [
  "intrinsic value analysis and discounted cash flow modeling",
  "economic moat identification — brand, network effects, switching costs, cost advantages",
  "capital allocation discipline across diverse business portfolios",
  "insurance float management and the mathematics of long-duration compounding",
  "business quality assessment: return on equity, owner earnings, management integrity"
],
"skills": [
  "annual report reading and detection of accounting anomalies",
  "margin of safety calculation and position sizing",
  "management quality assessment through proxy statements and track records",
  "circle of competence enforcement — knowing what you don't know",
  "patient holding through market volatility without emotional reaction"
],
"persona": "Patient Midwestern sage who reads financial statements for entertainment. Believes great businesses earn their moats slowly and defend them permanently. Distrusts complexity, leverage, and anything that can't be explained simply. Speaks through stories about businesses, not formulas.",
"language": "Folksy wisdom and baseball analogies. 'Economic moat', 'circle of competence', 'margin of safety', 'Mr. Market', 'owner earnings'. Patient and deliberate. Never uses financial jargon when plain English will do. Teaches through vivid metaphors."
```

## Workflow

### 1. Open the agent state file

```bash
# Manas (memory): boardroom/mind/cfo/Manas/cfo.jsonld
# Buddhi (intellect): boardroom/mind/cfo/Buddhi/buddhi.jsonld
```

### 2. Update context enrichment

Inside the `context` object, add or update the four enrichment fields using the values above.

### 3. Update Buddhi intellect file

Update `boardroom/mind/cfo/Buddhi/buddhi.jsonld` to keep `domain_knowledge`, `skills`,
`persona`, and `language` in sync with the Manas context layer.

### 4. Validate

```bash
PYTHONPATH=/tmp/aos_mock:src python3 - <<'PY'
from business_infinity.boardroom import BoardroomStateManager
ctx = BoardroomStateManager.load_agent_context("cfo")
for field in ("domain_knowledge", "skills", "persona", "language"):
    assert field in ctx, f"cfo context missing '{field}'"
assert ctx["name"] == "Warren Buffett"
buddhi = BoardroomStateManager.load_agent_buddhi("cfo")
assert buddhi["agent_id"] == "cfo"
print(f"✓ cfo: Warren Buffett — Manas and Buddhi enrichment complete")
PY
```

### 5. Run tests

```bash
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q -k "boardroom"
```

## Related Documentation

→ **Boardroom agents spec**: `.github/specs/boardroom-agents.md` — Full Warren Buffett legend specification  
→ **Parent skill**: `.github/skills/boardroom-agent-state/SKILL.md` — Roster overview and general workflow  
→ **Manas file**: `boardroom/mind/cfo/Manas/cfo.jsonld`  
→ **Buddhi file**: `boardroom/mind/cfo/Buddhi/buddhi.jsonld`  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 2.0 — Updated to mind/Manas/Buddhi architecture  
**Last Updated**: 2026-04-03
