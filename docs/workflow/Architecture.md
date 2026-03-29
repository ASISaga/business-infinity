Architecture Overview

​Orchestrator: agent-operating-system (AOS) Azure Functions App. Provides the MCP Interface and handles conversation persistence.

​Domain Logic: business-infinity Azure Functions App. Uses aos-client-sdk to push workflow states to AOS.

​UI Layer: theme.asisaga.com (Library) and business-infinity.asisaga.com (Implementation).

​Identity: Google Identity Services (OAuth2 JWT) verified by AOS.