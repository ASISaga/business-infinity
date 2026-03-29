# subconscious.asisaga.com — Conversation Persistence for Boardroom

## Objective

Provide MCP-based conversation persistence for all boardroom interactions,
storing both text messages and MCP app payloads (graphical UI elements) from
structured workflows and dynamic CXO discussions.

## Context

The boardroom operates in two modes, both requiring full conversation
persistence:

1. **Structured workflows** — Step-by-step conversations between a
   workflow-owner agent and an external entity.  Includes text messages,
   MCP app payloads (narratives, actions, navigation), and step state.
2. **Dynamic discussions** — Free-form debates between CXO agents.
   Includes text messages, MCP app payloads (dashboards, charts),
   resonance scores, and debate context.

All conversations must be replayable on page refresh or session reconnect.

## Requirements

### 1. Text Message Persistence

Store all text messages from both modes:
- Agent-to-user messages (structured workflows)
- Agent-to-agent messages (dynamic discussions)
- User-to-agent messages (commands, queries)
- Include sender, timestamp, and session context

### 2. MCP App Payload Persistence

Store MCP app payloads (graphical UI elements) alongside text messages:
- `boardroom_ui` payloads with narrative, response, actions, navigation
- Any future app_id payloads (charts, dashboards, forms)
- Payloads are stored as structured JSON, not flattened text
- Each payload is associated with a session and timestamp

### 3. Workflow Step Persistence

Persist the current workflow state for structured sessions:
- `workflow_id` — which workflow is active
- `step_id` — current step in the workflow
- `owner` — the agent conducting the workflow
- On session reconnect, return the last active state

### 4. Agent Conversation History

Store the owner agent's conversational context across steps:
- Narrative and response pairs for each completed step
- User interactions (action button clicks, navigation commands)
- Timestamps for each interaction
- Support multiple concurrent workflow sessions per user

### 5. Session State API

Expose MCP-compatible endpoints for session state:

```
GET  /sessions/{session_id}/state
→ { workflow_id, step_id, owner, mode, history[] }

PUT  /sessions/{session_id}/state
→ Update step_id, append to history

GET  /sessions/{session_id}/conversation
→ Full conversation replay (text + MCP app payloads)
```

### 6. Multi-Workflow Support

Support concurrent sessions for different workflow types:
- `pitch_business_infinity` — Pitch delivery (owner: founder)
- `marketing_business_infinity` — Marketing (owner: cmo)
- `onboard_new_business` — Onboarding (owner: coo)
- `crisis_response` — Crisis response (owner: ceo)
- `quarterly_strategic_review` — Strategic review (owner: ceo)
- `product_launch` — Product launch (owner: ceo)
- Dynamic boardroom debates (no workflow_id, all CXOs)

### 7. Conversation Replay

On session reconnect or page refresh:
- Return the full conversation in order (text + MCP app payloads)
- Include metadata (sender, timestamp, payload type)
- The `<chatroom>` component replays the conversation to restore state

## Dependencies

- `agent-operating-system` — MCP transport layer for persistence API calls
- `business-infinity` — Workflow definitions and `WORKFLOW_REGISTRY`

## References

→ **Communication protocol**: `docs/workflow/Communication.md`
→ **Architecture**: `docs/workflow/Architecture.md`
→ **Workflow YAML samples**: `docs/workflow/samples/`
→ **Boardroom schema**: `docs/workflow/boardroom.yaml`
→ **Multi-repo roadmap**: `docs/multi-repository-implementation.md`