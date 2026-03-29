# aos-client-sdk — Boardroom Workflow SDK Extensions

## Objective

Extend the AOS Client SDK to support the generic boardroom workflow system,
including MCP app payload delivery, workflow YAML loading with owner agent
resolution, step navigation, and validation against the boardroom schema.

## Context

The boardroom supports multiple YAML-defined workflows, each owned by a
specific agent.  The SDK provides the runtime infrastructure to load any
workflow, validate it, navigate between steps, and deliver MCP app payloads
to the frontend.  The same SDK APIs support both structured workflows and
dynamic CXO discussions.

## Requirements

### 1. MCP App Payload API

Add `send_app_payload()` to the client interface:

```python
await request.client.send_app_payload(
    app_id="boardroom_ui",
    payload={
        "narrative": "...",
        "response": "...",
        "actions": [...],
        "navigation": {"next": "step_id", "back": "step_id"},
    },
)
```

This sends the payload to the connected client session via the AOS SSE
transport layer.  The payload is also routed to `subconscious.asisaga.com`
for persistence.

### 2. Workflow YAML Loader

Add a utility for loading and validating any boardroom workflow YAML file:

```python
from aos_client.workflow import load_workflow_yaml

workflow = load_workflow_yaml("docs/workflow/samples/pitch.yaml")
step = workflow.get_step("paul_graham_intro")
owner = workflow.owner  # "founder"
workflow_id = workflow.workflow_id  # "pitch_business_infinity"
```

The loader must support all registered workflows:
- `pitch.yaml` (owner: founder)
- `onboarding.yaml` (owner: coo)
- `marketing.yaml` (owner: cmo)
- `crisis-response.yaml` (owner: ceo)
- `strategic-review.yaml` (owner: ceo)
- `product-launch.yaml` (owner: ceo)

Validation must ensure:
- All steps contain a `narrative` field
- All steps contain a `response` field
- All steps contain an `actions` array (may be empty)
- Navigation references valid step IDs
- Workflow has `workflow_id`, `version`, and `owner`

### 3. Step Navigation Helper

Add a step navigation helper that resolves `next`/`back` commands:

```python
from aos_client.workflow import StepNavigator

navigator = StepNavigator(workflow)
next_step = navigator.resolve("cmd:next", current_step_id="paul_graham_intro")
# → "paul_graham_dataset"
```

### 4. WorkflowRequest Extensions

Extend `WorkflowRequest` to expose the workflow YAML context when available:
- `request.workflow_steps` — loaded steps from the associated YAML
- `request.current_step_id` — current step from session state
- `request.workflow_owner` — owner agent ID from the YAML
- `request.workflow_id` — workflow identifier

### 5. Workflow Registry Integration

Provide a method to discover available workflows:

```python
from aos_client.workflow import list_available_workflows

workflows = list_available_workflows()
# [{"workflow_id": "pitch_business_infinity", "owner": "founder", ...}, ...]
```

## Dependencies

- `pyyaml` — YAML parsing for workflow definitions
- `jsonschema` — Workflow YAML validation against boardroom schema

## References

→ **Backend prompt**: `docs/workflow/prompts/backend.md`
→ **Boardroom schema**: `docs/workflow/boardroom.yaml`
→ **Workflow YAML samples**: `docs/workflow/samples/`
→ **Repository spec**: `.github/specs/repository.md`
→ **Multi-repo roadmap**: `docs/multi-repository-implementation.md`