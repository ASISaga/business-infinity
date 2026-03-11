# BusinessInfinity Philosophy

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2026-03-11

## Core Thesis

> BusinessInfinity is a living boardroom of legendary CXOs.  Each CXO inherits
> your company's purpose, responds to events with spontaneous leadership, and
> debates through a decision tree of pathways.  Resonance scoring at CXO and
> boardroom levels ensures debates converge in seconds, and autonomous actions
> are taken with your purpose front and centre.

The boardroom debate is not a binary "go/no-go" vote.  It is a **decision tree
process** where each CXO, driven by events, applies their domain leadership to
propose pathways.  These pathways are evaluated through resonance scoring
against the company's purpose, and the boardroom synthesises them into one
autonomous action.

---

## Decision Tree Debate

### 1. Event Trigger

A business system or market event occurs — ERP, CRM, MES, LinkedIn, regulatory
change, competitor move, or any signal the company subscribes to.

### 2. Spontaneous Leadership

The relevant CXOs step forward, each proposing a pathway rooted in their domain
expertise and the company's purpose.

### 3. Decision Tree Formation

Each CXO proposes a pathway characteristic of their domain:

| CXO (Archetype) | Domain | Pathway Type |
|------------------|--------|--------------|
| CEO (Jobs) | Vision & Strategy | Narrative |
| CFO (Buffett) | Finance & Resources | Resource allocation |
| COO (Deming) | Operations & Workflow | Workflow |
| CMO (Ogilvy) | Market & Communication | Communication |
| CHRO (Drucker) | People & Culture | People-centric |
| CTO (Turing) | Technology & Innovation | Technology |
| CSO (Sun Tzu) | Strategy & Competitive Intelligence | Strategic |

### 4. Debate

CXOs challenge each other's branches of the decision tree, refining them
through cross-functional critique.

### 5. Resonance Scoring

Each branch is scored for alignment with the company's purpose.  Resonance
measures how fully a pathway embodies the organisation's reason for being.

### 6. Boardroom Convergence

The boardroom synthesises individual scores into an overarching resonance
decision — selecting the branch (or combination of branches) that most fully
embodies the company's purpose.

### 7. Autonomous Execution

The chosen pathway is enacted across business systems instantly.

---

## Example: Market + CRM Event

**Event**: Competitor launches a flashy campaign (market), while CRM shows
churn rising.

### Pathway Proposals

| CXO | Pathway | Resonance Score |
|-----|---------|-----------------|
| CMO (Ogilvy) | Retention campaign | 0.90 |
| CFO (Buffett) | Financial incentives | 0.70 |
| CEO (Jobs) | Narrative reframing | 0.85 |
| COO (Deming) | Workflow tweaks | 0.75 |
| CHRO (Drucker) | Staff engagement | 0.80 |

### Debate

- **Buffett** challenges Ogilvy: "Retention must not erode margins."
- **Ogilvy** counters: "Without retention, margins collapse anyway."
- **Jobs** reframes: "Both must serve the purpose of reliability, not just numbers."
- **Deming** adds: "Operational tweaks reduce churn pressure."
- **Drucker** grounds: "Staff must carry this purpose authentically."

### Convergence

Boardroom resonance score synthesised at **0.85** → retention + narrative
reframing chosen.

### Autonomous Execution

CRM launches retention, LinkedIn reframes messaging, ERP adjusts workflows,
HR initiates engagement.

---

## Implementation in BusinessInfinity

The philosophy is implemented through the Agent Operating System and
PurposeDrivenAgent-based CXO agents:

### CXO Domain Mappings

`src/business_infinity/boardroom.py` encodes the domain-pathway mapping for
each CXO role, derived from the archetypes above.  The `CXO_DOMAINS` constant
maps each agent ID to its archetype, domain, pathway type, and description.

### Boardroom Debate Workflow

`src/business_infinity/workflows.py` provides the `boardroom-debate` workflow
that implements the decision tree debate:

1. An event arrives as an HTTP request.
2. All C-suite agents are selected from the RealmOfAgents catalogue.
3. A perpetual orchestration starts with a purpose encoding the debate process.
4. Each agent's domain context is passed as part of the orchestration context.
5. AOS orchestrates the debate, resonance scoring, and convergence internally.

```bash
curl -X POST https://business-infinity.azurewebsites.net/api/workflows/boardroom-debate \
  -H "Content-Type: application/json" \
  -d '{
    "event": "Competitor launches aggressive campaign",
    "event_source": "market",
    "company_purpose": "Deliver reliable innovation that earns lasting trust",
    "context": {"churn_rate": 0.12, "market": "EU SaaS"}
  }'
# → {"orchestration_id": "...", "status": "ACTIVE"}
```

### Architecture

```
Event → boardroom-debate workflow → AOS Orchestration
                                       ├─ CEO proposes narrative pathway
                                       ├─ CFO proposes resource allocation pathway
                                       ├─ COO proposes workflow pathway
                                       ├─ CMO proposes communication pathway
                                       ├─ CHRO proposes people-centric pathway
                                       ├─ CTO proposes technology pathway
                                       └─ CSO proposes strategic pathway
                                       ↓
                                   Debate + Resonance Scoring
                                       ↓
                                   Boardroom Convergence
                                       ↓
                                   Autonomous Execution
```

---

## Principles

1. **Purpose-driven**: Every pathway and decision is measured against the
   company's stated purpose — not KPIs alone.
2. **Spontaneous leadership**: CXOs respond to events proactively, not
   reactively through approval chains.
3. **Decision tree, not binary vote**: The debate produces a rich tree of
   competing pathways, not a simple yes/no.
4. **Resonance over consensus**: Convergence is driven by alignment with
   purpose, not political compromise.
5. **Autonomous execution**: Once the boardroom converges, action is immediate
   and spans all relevant business systems.

---

## References

→ **Boardroom module**: `src/business_infinity/boardroom.py`
→ **Workflows**: `src/business_infinity/workflows.py`
→ **Architecture**: `docs/specifications/architecture.md`
→ **Repository spec**: `.github/specs/repository.md`
