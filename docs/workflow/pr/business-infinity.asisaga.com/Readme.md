# business-infinity.asisaga.com — Boardroom Pitch Interface

## Objective

Configure the `<chatroom>` Web Component on business-infinity.asisaga.com to
render the Business Infinity pitch as an interactive boardroom session.

## Requirements

### 1. Boardroom Pitch Page

Create a dedicated boardroom page (e.g. `/boardroom/`) that initialises the
`<chatroom>` component with the AOS API endpoint for the `pitch-orchestration`
workflow.

```html
<chatroom
  api-endpoint="https://business-infinity.azurewebsites.net/api/workflows/pitch-orchestration"
  app-id="boardroom_ui"
  workflow-id="pitch_business_infinity">
</chatroom>
```

### 2. Authentication Bridge

Implement a JavaScript listener on the boardroom page to capture the Google
Identity Services JWT and update the `access-token` attribute of the
`<chatroom>` component dynamically.

### 3. MCP Payload Rendering

Listen for `mcp_app` payloads where `app_id === "boardroom_ui"` and render:

- **Narrative** → Primary chat bubble (agent message)
- **Response** → Agent response bubble
- **Actions** → For each action, render the `description` as small text
  followed by a `<sl-button variant="primary">` with the `label`. On click,
  execute `window.open(url, '_blank')`.
- **Navigation** → Render "Next" and "Back" as `<sl-button variant="default">`.
  Clicking these sends `cmd:next` or `cmd:back` through the chat stream.

### 4. Step Tracking

Display a step progress indicator (e.g. "Step 3 of 9") using the `step_id`
and `total_steps` returned by the pitch-orchestration workflow response.

### 5. SCSS Theming

Apply "Boardroom" aesthetic overrides to the Shadow DOM:
- Brand colours from the ASI Saga identity
- Formal typography
- Minimal border radii
- Dark mode support for the pitch environment

## Dependencies

- `theme.asisaga.com` — `<chatroom>` Web Component and Shoelace integration
- `agent-operating-system` — MCP SSE endpoint for payload delivery
- `business-infinity` — `pitch-orchestration` workflow backend

## References

→ **Frontend prompt**: `docs/workflow/prompts/frontend.md`
→ **Pitch document**: `docs/workflow/samples/pitch.md`
→ **Pitch workflow**: `docs/workflow/samples/pitch.yaml`
→ **Communication protocol**: `docs/workflow/Communication.md`