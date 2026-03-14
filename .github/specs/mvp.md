# MVP Specification — Business Infinity

**Version**: 2.0.0
**Status**: Active
**Last Updated**: 2026-03-14

## Overview

Business Infinity is a three-layer system: a human-facing command centre, an autonomous boardroom powered by C-suite agents, and the Agent Operating System that provides memory, tools, and execution infrastructure.

---

## Layer 1: The Command Center (The Interface)

**Tech Stack**: VS Code + GitHub Copilot (Agent Mode) + MCP Client

**Role**: The "Observation Deck." It allows the human founder to see what the autonomous boardroom is doing in real-time.

**Functionality**:

- Connects to the Layer 3 MCP Server via a remote URL.
- Exposes "Legendary" strategic insights directly in the IDE.
- Provides "One-Click Approval" for code or infrastructure changes proposed by the AI Boardroom.

---

## Layer 2: Business Infinity (The Brain)

**Tech Stack**: `aos-client-sdk` (Python) + Azure Functions

**Role**: The "Autonomous Boardroom." It operates 24/7 to solve business problems, debate strategy, and drive autonomous action across the organisation.

**Repository**: [`ASISaga/business-infinity`](https://github.com/ASISaga/business-infinity)

### Boardroom Agents

Business Infinity orchestrates the full `/boardroom` agent roster, composed of two tiers:

#### C-Suite Agents (`/boardroom/c-suite/`)

| Agent | Archetype | Domain | Pathway Type |
|-------|-----------|--------|--------------|
| CEO | Jobs | Vision & Strategy | Narrative |
| CFO | Buffett | Finance & Resources | Resource Allocation |
| COO | Deming | Operations & Workflow | Workflow |
| CMO | Ogilvy | Market & Communication | Communication |
| CHRO | Drucker | People & Culture | People-Centric |
| CTO | Turing | Technology & Innovation | Technology |
| CSO | Sun Tzu | Strategy & Competitive Intelligence | Strategic |

Each C-suite agent is a purpose-driven PurposeDrivenAgent from the Agent Operating System, defined in its own submodule under `/boardroom/c-suite/`.

#### Boardroom Stakeholder Agents (`/boardroom/`)

| Agent | Role |
|-------|------|
| BusinessAgent | Base business intelligence agent |
| Founder | Long-term vision and founding purpose |
| Investor | Capital allocation and ROI perspective |
| Mentor | Guidance, governance, and accountability |

### Boardroom Debate Philosophy

Business Infinity implements a **purpose-driven decision tree debate** where each CXO agent proposes domain-specific pathways in response to a business event. The debate proceeds through:

1. **Event Trigger** — A business signal arrives (ERP, CRM, market, GitHub commit, CRON timer).
2. **Spontaneous Leadership** — Relevant CXOs step forward and propose pathways from their domain expertise.
3. **Decision Tree Formation** — Each CXO proposes a characteristic pathway type (see table above).
4. **Cross-Functional Debate** — Agents challenge and refine competing pathways.
5. **Resonance Scoring** — Each pathway is scored for alignment with the company's stated purpose.
6. **Boardroom Convergence** — The highest-resonance pathway (or synthesis of pathways) is selected.
7. **Autonomous Execution** — The chosen action is enacted across connected business systems.

### Workflows

Business Infinity exposes the following Azure Functions workflows via `@app.workflow`:

| Workflow | Agents | Description |
|----------|--------|-------------|
| `boardroom-debate` | All C-suite | Full purpose-driven decision tree debate on a business event |
| `strategic-review` | All C-suite | Perpetual strategic alignment and cross-functional improvement |
| `market-analysis` | CMO + CEO | Continuous market monitoring and competitive intelligence |
| `budget-approval` | CEO + CFO | Budget governance and fiscal decision oversight |
| `knowledge-search` | — | Search the AOS knowledge base |
| `risk-register` | — | Register a new organisational risk |
| `risk-assess` | — | Update likelihood and impact for a registered risk |
| `log-decision` | — | Record a boardroom decision in the immutable audit trail |
| `covenant-create` | — | Create a formal business covenant |
| `ask-agent` | Any | Send a synchronous question to a named boardroom agent |
| `mcp-orchestration` | CEO + CMO | C-suite orchestration with per-agent MCP server assignment |

**Trigger**: HTTP webhooks (e.g., triggered by a GitHub commit, CRM event, ERP signal) or CRON timer.

### Orchestration Model

All orchestrations are **perpetual and purpose-driven** — agents work toward the declared purpose indefinitely. There is no finite completion.

```python
status = await request.client.start_orchestration(
    agent_ids=["ceo", "cfo", "coo", "cmo", "chro", "cto", "cso"],
    purpose=BOARDROOM_DEBATE_PURPOSE,
    purpose_scope=BOARDROOM_DEBATE_SCOPE,
    context={"event": "...", "company_purpose": "..."},
)
```

### Design Principles

- **Zero boilerplate** — No Azure Functions scaffolding in this layer; `aos-client-sdk` handles all infrastructure.
- **Purpose-driven** — Orchestrations declare *why*, not *how*; AOS handles routing and execution.
- **Business-only** — Only business logic lives here; no agent internals, no infrastructure code.
- **SDK-delegated** — Azure Functions, Service Bus, auth, and health checks are all provisioned by the SDK.

---

## Layer 3: The Agent Operating System (Memory & Action)

**Tech Stack**: `aos-dispatcher` + `aos-realm-of-agents` + `aos-kernel`

**Role**: The "Memory and Action Layer." It provides the boardroom with tools to remember, reason, and act on business systems.

**Functionality**:

- **MCP Server** — Exposes tools to boardroom agents: ERP search, CRM queries, analytics, knowledge base, risk registry, decision audit trail, business covenants.
- **Agent Catalog** — `aos-realm-of-agents` hosts the live C-suite agents and BoardAgent implementations.
- **Orchestration Engine** — `aos-dispatcher` manages perpetual orchestrations, resonance scoring, and boardroom convergence.
- **OS Kernel** — `aos-kernel` provides messaging, storage, monitoring, and agent lifecycle management.

---

## References

→ **Philosophy**: `docs/philosophy.md` — Full boardroom debate philosophy and decision tree model
→ **Architecture**: `docs/specifications/architecture.md` — System architecture and layer responsibilities
→ **Workflows spec**: `.github/specs/workflows.md` — Core orchestration workflow specifications
→ **Enterprise capabilities**: `.github/specs/enterprise-capabilities.md` — Knowledge, risk, covenants, MCP
→ **Repository spec**: `.github/specs/repository.md` — Technology stack, coding patterns, testing