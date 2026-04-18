"""Additional Azure Function blueprints for repository capabilities."""

from __future__ import annotations

import json
from typing import Any, Dict

import azure.functions as func

from business_infinity.boardroom import (
    get_workflow_metadata,
    get_workflow_step_ids,
    list_registered_workflows,
)
from business_infinity.seo import get_category_by_slug, total_query_count


def _json_response(payload: Dict[str, Any], status_code: int = 200) -> func.HttpResponse:
    """Create a JSON HTTP response."""
    return func.HttpResponse(
        body=json.dumps(payload),
        status_code=status_code,
        mimetype="application/json",
    )


boardroom_blueprint = func.Blueprint()
seo_blueprint = func.Blueprint()


@boardroom_blueprint.route(route="boardroom/workflows", methods=["GET"])
def boardroom_workflows(_req: func.HttpRequest) -> func.HttpResponse:
    """Return all registered boardroom workflows."""
    workflows = list_registered_workflows()
    return _json_response(
        {
            "count": len(workflows),
            "workflows": workflows,
        }
    )


@boardroom_blueprint.route(route="boardroom/workflows/{workflow_id}", methods=["GET"])
def boardroom_workflow_details(req: func.HttpRequest) -> func.HttpResponse:
    """Return metadata and step IDs for a single workflow."""
    workflow_id = req.route_params.get("workflow_id", "")
    if not workflow_id:
        return _json_response({"error": "workflow_id route parameter is required"}, 400)

    try:
        metadata = get_workflow_metadata(workflow_id)
        step_ids = get_workflow_step_ids(workflow_id)
    except KeyError:
        return _json_response({"error": f"Unknown workflow_id '{workflow_id}'"}, 404)

    return _json_response(
        {
            "workflow_id": workflow_id,
            "metadata": metadata,
            "step_ids": step_ids,
        }
    )


@seo_blueprint.route(route="seo/summary", methods=["GET"])
def seo_summary(_req: func.HttpRequest) -> func.HttpResponse:
    """Return SEO taxonomy summary metrics."""
    return _json_response(
        {
            "total_queries": total_query_count(),
        }
    )


@seo_blueprint.route(route="seo/categories/{slug}", methods=["GET"])
def seo_category_details(req: func.HttpRequest) -> func.HttpResponse:
    """Return a single SEO taxonomy category by slug."""
    slug = req.route_params.get("slug", "")
    if not slug:
        return _json_response({"error": "slug route parameter is required"}, 400)

    try:
        category = get_category_by_slug(slug)
    except KeyError:
        return _json_response({"error": f"Unknown category slug '{slug}'"}, 404)

    return _json_response(
        {
            "slug": slug,
            "category": category,
        }
    )
