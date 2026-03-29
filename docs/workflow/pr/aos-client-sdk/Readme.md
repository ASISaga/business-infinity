# aos-client-sdk — Boardroom Workflow SDK Extensions

## Objective

Extend the AOS Client SDK to support boardroom workflow orchestration,
including MCP app payload delivery, workflow YAML loading, and step navigation
for the pitch-orchestration workflow pattern.

## Requirements

### 1. MCP App Payload API

Add `send_app_payload()` to the client interface:

```python
await request.client.send_app_payload(
    app_id="boardroom_ui",
    payload={
        "narrative": "...",
        "actions": [...],
        "navigation": {"next": "step_id", "back": "step_id"},
    },
)
```

This sends the payload to the connected client session via the AOS SSE
transport layer.

### 2. Workflow YAML Loader

Add a utility for loading and validating boardroom workflow YAML files:

```python
from aos_client.workflow import load_workflow_yaml

workflow = load_workflow_yaml("docs/workflow/samples/pitch.yaml")
step = workflow.get_step("paul_graham_intro")
```

Validation must ensure:
- All steps contain a `narrative` field
- All steps contain an `actions` array (may be empty)
- Navigation references valid step IDs
- Workflow has a `workflow_id` and `version`

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

## Dependencies

- `pyyaml` — YAML parsing for workflow definitions
- `jsonschema` — Workflow YAML validation against boardroom schema

## References

→ **Backend prompt**: `docs/workflow/prompts/backend.md`
→ **Boardroom schema**: `docs/workflow/boardroom.yaml`
→ **Pitch workflow**: `docs/workflow/samples/pitch.yaml`
→ **Repository spec**: `.github/specs/repository.md`