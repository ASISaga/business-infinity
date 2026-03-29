Communication Protocol (MCP App)

​Communication between the AOS and the <chatroom> Web Component uses the
Model Context Protocol (MCP).

​Transport: Server-Sent Events (SSE) via the AOS endpoint.

​Payload Type: mcp_app with a specific app_id: "boardroom_ui".

Both structured workflows and dynamic discussions use the same transport.
The <chatroom> component renders text messages as chat bubbles and MCP app
payloads as graphical UI elements (action buttons, navigation, dashboards).

Payload Types

1. Text Messages — Standard chat messages between agents and users.
   Persisted in subconscious.asisaga.com as conversation history.

2. MCP App Payloads — Graphical UI elements sent via mcp_app envelope:
   {
     "app_id": "boardroom_ui",
     "payload": {
       "narrative": "Step narrative text",
       "response": "Agent response text",
       "actions": [{"label": "...", "description": "...", "url": "..."}],
       "navigation": {"next": "step_id", "back": "step_id"}
     }
   }
   Persisted in subconscious.asisaga.com alongside text messages.

Navigation Commands

The <chatroom> component sends navigation commands as text with a cmd: prefix:
  cmd:next  — Advance to the next workflow step
  cmd:back  — Return to the previous workflow step

AOS recognises the cmd: prefix, extracts the command, and routes it to
the active workflow-orchestration instance.  The workflow responds with
the next step's MCP app payload.

Persistence

All conversations — text messages and MCP app payloads — are persisted
by subconscious.asisaga.com.  This ensures:
  - Page refreshes resume at the correct workflow step
  - Full conversation history is available for both modes
  - Agent context is maintained across interactions
  - MCP app payloads (graphical UI) are replayed on reconnect