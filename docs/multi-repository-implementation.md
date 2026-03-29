# Multi-Repository Implementation Roadmap

**Version**: 2.0.0
**Status**: Active
**Last Updated**: 2026-03-29

## Overview

This document describes the work required to fully implement the Business
Infinity boardroom system — a dual-mode chat interface that supports both
**structured YAML-driven workflows** (pitch, marketing, onboarding, etc.)
and **dynamic purpose-driven CXO discussions** — across the six repositories
in the ASI Saga ecosystem.

The boardroom chat interface uses the same `<chatroom>` Web Component for
both modes.  Each structured workflow is owned by a boardroom agent (Founder
for pitch, CMO for marketing, COO for onboarding, CEO for crisis/strategy).
Dynamic discussions involve the full C-suite debating through resonance
scoring.

All conversations — text and MCP app payloads (graphical UI elements) — are
persisted by `subconscious.asisaga.com`.  The Foundry Agent Service handles
multi-agent orchestration through the Agent Operating System.

---

## Architecture

```
┌─────────────────────────────────────┐
│  business-infinity.asisaga.com      │  ← Frontend: Jekyll + <chatroom>
│  (boardroom page, auth bridge)      │
└──────────────┬──────────────────────┘
               │ SSE (text + MCP app payloads)
               ▼
┌─────────────────────────────────────┐
│  agent-operating-system (AOS)       │  ← MCP routing, session management
│  (SSE transport, cmd: routing)      │     Foundry Agent Service orchestration
└──────────────┬──────────────────────┘
               │ start_orchestration / send_app_payload
               ▼
┌─────────────────────────────────────┐
│  business-infinity                  │  ← Workflows: workflow-orchestration
│  (YAML registry, boardroom.py)      │     + boardroom-debate (dynamic)
└──────────────┬──────────────────────┘
               │ SDK APIs
               ▼
┌─────────────────────────────────────┐
│  aos-client-sdk                     │  ← SDK: YAML loader, MCP API
│  (workflow helpers, validation)      │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  subconscious.asisaga.com           │  ← Persistence: conversations,
│  (text + MCP app payloads, state)   │     step state, agent context
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  theme.asisaga.com                  │  ← Component: <chatroom> + Shoelace
│  (text + MCP app payload rendering) │
└─────────────────────────────────────┘
```

---

## Dual-Mode Operation

The boardroom supports two modes through the same infrastructure:

### Mode 1: Structured Workflow

A workflow-owner agent conducts a step-by-step conversation with an
external entity.  Steps are defined in YAML files.

```
YAML file → workflow-orchestration → AOS → Owner Agent → MCP app payload → SSE → <chatroom>
```

| Workflow | Owner | External Entity | YAML |
|----------|-------|-----------------|------|
| pitch_business_infinity | Founder | Investor | pitch.yaml |
| marketing_business_infinity | CMO | Potential customer | marketing.yaml |
| onboard_new_business | COO | New business | onboarding.yaml |
| crisis_response | CEO | Boardroom (internal) | crisis-response.yaml |
| quarterly_strategic_review | CEO | Boardroom (internal) | strategic-review.yaml |
| product_launch | CEO | Boardroom (internal) | product-launch.yaml |

### Mode 2: Dynamic Discussion

The full boardroom of CXO agents engages in purpose-driven debate.  No
YAML steps; the conversation is orchestrated dynamically.

```
Business event → boardroom-debate → AOS → All CXO Agents → text + MCP app → SSE → <chatroom>
```

---

## Repository Work Items

### 1. business-infinity (This Repository) ✅ Core Complete

**Status**: Generic workflow system implemented

| Item | Status | Description |
|------|--------|-------------|
| `WORKFLOW_REGISTRY` in `boardroom.py` | ✅ Done | Registry of all structured workflows with owners |
| `workflow-orchestration` generic endpoint | ✅ Done | Single endpoint drives any registered YAML workflow |
| `pitch-orchestration` workflow | ✅ Done | Backward-compatible pitch delivery (uses registry) |
| `boardroom-debate` workflow | ✅ Done | Dynamic CXO discussion with resonance scoring |
| `owner` field in all YAML files | ✅ Done | Each workflow declares its owning agent |
| `boardroom.yaml` schema updated | ✅ Done | Schema documents dual-mode, owner field, response field |
| Sample workflows (6 YAML files) | ✅ Done | pitch, onboarding, marketing, crisis, strategic, launch |
| Tests (32 passing) | ✅ Done | Registry, backward compat, workflow registration |
| Pitch YAML loading in workflow | ⬜ Pending | Load and parse YAML within the workflow at runtime |
| `GOTO_STEP` handler | ⬜ Pending | Handle step navigation commands from client |
| MCP payload construction | ⬜ Pending | Build `boardroom_ui` payloads from YAML steps |

**Remaining work**: The `workflow-orchestration` endpoint starts
orchestrations with workflow context.  It needs the aos-client-sdk YAML
loader to parse steps at runtime and construct MCP payloads.

### 2. aos-client-sdk

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| `send_app_payload()` API | ⬜ Pending | MCP app payload delivery to client sessions |
| Workflow YAML loader | ⬜ Pending | Load and validate any boardroom YAML file |
| Workflow registry integration | ⬜ Pending | Discover workflows from `WORKFLOW_REGISTRY` |
| Step navigation helper | ⬜ Pending | Resolve next/back commands to step IDs |
| JSON Schema for boardroom YAML | ⬜ Pending | Validation including `owner` and `response` fields |
| `WorkflowRequest` extensions | ⬜ Pending | Expose workflow steps, current step, owner agent |

**Key dependency**: The SDK must provide `send_app_payload()` before any
workflow can deliver MCP app payloads to the frontend.

→ **PR specification**: `docs/workflow/pr/aos-client-sdk/Readme.md`

### 3. agent-operating-system

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| MCP app payload routing | ⬜ Pending | Route `mcp_app` payloads via SSE to clients |
| `cmd:` prefix routing | ⬜ Pending | Route navigation commands to active workflows |
| Session management (dual-mode) | ⬜ Pending | Support both structured and dynamic sessions |
| `GOTO_STEP` command dispatch | ⬜ Pending | Dispatch step commands to workflow instances |
| Foundry Agent Service integration | ⬜ Pending | Multi-agent orchestration for boardroom debates |
| MCP app persistence routing | ⬜ Pending | Route MCP app payloads to subconscious for storage |

**Key dependency**: AOS must support `mcp_app` envelope routing and
Foundry Agent Service orchestration before either mode works end-to-end.

→ **PR specification**: `docs/workflow/pr/agent-operating-system/Readme.md`

### 4. business-infinity.asisaga.com

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| Generic boardroom page | ⬜ Pending | Single page supporting any workflow via URL params |
| Google auth bridge | ⬜ Pending | JWT capture and `access-token` attribute update |
| MCP payload rendering | ⬜ Pending | Render text + MCP app payloads (narratives, actions) |
| Workflow selection | ⬜ Pending | Select workflow by ID, auto-detect owner agent |
| Step progress indicator | ⬜ Pending | Show current step for structured workflows |
| Boardroom SCSS theming | ⬜ Pending | Dark, formal aesthetic for boardroom interface |

**Key dependency**: Requires `theme.asisaga.com` chatroom component with
MCP app payload support, and AOS SSE endpoint.

→ **PR specification**: `docs/workflow/pr/business-infinity.asisaga.com/Readme.md`

### 5. theme.asisaga.com

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| `mcp_app` payload handler | ⬜ Pending | Handle `boardroom_ui` app payloads |
| Shoelace action buttons | ⬜ Pending | Render action `{label, description, url}` |
| Navigation controls | ⬜ Pending | Next/Back buttons sending `cmd:` commands |
| Text message rendering | ⬜ Pending | Standard chat bubbles for dynamic discussions |
| MCP app graphical rendering | ⬜ Pending | Render any UI elements from MCP app payloads |
| Step progress attribute | ⬜ Pending | `step_id` and `total_steps` display |
| `theme="boardroom"` variant | ⬜ Pending | Formal dark theme for boardroom pages |

**Key dependency**: This is a library consumed by business-infinity.asisaga.com.
Changes here must be published before the frontend can use them.

→ **PR specification**: `docs/workflow/pr/theme.asisaga.com/Readme.md`

### 6. subconscious.asisaga.com

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| Step state persistence | ⬜ Pending | Store/retrieve `step_id` per session |
| Text conversation persistence | ⬜ Pending | Store all text messages from both modes |
| MCP app payload persistence | ⬜ Pending | Store graphical UI payloads alongside text |
| Session state API | ⬜ Pending | GET/PUT endpoints for session state |
| Multi-workflow support | ⬜ Pending | Support concurrent workflow types per session |
| Dynamic discussion persistence | ⬜ Pending | Store CXO debate threads and resonance scores |
| Replay on reconnect | ⬜ Pending | Return full conversation (text + MCP app) on rejoin |

**Key dependency**: Provides persistence for both modes so page refreshes
resume correctly and full history is available.

→ **PR specification**: `docs/workflow/pr/subconscious.asisaga.com/Readme.md`

---

## Implementation Order

```
Phase 1 (Foundation)
├── aos-client-sdk        → send_app_payload(), YAML loader, owner support
└── subconscious.asisaga.com → Text + MCP app persistence, multi-workflow

Phase 2 (Infrastructure)
├── agent-operating-system → MCP routing, cmd: handling, Foundry integration
└── business-infinity      → GOTO_STEP handler, payload construction

Phase 3 (Presentation)
├── theme.asisaga.com      → Chatroom dual-mode rendering
└── business-infinity.asisaga.com → Generic boardroom page, auth, theming
```

### Critical Path

```
aos-client-sdk (send_app_payload + YAML loader)
    → agent-operating-system (MCP routing + Foundry orchestration)
        → business-infinity (payload construction)
            → theme.asisaga.com (dual-mode rendering)
                → business-infinity.asisaga.com (integration)
```

---

## Key Design Decisions

### 1. Single Generic Endpoint

One `workflow-orchestration` endpoint drives all structured workflows.
The `workflow_id` in the request body selects the YAML definition and
owner agent from `WORKFLOW_REGISTRY`.  No per-workflow Python code needed.

### 2. Owner Agent Pattern

Each structured workflow declares an `owner` agent in both the YAML file
and the registry.  The owner conducts the conversation with the external
entity, while the full boardroom participates in dynamic discussions.

### 3. MCP for All Communication

All boardroom communication — text and graphical UI elements — flows
through the Model Context Protocol.  `subconscious.asisaga.com` persists
both payload types, enabling full conversation replay.

### 4. Workflow YAML as Source of Truth

Workflow content lives in YAML files, not hardcoded in Python.  This allows
content updates without code deployment and enables non-developers to create
new workflows.

### 5. Dual-Mode Same Interface

The same `<chatroom>` component and same SSE transport handle both
structured workflows (step-by-step) and dynamic discussions (free-form).
The UI adapts based on payload type.

---

## Success Criteria

The implementation is complete when:

1. A user navigates to `business-infinity.asisaga.com/boardroom/?workflow=pitch_business_infinity`
2. The `<chatroom>` component connects via SSE to the AOS endpoint
3. The owner agent (Founder) delivers the pitch as interactive steps
4. Next/Back navigation moves through all workflow steps
5. Page refreshes resume at the correct step (via subconscious persistence)
6. Switching to `?workflow=marketing_business_infinity` starts the CMO-led marketing workflow
7. A dynamic boardroom debate can run in the same interface without a workflow ID
8. All conversations (text + MCP app payloads) are persisted and replayable

---

## References

→ **Workflow YAML samples**: `docs/workflow/samples/`
→ **Boardroom schema**: `docs/workflow/boardroom.yaml`
→ **Architecture**: `docs/workflow/Architecture.md`
→ **Communication**: `docs/workflow/Communication.md`
→ **Backend prompt**: `docs/workflow/prompts/backend.md`
→ **Frontend prompt**: `docs/workflow/prompts/frontend.md`
→ **Philosophy**: `docs/philosophy.md`
→ **Workflows**: `src/business_infinity/workflows.py`
→ **Boardroom module**: `src/business_infinity/boardroom.py`
→ **PR specs**: `docs/workflow/pr/`
