"""Tests for Azure Functions entrypoint wiring."""

import function_app
from azure.functions.decorators.function_app import FunctionApp


def test_function_app_exports_app_object() -> None:
    """The runtime-discoverable app object is exported."""
    assert isinstance(function_app.app, FunctionApp)


def test_function_app_compat_alias_points_to_same_object() -> None:
    """Backward-compatible alias references the same object."""
    assert function_app.functions is function_app.app
