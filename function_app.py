"""Azure Functions runtime entry point for BusinessInfinity workflows."""

from aos_client import AOSApp
from aos_client.observability import ObservabilityConfig

app = AOSApp(
    name="business-infinity",
    observability=ObservabilityConfig(
        structured_logging=True,
        correlation_tracking=True,
        health_checks=["aos", "service-bus"],
    ),
)

# Import side effects register all workflow decorators onto the shared app.
from business_infinity import workflow_definitions  # noqa: E402,F401  pylint: disable=wrong-import-position,unused-import

functions = app.get_functions()
