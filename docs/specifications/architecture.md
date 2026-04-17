# System Architecture

**Last Updated**: 2026-03-07  
**Status**: Active  
**Audience**: Developers, Contributors, AI Agents

## Overview

BusinessInfinity is a lean Python application that exposes business orchestration workflows via Azure Functions. All infrastructure concerns (Azure Functions scaffolding, Service Bus, auth, agent lifecycle) are delegated to the `aos-client-sdk`.

## Core Architecture Principle

> **BusinessInfinity focuses only on business logic. The SDK handles the rest.**

```
┌─────────────────────────────────────────────────────┐
│  BusinessInfinity (this app)                        │
│  ┌───────────────────────────────────────────────┐  │
│  │  workflows.py       @app.workflow decorators  │  │
│  │  function_app.py    app.get_functions()       │  │
│  │    └─ aos-client-sdk handles everything else  │  │
│  └───────────────────────────────────────────────┘  │
│  Zero Azure Functions boilerplate.                  │
│  Zero agent code. Zero infrastructure code.         │
└──────────────┬───────────────────┬──────────────────┘
               │ HTTPS             │ Azure Service Bus
               ▼                   ▼
┌─────────────────────────────────────────────────────┐
│  Agent Operating System (infrastructure)            │
│  ┌──────────────────┐  ┌─────────────────────────┐  │
│  │ aos-dispatcher   │  │ aos-realm-of-agents     │  │
│  │ Orchestration API│  │ Agent catalog:          │  │
│  │ + Service Bus    │  │  CEO · CFO · CMO        │  │
│  │   triggers       │  │  COO · CTO · CSO        │  │
│  └──────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Layer Responsibilities

| Layer | Repository | Responsibility |
|-------|-----------|----------------|
| Business Logic | `business-infinity` | Workflow definitions, business rules, orchestration intent |
| SDK / Framework | `aos-client-sdk` | Azure Functions, Service Bus, HTTP triggers, auth, health checks |
| Orchestration | `aos-dispatcher` | Agent routing, perpetual orchestration management |
| Agent Catalog | `aos-realm-of-agents` | C-suite agents, capabilities, LoRA adapters |
| OS Kernel | `aos-kernel` | Messaging, storage, monitoring, agent lifecycle |

## Key Components

### `src/business_infinity/workflows.py`

Compatibility export module. Provides:
- Shared `app` instance import
- C-suite agent ID constants and selection helpers

Workflow definitions live in `src/business_infinity/workflow_definitions.py`.

### `function_app.py`

Zero-boilerplate Azure Functions entry point:
```python
from aos_client import AOSApp
from aos_client.observability import ObservabilityConfig

app = AOSApp(
    name="business-infinity",
    observability=ObservabilityConfig(
        structured_logging=True,
        correlation_tracking=True,
        health_checks=["aos", "service-bus"],
    ),
)
from business_infinity import workflow_definitions  # register decorators
functions = app.get_functions()
```

The `workflow_definitions` import is intentional side-effect registration:
decorators execute at import time and attach workflows/update handlers/tools to
the shared `app` instance before `get_functions()` is called.

### `pyproject.toml`

Project configuration:
- Package metadata and version
- Dependencies (`aos-client-sdk[azure]`)
- Dev extras (`pytest`, `pytest-asyncio`, `pylint`)
- pytest configuration (`asyncio_mode = "auto"`)

### `azure.yaml`

Azure Developer CLI deployment configuration.

## Orchestration Model

All orchestrations are **perpetual and purpose-driven**:

1. Client calls `start_orchestration(agent_ids, purpose, purpose_scope, context)`
2. AOS creates a perpetual orchestration
3. Agents work toward the `purpose` indefinitely
4. Orchestration never "completes" — it continues until explicitly stopped

## Testing Architecture

```
tests/
└── test_workflows.py    # Unit tests for workflow registration and constants
```

Tests validate:
- Workflow registration counts and names
- C-suite constants (IDs and types)
- Update handler registration
- MCP tool registration
- Observability configuration

**No integration tests** — infrastructure is managed by AOS, not this app.

## References

→ **Build & deployment**: `/docs/specifications/build-deployment.md`  
→ **Agent guidelines**: `/docs/specifications/github-copilot-agent-guidelines.md`  
→ **Repository spec**: `.github/specs/repository.md`  
→ **Conventional tools**: `.github/docs/conventional-tools.md`
