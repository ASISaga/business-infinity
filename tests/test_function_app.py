"""Tests for Azure Functions entrypoint wiring."""

import function_app


def test_function_app_exports_app_object() -> None:
    """The runtime-discoverable app object is exported."""
    assert function_app.app is not None


def test_function_app_compat_alias_points_to_same_object() -> None:
    """Backward-compatible alias references the same object."""
    assert function_app.functions is function_app.app
