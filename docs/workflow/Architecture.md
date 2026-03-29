Architecture Overview

The boardroom chat interface serves two modes through the same <chatroom>
Web Component and the same MCP transport layer:

  1. Structured Workflow — A workflow-owner agent (e.g. Founder for pitch,
     CMO for marketing) conducts a step-by-step conversation with an
     external entity (investor, customer, new business).  Steps are defined
     in YAML files under docs/workflow/samples/.

  2. Dynamic Discussion — The full boardroom of CXO agents engages in
     purpose-driven debate for business decision-making.  No YAML steps;
     the conversation is orchestrated dynamically by AOS.

Both modes share the same infrastructure:

​Orchestrator: agent-operating-system (AOS) Azure Functions App.  Provides
the MCP Interface, handles conversation persistence via
subconscious.asisaga.com, and routes MCP app payloads to connected clients.

​Domain Logic: business-infinity Azure Functions App.  Uses aos-client-sdk
to push workflow states to AOS.  The generic workflow-orchestration endpoint
drives any registered YAML workflow.  The boardroom-debate endpoint drives
dynamic CXO discussions.

​Persistence: subconscious.asisaga.com.  Stores all conversations from
both structured workflows and dynamic discussions, including text messages,
MCP app payloads (graphical UI elements), step state, and agent context.

​UI Layer: theme.asisaga.com (Library) and business-infinity.asisaga.com
(Implementation).  The <chatroom> Web Component renders both text messages
and MCP app payloads (boardroom_ui) for graphical UI elements.

​Identity: Google Identity Services (OAuth2 JWT) verified by AOS.

Workflow Owner Mapping

Each structured workflow is owned by a boardroom agent:

| Workflow                    | Owner   | External Entity    |
|-----------------------------|---------|---------------------|
| pitch_business_infinity     | Founder | Investor            |
| marketing_business_infinity | CMO     | Potential customer  |
| onboard_new_business        | COO     | New business        |
| crisis_response             | CEO     | Boardroom (internal)|
| quarterly_strategic_review  | CEO     | Boardroom (internal)|
| product_launch              | CEO     | Boardroom (internal)|

Data Flow

Structured Workflow Mode:
  YAML → workflow-orchestration → AOS → Owner Agent → MCP app payload → SSE → <chatroom>

Dynamic Discussion Mode:
  Event → boardroom-debate → AOS → All CXO Agents → text + MCP app → SSE → <chatroom>

Persistence (both modes):
  All messages → AOS → subconscious.asisaga.com (text + MCP app payloads)