"""Boardroom API blueprint — workflow listing and details endpoints."""

from __future__ import annotations

import azure.functions as func

from business_infinity.boardroom import WorkflowRegistryManager
from business_infinity.blueprints._helpers import json_response, require_route_param

boardroom_blueprint = func.Blueprint()


@boardroom_blueprint.route(route="boardroom/workflows", methods=["GET"])
def boardroom_workflows(_req: func.HttpRequest) -> func.HttpResponse:
    """Return all registered boardroom workflows."""
    workflows = WorkflowRegistryManager.list_all()
    return json_response(
        {
            "count": len(workflows),
            "workflows": workflows,
        }
    )


@boardroom_blueprint.route(route="boardroom/workflows/{workflow_id}", methods=["GET"])
def boardroom_workflow_details(req: func.HttpRequest) -> func.HttpResponse:
    """Return metadata and step IDs for a single workflow."""
    workflow_id, error_response = require_route_param(req, "workflow_id")
    if error_response:
        return error_response

    try:
        metadata = WorkflowRegistryManager.get_metadata(workflow_id)
        step_ids = WorkflowRegistryManager.get_step_ids(workflow_id)
    except KeyError:
        return json_response({"error": f"Unknown workflow_id '{workflow_id}'"}, 404)

    return json_response(
        {
            "workflow_id": workflow_id,
            "metadata": metadata,
            "step_ids": step_ids,
        }
    )
