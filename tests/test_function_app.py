"""Tests for Azure Functions entrypoint wiring."""

import function_app
from azure.functions.decorators.function_app import FunctionApp


def test_function_app_exports_app_object() -> None:
    """The runtime-discoverable app object is exported."""
    assert isinstance(function_app.app, FunctionApp)


def test_function_app_only_exposes_single_function_app_instance() -> None:
    """Avoid duplicate top-level FunctionApp instances during indexing."""
    assert not hasattr(function_app, "functions")
