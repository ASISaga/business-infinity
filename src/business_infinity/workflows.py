"""Compatibility exports for BusinessInfinity workflow registration.

Import ``function_app`` first so the shared ``AOSApp`` instance is initialized
before these compatibility exports are accessed.
"""

from __future__ import annotations

from business_infinity.app_instance import get_app

from business_infinity.workflow_definitions import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    CSuiteAgentSelector,
    select_c_suite_agents,
)

app = get_app()  # pylint: disable=invalid-name

__all__ = [
    "app",
    "C_SUITE_TYPES",
    "C_SUITE_AGENT_IDS",
    "CSuiteAgentSelector",
    "select_c_suite_agents",
]
