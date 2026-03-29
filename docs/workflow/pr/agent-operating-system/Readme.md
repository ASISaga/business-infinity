# agent-operating-system — MCP App Payload Routing for Boardroom Workflows

## Objective

Enable the Agent Operating System to route MCP app payloads from boardroom
workflows to connected clients via Server-Sent Events (SSE), supporting the
interactive pitch delivery and navigation commands.

## Requirements

### 1. MCP App Payload Delivery

When a workflow calls `aos.mcp.send_app_payload()`, the AOS must:
- Wrap the payload in an `mcp_app` envelope with the specified `app_id`
- Deliver it to the correct client session via the existing SSE transport
- Support `app_id: "boardroom_ui"` for boardroom-specific rendering

### 2. Navigation Command Routing

When the `<chatroom>` client sends text commands (e.g. `cmd:next`, `cmd:back`),
the AOS must:
- Recognise the `cmd:` prefix as a workflow navigation command
- Extract the command type (`next`, `back`)
- Route the command to the active `pitch-orchestration` workflow instance
- The workflow responds with the next/previous step's MCP app payload

### 3. Session Persistence

Ensure `step_id` is persisted in the AOS session layer so that:
- Page refreshes resume at the correct pitch step
- The Founder agent maintains conversational context across steps

### 4. Workflow Step Resolution

When receiving a `GOTO_STEP` command, resolve the target step from the workflow
YAML and construct the MCP-compliant JSON payload containing:
- `narrative` — step narrative text
- `actions[]` — array of `{label, description, url}`
- `navigation` — `{next, back}` step IDs

## Dependencies

- `aos-client-sdk` — SDK extensions for `send_app_payload()` API
- `subconscious.asisaga.com` — Session persistence layer

## References

→ **Backend prompt**: `docs/workflow/prompts/backend.md`
→ **Architecture**: `docs/workflow/Architecture.md`
→ **Communication protocol**: `docs/workflow/Communication.md`
→ **Pitch workflow**: `docs/workflow/samples/pitch.yaml`