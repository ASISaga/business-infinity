# theme.asisaga.com — Chatroom Component for Boardroom Workflows

## Objective

Extend the `<chatroom>` Web Component to support structured boardroom workflow
payloads, enabling step-by-step narrative delivery with action buttons and
navigation controls.

## Requirements

### 1. MCP App Payload Handler

Add a handler for `mcp_app` payloads with `app_id: "boardroom_ui"` that
extracts:
- `narrative` — displayed as the primary agent message bubble
- `response` — displayed as the agent response bubble
- `actions[]` — array of `{label, description, url}` rendered as action buttons
- `navigation` — `{next, back}` step IDs rendered as navigation buttons

### 2. Shoelace Action Buttons

For each action in the payload:
```html
<small>{description}</small>
<sl-button variant="primary">{label}</sl-button>
```
On click, execute `window.open(url, '_blank')`.

### 3. Navigation Controls

Render navigation buttons when `next` or `back` step IDs are present:
```html
<sl-button variant="default" @click="sendCommand('cmd:back')">Back</sl-button>
<sl-button variant="default" @click="sendCommand('cmd:next')">Next</sl-button>
```

Navigation sends text commands through the chat stream to AOS, which routes
them to the `pitch-orchestration` workflow.

### 4. Step Progress Indicator

Accept `step_id` and `total_steps` attributes and render a progress indicator
(e.g. step dots or "3 of 9") within the chatroom header.

### 5. Boardroom Theme Variant

Expose a `theme="boardroom"` attribute that applies:
- Formal typography (serif headings, system sans-serif body)
- Dark gradient background
- Brand accent colours
- Reduced border radii
- Smooth step transition animations

## Dependencies

- `@modelcontextprotocol/sdk` — SSE client transport for MCP payloads
- Shoelace — UI components (`sl-button`, `sl-progress-bar`)

## References

→ **Frontend prompt**: `docs/workflow/prompts/frontend.md`
→ **Pitch document**: `docs/workflow/samples/pitch.md`
→ **Communication protocol**: `docs/workflow/Communication.md`