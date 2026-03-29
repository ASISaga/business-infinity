AI Agent Prompt: Backend Implementation
​Target: Business-Infinity Azure Functions App (Python)
​Objective: > Implement a Python-based Azure Function for the Business-Infinity boardroom that acts as a domain controller.
​Requirements:
​Integration: Use the aos-client-sdk to communicate with the agent-operating-system (AOS).
​Workflow Logic: Load a boardroom.yaml file. Validate it against a JSON Schema ensuring all steps contain a narrative and an actions array.
​State Management: Implement a handler for GOTO_STEP commands. When received:
​Fetch the corresponding step from the YAML.
​Construct an MCP-compliant JSON payload containing the narrative, action buttons (label, description, url), and navigation IDs.
​Use aos.mcp.send_app_payload() to push this data to the user's session.
​Security: Every request must receive a Google JWT. Use the aos.auth.verify() method from the SDK to ensure the user is authorized before returning workflow data.
​Persistence: Ensure that the current step_id is passed to the AOS persistence layer so the session remains stateful across page refreshes.