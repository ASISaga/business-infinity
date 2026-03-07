# GitHub Copilot Agent Guidelines

**Last Updated**: 2026-03-07  
**Status**: Active  
**Audience**: AI Agents, Contributors

## Overview

Guidelines for GitHub Copilot coding agents working in the BusinessInfinity repository. These standards ensure agents produce high-quality, consistent code that aligns with the repository's architecture and principles.

## Core Mandate

**BusinessInfinity contains only business logic.** Agents must never:
- Add Azure Functions boilerplate (triggers, bindings, decorators outside `@app.workflow`)
- Implement agent lifecycle management (that's AOS's job)
- Add infrastructure code (Service Bus, auth, storage)

## Python Standards

→ **Complete Python standards**: `.github/instructions/python.instructions.md`

Key rules:
- PEP 8 compliance, 88-char line limit
- Type hints on all function signatures
- `from __future__ import annotations` at module top
- Google-style docstrings for public functions
- Use `logging`, never `print()`

## Azure Functions / AOS Patterns

→ **Complete AOS patterns**: `.github/instructions/azure-functions.instructions.md`

Key patterns:
- Use `@app.workflow("name")` for workflow registration
- Use `await request.client.start_orchestration(...)` for perpetual orchestrations
- Always return `{"orchestration_id": ..., "status": ...}` from orchestration starters
- Use `workflow_template` for reusable orchestration patterns

## Validation Before Committing

```bash
pytest tests/ -v                      # Run all tests
pylint src/business_infinity/         # Lint
```

Both must pass with no errors before any code is committed.

## Documentation Standards

→ **Complete documentation standards**: `.github/instructions/docs.instructions.md`

Key rules:
- Update existing docs, don't create new ones for every change
- Reference specs instead of duplicating content
- Use progressive enhancement pattern

## Agent Quality Standards

→ **Complete agent framework**: `.github/specs/agent-intelligence-framework.md`

Key metrics:
- Instruction files: ≤200 lines
- Prompt files: ≤400 lines
- Skill files: ≤150 lines
- Spec references: ≥3 per agent file

## Workflow Addition Checklist

When adding a new workflow:

- [ ] Add `@app.workflow("name")` decorator in `workflows.py`
- [ ] Add descriptive docstring with request body format
- [ ] Return dict with `orchestration_id` and `status`
- [ ] Update `test_workflow_count` in `tests/test_workflows.py`
- [ ] Add the workflow name to `test_new_workflows_registered`
- [ ] Run `pytest tests/ -v` to confirm all tests pass

## Security Considerations

- Never commit secrets or API keys
- Use environment variables for all configuration
- The SDK handles auth — don't add custom auth logic
- Never log sensitive request body data

## References

→ **Architecture**: `/docs/specifications/architecture.md`  
→ **Build & deployment**: `/docs/specifications/build-deployment.md`  
→ **Repository spec**: `.github/specs/business-infinity-repository.md`  
→ **Agent framework**: `.github/specs/agent-intelligence-framework.md`  
→ **Python standards**: `.github/instructions/python.instructions.md`  
→ **Azure Functions patterns**: `.github/instructions/azure-functions.instructions.md`
