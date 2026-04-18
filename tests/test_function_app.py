"""Tests for Azure Functions entrypoint wiring."""

import json
from dataclasses import dataclass, field
from typing import Dict

from azure.functions.decorators.function_app import FunctionApp

import function_app
from business_infinity.blueprints import (
    boardroom_workflow_details,
    boardroom_workflows,
    seo_category_details,
    seo_summary,
)
from business_infinity.boardroom import WorkflowRegistryManager
from business_infinity.seo import PAIN_TAXONOMY, PainTaxonomy


@dataclass
class RequestStub:
    """Minimal request stub with route params for endpoint tests."""

    route_params: Dict[str, str] = field(default_factory=dict)


def test_function_app_exports_app_object() -> None:
    """The runtime-discoverable app object is exported."""
    assert isinstance(function_app.app, FunctionApp)


def test_function_app_only_exposes_single_function_app_instance() -> None:
    """Avoid duplicate top-level FunctionApp instances during indexing."""
    assert not hasattr(function_app, "functions")


def test_function_app_registers_additional_blueprints() -> None:
    """Additional functionality blueprints are registered on the FunctionApp."""
    function_names = {
        fn.get_function_name()
        for fn in function_app.app.get_functions()
    }
    assert "boardroom_workflows" in function_names
    assert "boardroom_workflow_details" in function_names
    assert "seo_summary" in function_names
    assert "seo_category_details" in function_names
    assert "ping" in function_names


def test_boardroom_workflows_returns_registry_payload() -> None:
    """Boardroom list endpoint mirrors registry data."""
    response = boardroom_workflows(RequestStub())
    payload = json.loads(response.get_body().decode("utf-8"))
    registry = WorkflowRegistryManager.list_all()
    assert response.status_code == 200
    assert payload["count"] == len(registry)
    assert payload["workflows"] == registry


def test_boardroom_workflow_details_returns_400_when_missing_route_param() -> None:
    """Boardroom details endpoint validates workflow_id route param."""
    response = boardroom_workflow_details(RequestStub())
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 400
    assert "workflow_id route parameter is required" in payload["error"]


def test_boardroom_workflow_details_returns_404_for_unknown_workflow() -> None:
    """Boardroom details endpoint returns 404 for unknown workflow IDs."""
    response = boardroom_workflow_details(
        RequestStub(route_params={"workflow_id": "does-not-exist"})
    )
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 404
    assert "Unknown workflow_id" in payload["error"]


def test_boardroom_workflow_details_returns_metadata_for_known_workflow() -> None:
    """Boardroom details endpoint returns metadata and steps for known IDs."""
    workflow_id = next(iter(WorkflowRegistryManager.list_all()))
    response = boardroom_workflow_details(
        RequestStub(route_params={"workflow_id": workflow_id})
    )
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 200
    assert payload["workflow_id"] == workflow_id
    assert "metadata" in payload
    assert "step_ids" in payload


def test_seo_summary_returns_total_query_count() -> None:
    """SEO summary endpoint returns global taxonomy metrics."""
    response = seo_summary(RequestStub())
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 200
    assert payload["total_queries"] == PainTaxonomy.total_query_count()


def test_seo_category_details_returns_400_when_missing_slug() -> None:
    """SEO details endpoint validates slug route param."""
    response = seo_category_details(RequestStub())
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 400
    assert "slug route parameter is required" in payload["error"]


def test_seo_category_details_returns_404_for_unknown_slug() -> None:
    """SEO details endpoint returns 404 for unknown category slugs."""
    response = seo_category_details(RequestStub(route_params={"slug": "unknown"}))
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 404
    assert "Unknown category slug" in payload["error"]


def test_seo_category_details_returns_category_for_known_slug() -> None:
    """SEO details endpoint returns category payload for known slug."""
    slug = PAIN_TAXONOMY[0]["slug"]
    response = seo_category_details(RequestStub(route_params={"slug": slug}))
    payload = json.loads(response.get_body().decode("utf-8"))
    assert response.status_code == 200
    assert payload["slug"] == slug
    assert payload["category"]["slug"] == slug
