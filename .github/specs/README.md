# Agent System Specifications

This directory contains specifications and frameworks for the agent intelligence system.

## Files

### Agent System Specifications

- **`agent-intelligence-framework.md`** - Complete reusable framework for establishing Copilot agent ecosystems
  - Five-pillar structure (agents, instructions, prompts, skills, copilot-instructions.md)
  - Tool leverage patterns (reference, don't duplicate)
  - Validation workflows
  - Context window optimization

- **`spec-driven-development.md`** - Specification-Driven Development (SDD) workflow
  - speckit commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`)
  - Feature directory structure (`specs/NNN-slug/`)
  - Constitutional principles (Nine Articles) and gate definitions
  - Validation scripts and quality standards

### Repository-Specific Specifications

- **`repository.md`** - Repository-specific spec (one per repository, same standard name)
  - Repository name, description, and role in the ecosystem
  - Technology stack and coding patterns
  - Testing and validation workflows
  - Key design principles for agents and contributors

## Purpose

Specifications define **how** systems work and **what** patterns to follow. Unlike instructions (which are path-activated for specific file types), specs are reference documents providing detailed technical specifications.

New specs are created using the Spec Manager Agent via speckit commands.

→ **Create a spec**: `.github/agents/spec-manager.agent.md`
→ **SDD workflow**: `.github/specs/spec-driven-development.md`

## Usage

Reference these specs when:
- Creating new agents, prompts, or skills
- Understanding system architecture
- Implementing validation workflows
- Adapting system to new repositories
- Learning repository-specific patterns
- Creating or updating feature specifications

→ **Agent philosophy**: `.github/docs/agent-philosophy.md`
→ **Documentation**: `.github/docs/`
→ **Instructions**: `.github/instructions/`
