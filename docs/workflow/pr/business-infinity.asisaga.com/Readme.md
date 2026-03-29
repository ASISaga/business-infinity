# business-infinity.asisaga.com — Generic Boardroom Interface

## Objective

Configure the `<chatroom>` Web Component on business-infinity.asisaga.com to
serve as the generic boardroom interface, supporting any registered workflow
(pitch, marketing, onboarding, etc.) and dynamic CXO discussions through the
same page.

## Context

The boardroom page is the single entry point for all boardroom interactions.
It supports two modes:

1. **Structured workflow** — Selected via URL parameter (e.g.
   `?workflow=pitch_business_infinity`).  The owner agent conducts the
   step-by-step conversation.
2. **Dynamic discussion** — No workflow parameter.  The full C-suite
   engages in purpose-driven debate.

## Requirements

### 1. Generic Boardroom Page

Create a single boardroom page (`/boardroom/`) that initialises the
`<chatroom>` component dynamically based on the URL:

```html
<!-- Structured workflow mode -->
<chatroom
  api-endpoint="https://business-infinity.azurewebsites.net/api/workflows/workflow-orchestration"
  app-id="boardroom_ui"
  workflow-id="pitch_business_infinity">
</chatroom>

<!-- Dynamic discussion mode (no workflow-id) -->
<chatroom
  api-endpoint="https://business-infinity.azurewebsites.net/api/workflows/boardroom-debate"
  app-id="boardroom_ui">
</chatroom>
```

The page reads `?workflow=<workflow_id>` from the URL to determine the mode.

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

### 4. Workflow Selection

Support workflow selection via:
- URL parameter: `?workflow=marketing_business_infinity`
- JavaScript API: `chatroom.setAttribute('workflow-id', 'onboard_new_business')`
- Landing page with workflow cards showing all available workflows

### 5. Step Progress Indicator

Display a step progress indicator (e.g. "Step 3 of 9") using the `step_id`
and `total_steps` returned by the `workflow-orchestration` response.
Hide the indicator for dynamic discussion mode.

### 6. Owner Agent Display

Show the workflow owner's name and role (e.g. "CMO — David Ogilvy") in the
chat header during structured workflows.  Show "Boardroom" for dynamic
discussions.

### 7. SCSS Theming

Apply "Boardroom" aesthetic overrides to the Shadow DOM:
- Brand colours from the ASI Saga identity
- Formal typography
- Minimal border radii
- Dark mode support for the boardroom environment

## Dependencies

- `theme.asisaga.com` — `<chatroom>` Web Component and Shoelace integration
- `agent-operating-system` — MCP SSE endpoint for payload delivery
- `business-infinity` — `workflow-orchestration` and `boardroom-debate` backends

## References

→ **Frontend prompt**: `docs/workflow/prompts/frontend.md`
→ **Workflow YAML samples**: `docs/workflow/samples/`
→ **Boardroom schema**: `docs/workflow/boardroom.yaml`
→ **Communication protocol**: `docs/workflow/Communication.md`
→ **Multi-repo roadmap**: `docs/multi-repository-implementation.md`