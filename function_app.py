"""BusinessInfinity Azure Functions entry point."""

from business_infinity.workflows import app  # noqa: F401

functions = app.get_functions()
