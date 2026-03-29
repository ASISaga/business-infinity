# subconscious.asisaga.com — Session Persistence for Boardroom Workflows

## Objective

Provide MCP-based session persistence for boardroom workflow interactions,
ensuring that agent conversations and workflow step state survive page
refreshes and session reconnections.

## Requirements

### 1. Workflow Step Persistence

Persist the current `step_id` for each active boardroom session:
- On each step navigation event, update the stored `step_id`
- On session reconnect, return the last active `step_id` so the client
  can resume at the correct pitch step

### 2. Agent Conversation History

Store the Founder agent's conversational context across pitch steps:
- Narrative and response pairs for each completed step
- User interactions (action button clicks, navigation commands)
- Timestamps for each interaction

### 3. Session State API

Expose MCP-compatible endpoints for session state:

```
GET  /sessions/{session_id}/state    → { step_id, workflow_id, history[] }
PUT  /sessions/{session_id}/state    → Update step_id and append to history
```

### 4. Multi-Workflow Support

Support concurrent sessions for different workflow types:
- `pitch_business_infinity` — Pitch delivery workflow
- `boardroom_initiation` — General boardroom workflow
- Future workflow types as defined in `docs/workflow/boardroom.yaml`

## Dependencies

- `agent-operating-system` — MCP transport layer for persistence API calls
- `business-infinity` — Workflow definitions and step ID constants

## References

→ **Communication protocol**: `docs/workflow/Communication.md`
→ **Architecture**: `docs/workflow/Architecture.md`
→ **Pitch workflow**: `docs/workflow/samples/pitch.yaml`