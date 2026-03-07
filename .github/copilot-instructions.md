# GitHub Copilot Agent Intelligence System

This repository uses a structured GitHub Copilot agent intelligence system for optimal AI-assisted development.

→ **Repository-specific details**: `.github/specs/repository.md`

## Directory Structure

```
.github/
├── copilot-instructions.md     # This file - high-level architecture
├── instructions/               # Path-activated coding standards (auto-load by glob)
├── specs/                      # Detailed specifications & frameworks
│   ├── repository.md           #   ← Repository-specific spec (update per repo)
│   └── agent-intelligence-framework.md
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

→ **Repository tools & commands**: `.github/specs/repository.md`  
→ **Complete tool reference**: `.github/docs/conventional-tools.md`  
→ **Dogfooding guide**: `.github/docs/dogfooding-guide.md`  
→ **CI/CD workflow**: `.github/workflows/ci.yml`

```bash
# Agent quality validation (repository-agnostic)
./.github/skills/agent-evolution-agent/scripts/audit-agent-quality.sh
```

## Bootstrapping New Repositories

1. **Use onboarding agent**: Invoke `repository-onboarding` agent
2. **Or manual setup**: Follow `.github/prompts/repository-onboarding.prompt.md`
3. **Or copy templates**: Extract from `.github/specs/agent-intelligence-framework.md`

→ **Extraction guide**: `.github/docs/TEMPLATE-EXTRACTION-GUIDE.md`

## Key References

| Resource | Location |
|----------|----------|
| Repository spec | `.github/specs/repository.md` |
| Agent framework | `.github/specs/agent-intelligence-framework.md` |
| Conventional tools | `.github/docs/conventional-tools.md` |
| Path-specific mechanism | `.github/docs/path-specific-instructions.md` |
