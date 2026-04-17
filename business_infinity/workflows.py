"""Compatibility exports for BusinessInfinity workflow registration."""

from __future__ import annotations

from function_app import app

from business_infinity.workflow_definitions import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    select_c_suite_agents,
)

__all__ = ["app", "C_SUITE_TYPES", "C_SUITE_AGENT_IDS", "select_c_suite_agents"]
