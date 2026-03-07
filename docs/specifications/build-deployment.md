# Build & Deployment

**Last Updated**: 2026-03-07  
**Status**: Active  
**Audience**: Developers, Contributors, AI Agents

## Local Development

### Prerequisites

- Python 3.10+
- Azure Functions Core Tools (for local func start)
- Access to an AOS endpoint

### Setup

```bash
# Clone and install dev dependencies
pip install -e ".[dev]"

# Set environment variables
export AOS_ENDPOINT=http://localhost:7071        # AOS Function App
export REALM_ENDPOINT=http://localhost:7072      # RealmOfAgents (if separate)
export SERVICE_BUS_CONNECTION=                   # Service Bus (optional for local dev)

# Start Azure Functions locally
func start
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific tests
pytest tests/ -v -k "test_workflows_registered"

# Lint
pylint src/business_infinity/
```

**CI matrix**: Python 3.10, 3.11, 3.12 (see `.github/workflows/ci.yml`)

## Deployment

Deployment is managed via **Azure Developer CLI** using `azure.yaml`:

```bash
# Deploy to Azure
azd up

# Deploy only code changes
azd deploy
```

## Dependencies

### Production

```toml
[project.dependencies]
"aos-client-sdk[azure]>=7.0.0"
```

The `[azure]` extra installs:
- Azure Functions integration
- Service Bus client
- Azure authentication

### Development

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pylint>=3.0.0",
]
```

## CI/CD

**GitHub Actions**: `.github/workflows/ci.yml`
- Triggers: push/PR to `main`
- Matrix: Python 3.10, 3.11, 3.12
- Steps: `pip install -e ".[dev]"` → `pytest tests/ -v`

**GitHub Actions**: `.github/workflows/deploy.yml`
- Deployment workflow (see file for triggers)

## Registering with AOS

After deployment, register the app to provision Service Bus infrastructure:

```python
from aos_client import AOSRegistration

async with AOSRegistration(aos_endpoint="https://my-aos.azurewebsites.net") as reg:
    info = await reg.register_app(
        app_name="business-infinity",
        workflows=["strategic-review", "market-analysis", "budget-approval"],
    )
```

## References

→ **Architecture**: `/docs/specifications/architecture.md`  
→ **Agent guidelines**: `/docs/specifications/github-copilot-agent-guidelines.md`  
→ **Repository spec**: `.github/specs/business-infinity-repository.md`  
→ **CI workflow**: `.github/workflows/ci.yml`
