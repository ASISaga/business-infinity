# theme.asisaga.com — Chatroom Component for Boardroom (Dual-Mode)

## Objective

Extend the `<chatroom>` Web Component to support the dual-mode boardroom
interface: rendering both structured workflow payloads (step-by-step
narratives with actions and navigation) and dynamic discussion messages
(free-form CXO debates with MCP app graphical UI elements).

## Context

The `<chatroom>` component is the universal rendering layer for the
boardroom.  It handles:
- Text messages (standard chat bubbles) for dynamic discussions
- MCP app payloads (`boardroom_ui`) for structured workflow steps
- Any graphical UI elements sent via MCP app payloads (charts, forms, etc.)

The component must work identically regardless of which workflow is active
or whether the session is a dynamic discussion.

## Requirements

### 1. MCP App Payload Handler

Add a handler for `mcp_app` payloads with `app_id: "boardroom_ui"` that
extracts:
- `narrative` — displayed as the primary agent message bubble
- `response` — displayed as the agent response bubble
- `actions[]` — array of `{label, description, url}` rendered as action buttons
- `navigation` — `{next, back}` step IDs rendered as navigation buttons

### 2. Generic MCP App Rendering

Support rendering any MCP app payload beyond `boardroom_ui`:
- Extensible handler registry for different `app_id` values
- Default renderer for unknown app IDs (display as formatted JSON)
- Support for graphical UI elements (charts, dashboards, forms) as they
  are added to the system

### 3. Shoelace Action Buttons

For each action in the payload:
```html
<small>{description}</small>
<sl-button variant="primary">{label}</sl-button>
```
On click, execute `window.open(url, '_blank')`.

### 4. Navigation Controls

Render navigation buttons when `next` or `back` step IDs are present:
```html
<sl-button variant="default" @click="sendCommand('cmd:back')">Back</sl-button>
<sl-button variant="default" @click="sendCommand('cmd:next')">Next</sl-button>
```

Navigation sends text commands through the chat stream to AOS, which routes
them to the active `workflow-orchestration` instance.

### 5. Step Progress Indicator

Accept `step_id` and `total_steps` attributes and render a progress indicator
(e.g. step dots or "3 of 9") within the chatroom header.  Hide when not in
structured workflow mode.

### 6. Owner Agent Display

Accept an `owner` attribute and display the workflow owner's name/role in
the chat header (e.g. "CMO — David Ogilvy").  Show "Boardroom" when no
owner is set (dynamic discussion mode).

### 7. Conversation Replay

On reconnect, replay the full conversation from `subconscious.asisaga.com`:
- Render text messages as chat bubbles
- Render MCP app payloads using the appropriate handler
- Restore scroll position and step state

### 8. Boardroom Theme Variant

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
→ **Workflow YAML samples**: `docs/workflow/samples/`
→ **Boardroom schema**: `docs/workflow/boardroom.yaml`
→ **Communication protocol**: `docs/workflow/Communication.md`
→ **Multi-repo roadmap**: `docs/multi-repository-implementation.md`