# GitHub Copilot Agent Intelligence System

This repository uses a structured GitHub Copilot agent intelligence system for optimal AI-assisted development.

→ **Repository-specific details**: `.github/specs/business-infinity-repository.md`

## Repository: BusinessInfinity

A lean Python Azure Functions application powered by the **Agent Operating System (AOS)**. Business logic lives here; all infrastructure (Azure Functions scaffolding, Service Bus, auth, agent lifecycle) is delegated to `aos-client-sdk`.

**Tech stack**: Python 3.10+, `aos-client-sdk`, pytest, pylint, Azure Developer CLI

## Directory Structure

```
.github/
├── copilot-instructions.md     # This file - high-level architecture
├── instructions/               # Path-activated coding standards (auto-load by glob)
├── specs/                      # Detailed specifications & frameworks
├── docs/                       # Implementation guides & references
├── agents/                     # Custom agents (*.agent.md)
├── prompts/                    # Agent prompts (*.prompt.md)
└── skills/                     # Agent skills (SKILL.md + scripts)
```

- **Instructions** auto-load when editing matching file types
- **Specs** define frameworks; **Docs** provide guides
- **Agents/Prompts/Skills** provide executable capabilities
- **Validation** via agent quality scripts ensures continuous quality

→ **Framework**: `.github/specs/agent-intelligence-framework.md`  
→ **Philosophy**: `.github/docs/agent-philosophy.md`  
→ **System overview**: `.github/docs/agent-system-overview.md`  
→ **Documentation index**: `.github/docs/README.md`

## Core Principles

1. **Tool Leverage** — Orchestrate existing automation, never duplicate
2. **Path Specificity** — Instructions auto-load based on file patterns
3. **Context Efficiency** — Reference specs/docs, eliminate redundancy
4. **Ouroboros Pattern** — Agents evolve themselves through continuous use

## Tools & Validation

```bash
pip install -e ".[dev]"                                        # Install dev dependencies
pytest tests/ -v                                               # Run all tests
pylint src/business_infinity/                                  # Lint
./.github/skills/agent-evolution-agent/scripts/audit-agent-quality.sh  # Validate agent quality
```

→ **Complete tool reference**: `.github/docs/conventional-tools.md`  
→ **Dogfooding guide**: `.github/docs/dogfooding-guide.md`  
→ **CI/CD workflow**: `.github/workflows/ci.yml`

## Bootstrapping New Repositories

1. **Use onboarding agent**: Invoke `repository-onboarding` agent
2. **Or manual setup**: Follow `.github/prompts/repository-onboarding.prompt.md`
3. **Or copy templates**: Extract from `.github/specs/agent-intelligence-framework.md`

→ **Extraction guide**: `.github/docs/TEMPLATE-EXTRACTION-GUIDE.md`

## Key References

| Resource | Location |
|----------|----------|
| Repository spec | `.github/specs/business-infinity-repository.md` |
| Python standards | `.github/instructions/python.instructions.md` |
| Azure Functions patterns | `.github/instructions/azure-functions.instructions.md` |
| Agent framework | `.github/specs/agent-intelligence-framework.md` |
| Conventional tools | `.github/docs/conventional-tools.md` |
| Path-specific mechanism | `.github/docs/path-specific-instructions.md` |
