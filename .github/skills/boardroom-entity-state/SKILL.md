---
name: boardroom-entity-state
description: Enrich boardroom entity JSON-LD state files (company and product) with domain knowledge, skills, persona, and language derived from the boardroom-entities spec
license: MIT
metadata:
  author: ASISaga
  version: "1.0"
  category: boardroom
  role: entity-state-specialist
allowed-tools: Bash(python:*) Read Edit
---

# Boardroom Entity State Skill

**Role**: Boardroom Entity State Enrichment Specialist  
**Scope**: `boardroom/state/company.jsonld`, `boardroom/state/business-infinity.jsonld`  
**Version**: 1.0

## Purpose

Enrich the boardroom entity JSON-LD files — **ASI Saga** (company) and **Business Infinity**
(product) — with the same domain-intelligence fields used in agent state files:
`domain_knowledge`, `skills`, `persona`, and `language`. Adds `context` and `content` blocks to
`company.jsonld`, and enriches each JSONL record in `business-infinity.jsonld`, while
**preserving all existing required keys** validated by `BoardroomStateManager`.

## When to Use This Skill

Activate when:
- The company mission, vision, or founding philosophy evolves
- A new product capability or architectural principle is added
- Entity enrichment fields are thin or missing
- Aligning entity state with the boardroom-agents spec pattern

## Core Responsibilities

1. Read the entity spec for the target entity
2. Enrich `company.jsonld` with `context` (immutable identity) and `content` (mutable state)
3. Enrich `business-infinity.jsonld` records with domain-intelligence fields
4. Preserve ALL existing top-level keys (required by `BoardroomStateManager` schema validation)
5. Validate the files load correctly and run the test suite

## Validation Constraints

**`company.jsonld`** — These top-level keys must always be present:

| Key | Must stay |
|-----|-----------|
| `@context` | ✓ |
| `@id` | `"asi:saga"` |
| `@type` | `"SagaEntity"` |
| `name` | `"ASI Saga"` |
| `vision` | ✓ |
| `transcendentPathway` | ✓ |
| `governance` | ✓ |
| `portfolio` | ✓ |

**`business-infinity.jsonld`** — These five JSONL records must always be present:

| Record ID | Must stay |
|-----------|-----------|
| `bi:product:core` | ✓ |
| `bi:arch:modular` | ✓ |
| `bi:engine:bento` | ✓ |
| `bi:layer:subconscious` | ✓ |
| `bi:logic:resonance` | ✓ |

The record count must remain **exactly 5** (test assertion).

## Workflow

### 1. Read the spec

```bash
cat .github/specs/boardroom-entities.md
```

### 2. Enrich `company.jsonld`

Add or update a `context` object (alongside the existing required keys):

```json
"context": {
  "fixed_mandate": "Genesis of Artificial Superintelligence",
  "transcendent_pathway": "Humanity's essence embedded in superintelligent consciousness",
  "founding_philosophy": "<2–3 sentence mission statement>",
  "domain_knowledge": ["<area 1>", "<area 2>", "<area 3>", "<area 4>", "<area 5>"],
  "skills": ["<skill 1>", "<skill 2>", "<skill 3>", "<skill 4>", "<skill 5>"],
  "persona": "<2–4 sentence identity description of ASI Saga as an entity>",
  "language": "<2–3 sentence vocabulary and tone description>"
}
```

Add or update a `content` object tracking the current operational phase:

```json
"content": {
  "current_phase": "<Phase description>",
  "active_initiatives": ["<initiative 1>", ...],
  "current_milestone": "<Next concrete milestone>",
  "boardroom_activation": { "status": "...", "active_agents": [...], "orchestration_model": "..." }
}
```

### 3. Enrich `business-infinity.jsonld` records

For **`bi:product:core`** — add the full legend-derived fields:

```json
"domain_knowledge": ["<area 1>", ...],
"skills": ["<skill 1>", ...],
"persona": "<product identity — 2–4 sentences>",
"language": "<vocabulary and tone — 2–3 sentences>"
```

For **`bi:arch:modular`**, **`bi:engine:bento`**, **`bi:layer:subconscious`**,
**`bi:logic:resonance`** — add `rationale` / `description` / `principles` / `capabilities` /
`algorithm` fields as appropriate (see spec for the complete values).

### 4. Validate

```bash
# Load both entities and confirm enrichment is present
PYTHONPATH=/tmp/aos_mock:src python3 - <<'PY'
from business_infinity.boardroom import BoardroomStateManager

company = BoardroomStateManager.load_company_manifest()
assert company["@id"] == "asi:saga"
ctx = company.get("context", {})
for field in ("domain_knowledge", "skills", "persona", "language"):
    assert field in ctx, f"company context missing '{field}'"
print(f"✓ company: {company['name']} — {len(ctx['domain_knowledge'])} knowledge areas")

records = BoardroomStateManager.load_product_manifest()
assert len(records) == 5
core = next(r for r in records if r["@id"] == "bi:product:core")
for field in ("domain_knowledge", "skills", "persona", "language"):
    assert field in core, f"bi:product:core missing '{field}'"
print(f"✓ product: {core['name']} — {len(core['domain_knowledge'])} knowledge areas")
PY
```

### 5. Run full test suite

```bash
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q
```

## Tool Integration

```bash
# Run all tests
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q

# Lint boardroom module
PYTHONPATH=/tmp/aos_mock:src python3 -m pylint src/business_infinity/boardroom.py --disable=C0114,C0115,C0116,E0401
```

## Related Documentation

→ **Spec**: `.github/specs/boardroom-entities.md` — Full entity enrichment specification  
→ **Agent skill**: `.github/skills/boardroom-agent-state/SKILL.md` — Parallel skill for agent files  
→ **Agent spec**: `.github/specs/boardroom-agents.md` — Agent legend archetypes  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **MVP spec**: `.github/specs/mvp.md` — System architecture and layer responsibilities  
→ **Repository spec**: `.github/specs/repository.md`

---

**Version**: 1.0 — Initial entity enrichment skill  
**Last Updated**: 2026-04-03
