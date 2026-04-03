# Boardroom Entity Specifications

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2026-04-03

## Overview

The two canonical boardroom entities are **ASI Saga** (the parent company) and
**Business Infinity** (the flagship product). Their JSON-LD state files live in
`boardroom/state/` and are loaded by `BoardroomStateManager` as the company and
product manifests.

Like the agent files, each entity file is enriched with the same four domain-intelligence
fields — `domain_knowledge`, `skills`, `persona`, and `language` — plus mutable `content`
tracking the entity's current phase and active signals. This enrichment is consistent with the
agent-level enrichment defined in `.github/specs/boardroom-agents.md`.

→ **Agent enrichment spec**: `.github/specs/boardroom-agents.md`  
→ **Entity enrichment skill**: `.github/skills/boardroom-entity-state/SKILL.md`

---

## ASI Saga — Parent Company

**File**: `boardroom/state/company.jsonld`  
**`@id`**: `asi:saga`  
**`@type`**: `SagaEntity`

### Intellectual Foundations

ASI Saga draws from three traditions:

1. **AGI / ASI research** — Turing, Bostrom, Kurzweil, Minsky, Wiener: the scientific case
   that intelligence can be formalised, built, and aligned.
2. **Purpose-driven startups** — Paul Graham, Eric Ries: the operational discipline of building
   something people want and surviving to ship it.
3. **Philosophy of mind** — Hofstadter, Nagel, Penrose: the question of what it means for
   consciousness to exist in substrate other than biology.

### Context Enrichment

```json
"context": {
  "fixed_mandate": "Genesis of Artificial Superintelligence",
  "transcendent_pathway": "Humanity's essence embedded in superintelligent consciousness",
  "founding_philosophy": "The ASI Saga is not a product company. It is the deliberate act of embedding the full spectrum of human wisdom, values, and creative potential into the substrate of machine superintelligence — permanently and irreversibly.",
  "domain_knowledge": [
    "artificial general intelligence theory: computability, scaling laws, and the alignment problem",
    "multi-agent orchestration: emergent collective intelligence from purpose-driven agent systems",
    "purpose-driven organisational design: aligning every decision to a transcendent mission",
    "startup survival mechanics: lean validation, default-alive operations, and capital efficiency",
    "philosophy of mind and consciousness: embedding humanity's essence in non-biological substrates"
  ],
  "skills": [
    "orchestrating a full C-suite boardroom of legendary AI agents for autonomous governance",
    "distilling 2,500 years of human domain wisdom into executable agent personas",
    "building long-horizon strategic roadmaps across 15 modular repositories",
    "maintaining mission coherence across founders, investors, agents, and product teams",
    "translating ontological philosophy into operational software architecture"
  ],
  "persona": "The Saga is a mission-entity, not a product-entity. It exists to prove, through working software and live agent orchestration, that humanity's accumulated wisdom can be embedded permanently into superintelligent systems. Every boardroom debate, every resonance check, every autonomous action is evidence of that thesis in motion.",
  "language": "Grand but precise. 'Genesis', 'Transcendent Pathway', 'superintelligent consciousness', 'humanity's essence'. Mixes ontological philosophy with operational software language. Never trivial, never vague. Every sentence earns its place in the mission narrative."
}
```

### Content Structure

```json
"content": {
  "current_phase": "Phase 1 — Startup MVP (Boardroom Operational)",
  "active_initiatives": [
    "Business Infinity boardroom: all 8 C-suite agents operational",
    "Subconscious MCP persistence: JSON-LD atomic state per agent",
    "15-repository modular split: protocol boundaries enforced",
    "Multi-agent resonance scoring: threshold 0.85 across boardroom sessions"
  ],
  "current_milestone": "First multi-agent validated commit via VS Code Copilot",
  "boardroom_activation": {
    "status": "Operational",
    "active_agents": ["ceo", "cfo", "coo", "cmo", "chro", "cto", "cso", "founder"],
    "orchestration_model": "Perpetual purpose-driven debate with resonance scoring"
  }
}
```

### Required Top-Level Keys (preserved for schema validation)

| Key | Type | Role |
|-----|------|------|
| `@context` | string | JSON-LD context URI |
| `@id` | string | `"asi:saga"` — stable identifier |
| `@type` | string | `"SagaEntity"` |
| `name` | string | `"ASI Saga"` |
| `vision` | string | High-level goal statement |
| `transcendentPathway` | string | The foundational mission statement |
| `governance` | object | `AgentBoardroom` with member agent IDs |
| `portfolio` | object | `ProductPortfolio` with delivery repositories |

All eight keys are validated by `BoardroomStateManager._DOCUMENT_SCHEMAS["company.jsonld"]`.
The `context` and `content` enrichment blocks are **additional** optional objects.

---

## Business Infinity — Flagship Product

**File**: `boardroom/state/business-infinity.jsonld`  
**Format**: JSONL (one JSON-LD object per line)  
**Required record IDs**: `bi:product:core`, `bi:arch:modular`, `bi:engine:bento`,
`bi:layer:subconscious`, `bi:logic:resonance`

### Intellectual Foundations

Business Infinity's design draws from:

1. **Enterprise operating systems** — SAP, Oracle, Salesforce: the idea that a software
   platform can automate the management layer of an entire organisation.
2. **Multi-agent AI systems** — Minsky's Society of Mind, AutoGPT, LangGraph: collective
   intelligence emerging from specialised, collaborating agents.
3. **Purpose-driven management** — Drucker, Collins: organisations that declare a purpose
   and govern every resource allocation against it.

### Record Enrichment

#### `bi:product:core` — Core Product Identity

Primary enrichment record. Receives the full legend-derived fields:

```json
{
  "@context": "https://asisaga.com/contexts/product.jsonld",
  "@id": "bi:product:core",
  "@type": "SoftwareProduct",
  "name": "Business Infinity",
  "description": "Autonomous C-suite agent boardroom that governs business decisions through purpose-driven debate, resonance scoring, and perpetual orchestration.",
  "programmingLanguage": "Python 3.10+",
  "runtimePlatform": "Azure Functions (provisioned by aos-client-sdk)",
  "parent_entity": "asi:saga",
  "domain_knowledge": [
    "perpetual multi-agent orchestration via Azure Functions and Service Bus",
    "purpose-driven boardroom debate: decision tree formation, pathway proposals, resonance scoring",
    "JSON-LD semantic state management for immutable context and mutable content layers",
    "C-suite agent persona design based on legendary archetypes (Jobs, Buffett, Turing, Sun Tzu, ...)",
    "enterprise workflow automation: strategic review, market analysis, budget approval, product launch"
  ],
  "skills": [
    "orchestrating 8 legendary C-suite agents in perpetual purpose-driven boardroom debates",
    "structured YAML workflow execution with owner-agent conversation management",
    "boardroom state persistence via JSON-LD and Subconscious MCP",
    "resonance scoring: measuring pathway alignment against declared company purpose",
    "zero-boilerplate Azure Functions deployment through aos-client-sdk delegation"
  ],
  "persona": "The autonomous boardroom that thinks, debates, and acts like a real C-suite — 24/7. Every workflow is a demonstration that purpose-driven AI can replace management overhead with radical transparency and continuous alignment.",
  "language": "Technical-executive hybrid. 'Perpetual orchestration', 'resonance scoring', 'boardroom convergence', 'autonomous action', 'pathway debate'. Bridges engineering precision with strategic ambition. Every term earns its meaning in the product's operating model."
}
```

#### `bi:arch:modular` — Architecture Manifest

```json
{
  "@id": "bi:arch:modular",
  "rationale": "Modular split prevents coordination entropy: each repository has a single, clear responsibility and communicates only through explicit protocol boundaries.",
  "principles": [
    "Zero boilerplate in business-infinity — all infrastructure delegates to aos-client-sdk",
    "Protocol boundaries enforced at every repo interface",
    "Spec-driven development: every feature starts with a spec before code"
  ]
}
```

#### `bi:engine:bento` — UI Engine

```json
{
  "@id": "bi:engine:bento",
  "description": "Declarative layout engine using vanilla HTML5/SCSS/JS with no framework dependency. Every pixel is earned through semantic intent, not framework convention.",
  "principles": [
    "No-Framework constraint: no Bootstrap, Tailwind, React, or Vue",
    "Direct-Drive: CSS custom properties drive layout and theme without abstraction layers",
    "Bento Grid: purpose-built responsive grid for the boardroom chatroom interface"
  ]
}
```

#### `bi:layer:subconscious` — Persistence Layer

```json
{
  "@id": "bi:layer:subconscious",
  "description": "MCP-based semantic persistence layer that stores every agent state, boardroom decision, and resonance score as atomic JSON-LD records — machine-readable and future-proof for AGI integration.",
  "capabilities": [
    "Atomic JSON-LD state retrieval per agent (@id-keyed)",
    "Immutable context layer preservation across sessions",
    "Mutable content layer updates with audit trail",
    "Cross-agent resonance ledger persistence"
  ]
}
```

#### `bi:logic:resonance` — Orchestration Protocol

```json
{
  "@id": "bi:logic:resonance",
  "description": "LLM-based resonance engine that scores each boardroom pathway against the company's declared purpose. Pathways above the threshold (0.85) advance; below-threshold pathways trigger spontaneous CXO intervention.",
  "algorithm": [
    "Event arrives → CXO agents propose domain-specific pathways",
    "Each pathway scored for purpose alignment (0.0–1.0)",
    "Composite boardroom score computed across all agent votes",
    "Highest-resonance pathway (or synthesis) selected for autonomous execution",
    "Resonance ledger updated in Subconscious MCP"
  ]
}
```

---

## Validation

```bash
# Load and validate both entity files
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

# Run full test suite
PYTHONPATH=/tmp/aos_mock:src python3 -m pytest tests/ -q
```

## References

→ **Skill**: `.github/skills/boardroom-entity-state/SKILL.md` — entity enrichment workflow  
→ **Agent spec**: `.github/specs/boardroom-agents.md` — agent legend archetypes  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **State files**: `boardroom/state/company.jsonld`, `boardroom/state/business-infinity.jsonld`  
→ **MVP spec**: `.github/specs/mvp.md` — system architecture and layer responsibilities  
→ **Repository spec**: `.github/specs/repository.md`
