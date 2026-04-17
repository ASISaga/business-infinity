"""Shared AOS app instance for workflow registration."""

from __future__ import annotations

from aos_client import AOSApp
from aos_client.observability import ObservabilityConfig

aos_app: AOSApp = AOSApp(
    name="business-infinity",
    observability=ObservabilityConfig(
        structured_logging=True,
        correlation_tracking=True,
        health_checks=["aos", "service-bus"],
    ),
)
