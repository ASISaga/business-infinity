"""Compatibility exports for BusinessInfinity workflow registration."""

from __future__ import annotations

from business_infinity.app_instance import aos_app

from business_infinity.workflow_definitions import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    CSuiteAgentSelector,
    select_c_suite_agents,
)

app = aos_app  # pylint: disable=invalid-name

__all__ = [
    "aos_app",
    "app",
    "C_SUITE_TYPES",
    "C_SUITE_AGENT_IDS",
    "CSuiteAgentSelector",
    "select_c_suite_agents",
]
