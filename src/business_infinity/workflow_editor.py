"""Workflow editor service for BusinessInfinity.

Provides list, get, and save operations for step-wise editing of workflow YAML
files through the website frontend.  Wrapped with ``@aos_app.workflow`` blueprint
decorators for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app
from business_infinity.boardroom import (
    WORKFLOW_REGISTRY,
    WorkflowRegistryManager,
    WorkflowYAMLManager,
)

logger = logging.getLogger(__name__)


# ── Workflow Editor Service ──────────────────────────────────────────────────


class WorkflowEditorService:
    """Workflow editor endpoint business logic.

    Provides list, get, and save operations for step-wise editing of
    workflow YAML files through the website frontend.
    """

    @staticmethod
    async def list_workflows(request: WorkflowRequest) -> Dict[str, Any]:
        """Return metadata for all registered workflows."""
        workflows = [
            {
                "workflow_id": wf_id,
                "owner": meta["owner"],
                "yaml_path": meta["yaml_path"],
            }
            for wf_id, meta in WorkflowRegistryManager.list_all().items()
        ]
        logger.info(
            "Workflow editor list requested: %d workflows", len(workflows)
        )
        return {"workflows": workflows}

    @staticmethod
    async def get_workflow(request: WorkflowRequest) -> Dict[str, Any]:
        """Return the full structured content of a workflow for editing."""
        workflow_id = request.body.get("workflow_id", "")
        if not workflow_id:
            raise ValueError("workflow_id is required in request body")
        try:
            data = WorkflowYAMLManager.load(workflow_id)
        except KeyError:
            registered = list(WORKFLOW_REGISTRY.keys())
            raise ValueError(
                f"Unknown workflow_id '{workflow_id}'. "
                f"Registered workflows: {registered}"
            )
        logger.info(
            "Workflow editor get: %s (%d steps)",
            workflow_id,
            len(data.get("steps", {})),
        )
        return data

    @staticmethod
    async def save_workflow(request: WorkflowRequest) -> Dict[str, Any]:
        """Validate and save an updated workflow structure to its YAML file."""
        workflow_id = request.body.get("workflow_id", "")
        if not workflow_id:
            raise ValueError("workflow_id is required in request body")
        try:
            WorkflowYAMLManager.save(workflow_id, request.body)
        except KeyError:
            registered = list(WORKFLOW_REGISTRY.keys())
            raise ValueError(
                f"Unknown workflow_id '{workflow_id}'. "
                f"Registered workflows: {registered}"
            )
        step_count = len(request.body.get("steps", {}))
        logger.info(
            "Workflow editor save: %s (%d steps)",
            workflow_id,
            step_count,
        )
        return {
            "status": "saved",
            "workflow_id": workflow_id,
            "step_count": step_count,
        }


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("workflow-editor-list")
async def workflow_editor_list(request: WorkflowRequest) -> Dict[str, Any]:
    """Return metadata for all registered workflows.

    Response::

        {
            "workflows": [
                {
                    "workflow_id": "pitch_business_infinity",
                    "owner": "founder",
                    "yaml_path": "docs/workflow/samples/pitch.yaml"
                },
                ...
            ]
        }
    """
    return await WorkflowEditorService.list_workflows(request)


@aos_app.workflow("workflow-editor-get")
async def workflow_editor_get(request: WorkflowRequest) -> Dict[str, Any]:
    """Return the full structured content of a workflow for step-wise editing.

    Request body::

        {"workflow_id": "pitch_business_infinity"}
    """
    return await WorkflowEditorService.get_workflow(request)


@aos_app.workflow("workflow-editor-save")
async def workflow_editor_save(request: WorkflowRequest) -> Dict[str, Any]:
    """Validate and save an updated workflow structure to its YAML file.

    Request body mirrors the boardroom YAML schema::

        {
            "workflow_id": "pitch_business_infinity",
            "version": "1.0.0",
            "owner": "founder",
            "steps": { ... }
        }

    Response::

        {"status": "saved", "workflow_id": "pitch_business_infinity", "step_count": 9}
    """
    return await WorkflowEditorService.save_workflow(request)
