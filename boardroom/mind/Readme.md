# Boardroom Mind

The `boardroom/mind/` directory holds the **initial mind** of the Business Infinity boardroom — both individual members and the collective. It is the first-principles knowledge and memory substrate that is hydrated into each agent at initialisation and thereafter maintained by the agent itself.

> **Manas** (Sanskrit: मनस्) — memory; the working, evolving mind.  
> **Buddhi** (Sanskrit: बुद्धि) — intellect; the stable, discriminating intelligence.

---

## Architecture

Each of the eight boardroom members has a subdirectory under `boardroom/mind/{agent_id}/`:

```
boardroom/mind/
├── {agent_id}/
│   ├── Manas/                        # Memory — the agent's JSON-LD state file
│   │   ├── {agent_id}.jsonld         # Full agent state (context + content layers)
│   │   ├── context/                  # Immutable perspective on each entity
│   │   │   ├── company.jsonld        # Agent's fixed knowledge of ASI Saga
│   │   │   └── business-infinity.jsonld  # Agent's fixed knowledge of the product
│   │   └── content/                  # Mutable perspective on each entity
│   │       ├── company.jsonld        # Agent's current signals about ASI Saga
│   │       └── business-infinity.jsonld  # Agent's current signals about the product
│   └── Buddhi/                       # Intellect — legend-derived domain layer
│       ├── buddhi.jsonld             # Legend's domain_knowledge, skills, persona, language
│       └── action-plan.jsonld        # Agent's action plan toward the initial company purpose
└── collective/                       # Shared boardroom mind (no individual owner)
    ├── boardroom.jsonld              # Collective consciousness, resonance ledger, directives
    ├── company.jsonld                # ASI Saga entity — full enriched manifest
    ├── business-infinity.jsonld      # Business Infinity product — JSONL records
    ├── environment.jsonl             # Infrastructure manifest (Azure / GitHub)
    ├── mvp.jsonl                     # MVP feature and milestone records
    └── orchestration.jsonld          # Orchestration session configuration
```

### Manas layer (memory)

The Manas file (`{agent_id}.jsonld`) is the live state of the agent. It has two layers:

| Layer | Mutability | Purpose |
|-------|------------|---------|
| `context` | Immutable | Identity, mandate, domain knowledge, skills, persona, language — the agent's constitution |
| `content` | Mutable | Active focus, working memory, spontaneous intent, per-entity perspective state |

The `context/` and `content/` subdirectories hold the agent's perspective on each shared entity (ASI Saga and Business Infinity) in the same two-layer split.

### Buddhi layer (intellect)

`buddhi.jsonld` encodes the legend's domain wisdom as a standalone intellect document. It is the seed used to hydrate the agent and is loaded independently by `BoardroomStateManager.load_agent_buddhi(agent_id)`.

`action-plan.jsonld` captures the agent's action steps toward the initial purpose of the company: development of the Business Infinity MVP. Each step is expressed from the legend's own perspective, persona, and language.

---

## Agent Roster

| Agent | Legend | Domain | `@id` |
|-------|--------|--------|-------|
| CEO | Steve Jobs | Vision & Strategy | `agent:ceo` |
| CFO | Warren Buffett | Finance & Resources | `agent:cfo` |
| COO | W. Edwards Deming | Operations & Workflow | `agent:coo` |
| CMO | Seth Godin | Remarkability / Tribe Building | `agent:sg_cmo` |
| CHRO | Peter Drucker | People & Culture | `agent:chro` |
| CTO | Alan Turing | Technology & Innovation | `agent:sj_cto` |
| CSO | Sun Tzu | Strategy & Competitive Intelligence | `agent:cso_strategy` |
| Founder | Paul Graham | Prioritization / Survival / Shipping | `agent:pg_founder` |

> **CTO `@id` note**: `agent:sj_cto` originally referenced Steve Jobs (the first CTO persona). It is preserved for backward compatibility with governance references. `context.name` is the authoritative field — it reads `Alan Turing`.

---

## Collective Mind

The `collective/` subdirectory holds the shared boardroom consciousness — state that belongs to the whole rather than to any individual agent:

| File | Description |
|------|-------------|
| `boardroom.jsonld` | Active session, resonance ledger, composite score, and directives |
| `company.jsonld` | ASI Saga entity manifest with full context and content enrichment |
| `business-infinity.jsonld` | Business Infinity product records (JSONL, 5 records) |
| `environment.jsonl` | Azure / GitHub infrastructure manifest |
| `mvp.jsonl` | MVP phase, configuration, and milestone records |
| `orchestration.jsonld` | Orchestration session configuration and resonance protocol |

---

## Initial Purpose

The initial purpose of **ASI Saga** is the development of the MVP of **Business Infinity** — an autonomous C-suite boardroom that governs business decisions through purpose-driven debate, resonance scoring, and perpetual orchestration. Every action-plan in every agent's Buddhi is anchored to this purpose.

---

## References

→ **Agent spec**: `.github/specs/boardroom-agents.md` — legend archetypes, schemas, validation  
→ **Entity spec**: `.github/specs/boardroom-entities.md` — company and product enrichment  
→ **State manager**: `src/business_infinity/boardroom.py` → `BoardroomStateManager`  
→ **Skill (roster)**: `.github/skills/boardroom-agent-state/SKILL.md`  
→ **Repository spec**: `.github/specs/repository.md`

