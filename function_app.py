"""Azure Functions runtime entry point for BusinessInfinity workflows."""

from aos_client import AOSApp
from aos_client.observability import ObservabilityConfig

from business_infinity.app_instance import set_app

app = AOSApp(
    name="business-infinity",
    observability=ObservabilityConfig(
        structured_logging=True,
        correlation_tracking=True,
        health_checks=["aos", "service-bus"],
    ),
)
set_app(app)

# Deferred import is required so the shared app is initialized first. Workflow
# modules read that shared instance and register decorators at import time.
# This side-effect import is therefore part of startup sequencing: without it,
# no workflows/update handlers/MCP tools would be attached before
# ``app.get_functions()`` runs. Unused warnings are expected and suppressed.
from business_infinity import workflow_definitions  # noqa: E402,F401  pylint: disable=wrong-import-position,unused-import

functions = app.get_functions()
