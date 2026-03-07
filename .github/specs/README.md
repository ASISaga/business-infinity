# Agent System Specifications

This directory contains specifications and frameworks for the agent intelligence system.

## Files

### Agent System Specifications

- **`agent-intelligence-framework.md`** - Complete reusable framework for establishing Copilot agent ecosystems
  - Five-pillar structure (agents, instructions, prompts, skills, copilot-instructions.md)
  - Tool leverage patterns (reference, don't duplicate)
  - Validation workflows
  - Context window optimization

### Repository-Specific Specifications

- **`business-infinity-repository.md`** - BusinessInfinity repository specifics
  - Repository role in the AOS ecosystem
  - Technology stack (Python 3.10+, aos-client-sdk, pytest, pylint)
  - Directory structure and core patterns
  - Testing and validation workflows
  - Key design principles

## Purpose

Specifications define **how** systems work and **what** patterns to follow. Unlike instructions (which are path-activated for specific file types), specs are reference documents providing detailed technical specifications.

## Usage

Reference these specs when:
- Creating new agents, prompts, or skills
- Understanding system architecture
- Implementing validation workflows
- Adapting system to new repositories
- Learning repository-specific patterns

→ **Agent philosophy**: `.github/docs/agent-philosophy.md`  
→ **Documentation**: `.github/docs/`  
→ **Instructions**: `.github/instructions/`
