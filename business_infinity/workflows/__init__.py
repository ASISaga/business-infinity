"""BusinessInfinity workflows package.

Registers all workflow modules with the shared ``aos_app`` instance and
re-exports utilities for backward compatibility.

Usage::

    from business_infinity.workflows import aos_app

    # function_app.py:
    import azure.functions as func
    bp = aos_app.get_blueprint()
    app = func.FunctionApp()
    app.register_blueprint(bp)
"""

from __future__ import annotations

from business_infinity.app_instance import aos_app

# Trigger all @aos_app.workflow, @aos_app.on_orchestration_update, and
# @aos_app.mcp_tool registrations by importing the aggregator module.
from business_infinity.workflows import _definitions  # noqa: F401

# Backward-compatible utility re-exports
from business_infinity.workflows._utils import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    CSuiteAgentSelector,
    select_c_suite_agents,
)

# Re-export workflow_orchestration for direct access
from business_infinity.workflows.orchestration import workflow_orchestration
from business_infinity.workflows.debate import BoardroomDebateWorkflows as _BoardroomDebateWorkflows


async def boardroom_debate(request):
    """Boardroom debate entry point via the workflows package.

    Calls ``select_c_suite_agents`` through this module's namespace so that
    tests can monkeypatch ``business_infinity.workflows.select_c_suite_agents``
    to inject specific agent sets without touching ``CSuiteAgentSelector``.
    """
    agents = await select_c_suite_agents(request.client)
    return await _BoardroomDebateWorkflows.debate(request, agents=agents)

app = aos_app  # pylint: disable=invalid-name

__all__ = [
    "aos_app",
    "app",
    "C_SUITE_TYPES",
    "C_SUITE_AGENT_IDS",
    "CSuiteAgentSelector",
    "select_c_suite_agents",
    "boardroom_debate",
    "workflow_orchestration",
]
