"""Compatibility exports for BusinessInfinity workflow registration.

This module intentionally imports :mod:`function_app` so existing imports
(`from business_infinity.workflows import app`) still initialize the shared
`AOSApp` instance before exports are accessed.
"""

from __future__ import annotations

# Ensure app initialization when using this legacy import path.
import function_app  # noqa: F401  pylint: disable=unused-import
from business_infinity.app_instance import get_app

from business_infinity.workflow_definitions import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    select_c_suite_agents,
)

app = get_app()  # pylint: disable=invalid-name

__all__ = ["app", "C_SUITE_TYPES", "C_SUITE_AGENT_IDS", "select_c_suite_agents"]
