AI Agent Prompt: Frontend Implementation
​Target: business-infinity.asisaga.com (Jekyll) & <chatroom> Component
​Objective: > Configure the <chatroom> Web Component (from theme.asisaga.com) to serve as the Business-Infinity Boardroom interface.
​Requirements:
​Component Setup: In the Jekyll boardroom page, initialize the <chatroom> component with the api-endpoint pointing to the AOS Azure Function.
​Auth Bridge: Create a JavaScript listener on the parent page to capture the Google Identity Services JWT. Update the access-token attribute of the <chatroom> component dynamically.
​MCP JS SDK Integration: >    - Use @modelcontextprotocol/sdk to establish an SSEClientTransport to the AOS.
​Listen for mcp_app payloads where app_id === "boardroom_ui".
​UI Rendering (Shoelace): >    - Render the narrative as a primary chat bubble.
​For each action, render the description as small text followed by a <sl-button variant="primary"> using the label.
​On button click, execute window.open(url, '_blank').
​Render "Next" and "Back" as <sl-button variant="default">. Clicking these must send a text command (e.g., cmd:next) through the generic chat stream to the AOS.
​SCSS Theming: Apply overrides to the Shadow DOM to ensure a "Boardroom" aesthetic (e.g., specific brand colors, formal typography, and minimal border radii).