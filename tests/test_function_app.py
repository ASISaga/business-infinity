"""Tests for Azure Functions entrypoint wiring."""

import function_app
from azure.functions.decorators.function_app import FunctionApp


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
