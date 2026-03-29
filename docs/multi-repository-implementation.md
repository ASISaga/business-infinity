# Multi-Repository Implementation Roadmap

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2026-03-29

## Overview

This document describes the work required to fully implement the Business
Infinity pitch orchestration — delivering `samples/pitch.md` as an interactive
boardroom session through business-infinity.asisaga.com — across the five
repositories in the ASI Saga ecosystem.

The pitch is not just a presentation: it is a live demonstration of the product
itself. The Paul Graham Founder Agent delivers the pitch through the very
boardroom system being pitched, embodying the recursive self-learning philosophy
at the core of Business Infinity.

---

## Architecture

```
┌─────────────────────────────────────┐
│  business-infinity.asisaga.com      │  ← Frontend: Jekyll + <chatroom>
│  (boardroom page, auth bridge)      │
└──────────────┬──────────────────────┘
               │ SSE (MCP payloads)
               ▼
┌─────────────────────────────────────┐
│  agent-operating-system (AOS)       │  ← MCP routing, session management
│  (SSE transport, cmd: routing)      │
└──────────────┬──────────────────────┘
               │ start_orchestration
               ▼
┌─────────────────────────────────────┐
│  business-infinity                  │  ← Workflows: pitch-orchestration
│  (pitch.yaml, boardroom.py)         │
└──────────────┬──────────────────────┘
               │ send_app_payload
               ▼
┌─────────────────────────────────────┐
│  aos-client-sdk                     │  ← SDK: YAML loader, MCP API
│  (workflow helpers, validation)      │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  subconscious.asisaga.com           │  ← Persistence: step state, history
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  theme.asisaga.com                  │  ← Component: <chatroom> + Shoelace
│  (MCP handler, boardroom theme)     │
└─────────────────────────────────────┘
```

---

## Repository Work Items

### 1. business-infinity (This Repository) ✅ Partially Complete

**Status**: Core workflow implemented

| Item | Status | Description |
|------|--------|-------------|
| `pitch-orchestration` workflow | ✅ Done | Orchestrates pitch delivery through boardroom |
| `PITCH_*` constants in `boardroom.py` | ✅ Done | Purpose, scope, step IDs |
| `pitch.md` documentation | ✅ Done | Markdown pitch + philosophy document |
| Tests for new workflow | ✅ Done | 6 new tests in `test_workflows.py` |
| Pitch YAML loading in workflow | ⬜ Pending | Load and parse `pitch.yaml` within the workflow |
| `GOTO_STEP` handler | ⬜ Pending | Handle step navigation commands from client |
| MCP payload construction | ⬜ Pending | Build `boardroom_ui` payloads from YAML steps |

**Remaining work**: The `pitch-orchestration` workflow currently starts an
orchestration with the pitch context. It needs to be extended to handle
`GOTO_STEP` commands from the client, load individual steps from `pitch.yaml`,
and construct MCP-compliant payloads for the boardroom UI.

### 2. aos-client-sdk

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| `send_app_payload()` API | ⬜ Pending | MCP app payload delivery to client sessions |
| Workflow YAML loader | ⬜ Pending | Load and validate boardroom YAML files |
| Step navigation helper | ⬜ Pending | Resolve next/back commands to step IDs |
| JSON Schema for boardroom YAML | ⬜ Pending | Validation schema for workflow definitions |
| `WorkflowRequest` extensions | ⬜ Pending | Expose workflow steps and current step |

**Key dependency**: The SDK must provide `send_app_payload()` before the
business-infinity workflow can deliver payloads to the frontend. This is the
critical path.

→ **PR specification**: `docs/workflow/pr/aos-client-sdk/Readme.md`

### 3. agent-operating-system

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| MCP app payload routing | ⬜ Pending | Route `mcp_app` payloads via SSE to clients |
| `cmd:` prefix routing | ⬜ Pending | Route navigation commands to active workflows |
| Session step persistence | ⬜ Pending | Persist `step_id` in session layer |
| `GOTO_STEP` command dispatch | ⬜ Pending | Dispatch step commands to workflow instances |

**Key dependency**: AOS must support `mcp_app` envelope routing before the
frontend can receive boardroom payloads. The `cmd:` routing enables interactive
navigation.

→ **PR specification**: `docs/workflow/pr/agent-operating-system/Readme.md`

### 4. business-infinity.asisaga.com

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| Boardroom page (`/boardroom/`) | ⬜ Pending | Jekyll page with `<chatroom>` component |
| Google auth bridge | ⬜ Pending | JWT capture and `access-token` attribute update |
| MCP payload rendering | ⬜ Pending | Render narratives, actions, navigation |
| Step progress indicator | ⬜ Pending | Show current step (e.g. "3 of 9") |
| Boardroom SCSS theming | ⬜ Pending | Dark, formal aesthetic for pitch delivery |

**Key dependency**: Requires `theme.asisaga.com` chatroom component with
boardroom payload support, and AOS MCP SSE endpoint.

→ **PR specification**: `docs/workflow/pr/business-infinity.asisaga.com/Readme.md`

### 5. theme.asisaga.com

**Status**: Not started

| Item | Status | Description |
|------|--------|-------------|
| `mcp_app` payload handler | ⬜ Pending | Handle `boardroom_ui` app payloads |
| Shoelace action buttons | ⬜ Pending | Render action `{label, description, url}` |
| Navigation controls | ⬜ Pending | Next/Back buttons sending `cmd:` commands |
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
| Conversation history | ⬜ Pending | Narrative/response pairs per step |
| Session state API | ⬜ Pending | GET/PUT endpoints for session state |
| Multi-workflow support | ⬜ Pending | Support concurrent workflow types |

**Key dependency**: Provides session persistence so page refreshes resume at
the correct pitch step.

→ **PR specification**: `docs/workflow/pr/subconscious.asisaga.com/Readme.md`

---

## Implementation Order

The repositories have dependencies that dictate the implementation sequence:

```
Phase 1 (Foundation)
├── aos-client-sdk        → send_app_payload(), YAML loader
└── subconscious.asisaga.com → Session persistence API

Phase 2 (Infrastructure)
├── agent-operating-system → MCP routing, cmd: handling
└── business-infinity      → GOTO_STEP handler, payload construction

Phase 3 (Presentation)
├── theme.asisaga.com      → Chatroom boardroom support
└── business-infinity.asisaga.com → Boardroom page, auth, theming
```

### Critical Path

```
aos-client-sdk (send_app_payload)
    → agent-operating-system (MCP routing)
        → business-infinity (payload construction)
            → theme.asisaga.com (rendering)
                → business-infinity.asisaga.com (integration)
```

---

## Key Design Decisions

### 1. MCP for All Communication

All boardroom communication flows through the Model Context Protocol. This
ensures a single, standardised transport layer and enables the chatroom
component to remain protocol-agnostic.

### 2. Workflow YAML as Source of Truth

The pitch content lives in `docs/workflow/samples/pitch.yaml`, not hardcoded in
Python. This allows pitch content updates without code deployment and enables
non-developers to modify narratives.

### 3. Founder Agent as Presenter

The Paul Graham Founder Agent delivers the pitch, embodying the recursive
philosophy: the product demonstrates itself through its own capabilities.

### 4. Purpose-Driven Orchestration

The pitch orchestration follows the same perpetual, purpose-driven pattern as
all Business Infinity workflows. This consistency ensures the pitch is truly a
product demonstration, not a separate presentation system.

---

## Success Criteria

The implementation is complete when:

1. A user navigates to `business-infinity.asisaga.com/boardroom/`
2. The `<chatroom>` component connects via SSE to the AOS endpoint
3. The `pitch-orchestration` workflow starts with the Founder agent
4. Each pitch step renders as an interactive narrative with actions
5. Next/Back navigation moves through all 9 pitch steps
6. Page refreshes resume at the correct step
7. The final reveal step confirms the live boardroom session

---

## References

→ **Pitch document**: `docs/workflow/samples/pitch.md`
→ **Pitch workflow**: `docs/workflow/samples/pitch.yaml`
→ **Architecture**: `docs/workflow/Architecture.md`
→ **Communication**: `docs/workflow/Communication.md`
→ **Backend prompt**: `docs/workflow/prompts/backend.md`
→ **Frontend prompt**: `docs/workflow/prompts/frontend.md`
→ **Philosophy**: `docs/philosophy.md`
→ **PR specs**: `docs/workflow/pr/`
