"""Strategic orchestration workflows for BusinessInfinity.

Implements the three core perpetual C-suite orchestrations: strategic review,
market analysis, and budget approval.  Each workflow is wrapped with the
``@aos_app.workflow`` blueprint decorator for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app
from business_infinity.workflow_utils import (
    CSuiteAgentSelector,
    OrchestrationUpdateHandlers,
    c_suite_orchestration,
)

logger = logging.getLogger(__name__)


# ── Strategic Orchestration Workflows ────────────────────────────────────────


class StrategicWorkflows:
    """C-suite strategic orchestration business logic.

    Encapsulates the three core perpetual orchestrations: strategic review,
    market analysis, and budget approval.
    """

    @staticmethod
    async def strategic_review(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a perpetual strategic review orchestration with C-suite agents."""
        return await c_suite_orchestration(
            request,
            agent_filter=lambda a: True,
            purpose="Drive strategic review and continuous organisational improvement",
            purpose_scope="C-suite strategic alignment and cross-functional coordination",
        )

    @staticmethod
    async def market_analysis(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a perpetual market analysis orchestration led by the CMO agent."""
        agents = await CSuiteAgentSelector.select(request.client)
        agent_ids = [a.agent_id for a in agents if a.agent_type == "CMOAgent"]

        ceo = [a for a in agents if a.agent_id == "ceo"]
        if ceo and ceo[0].agent_id not in agent_ids:
            agent_ids.insert(0, ceo[0].agent_id)

        if not agent_ids:
            raise ValueError("No CMO or CEO agents available in the catalog")

        status = await request.client.start_orchestration(
            agent_ids=agent_ids,
            purpose="Continuously analyse markets and surface competitive insights",
            purpose_scope="Market intelligence, competitor monitoring, and opportunity identification",
            context={
                "market": request.body.get("market", ""),
                "competitors": request.body.get("competitors", []),
            },
            workflow="hierarchical",
        )
        logger.info(
            "Market analysis orchestration started: %s",
            status.orchestration_id,
        )
        return {
            "orchestration_id": status.orchestration_id,
            "status": status.status.value,
        }

    @staticmethod
    async def budget_approval(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a perpetual budget governance orchestration."""
        agents = await CSuiteAgentSelector.select(request.client)
        agent_ids = [
            a.agent_id for a in agents if a.agent_id in ("ceo", "cfo")
        ]

        if not agent_ids:
            raise ValueError("CEO and/or CFO agents not available in the catalog")

        status = await request.client.start_orchestration(
            agent_ids=agent_ids,
            purpose="Govern budget allocation and ensure fiscal responsibility",
            purpose_scope="Financial governance, budget oversight, and resource allocation",
            context={
                "department": request.body.get("department", ""),
                "amount": request.body.get("amount", 0),
                "justification": request.body.get("justification", ""),
            },
            workflow="sequential",
        )
        logger.info(
            "Budget governance orchestration started: %s",
            status.orchestration_id,
        )
        return {
            "orchestration_id": status.orchestration_id,
            "status": status.status.value,
        }


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("strategic-review")
async def strategic_review(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual strategic review orchestration with C-suite agents.

    Request body::

        {"quarter": "Q1-2026", "focus_areas": ["revenue", "growth"]}
    """
    return await StrategicWorkflows.strategic_review(request)


@aos_app.workflow("market-analysis")
async def market_analysis(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual market analysis orchestration led by the CMO agent.

    Request body::

        {"market": "EU SaaS", "competitors": ["AcmeCorp", "Globex"]}
    """
    return await StrategicWorkflows.market_analysis(request)


@aos_app.workflow("budget-approval")
async def budget_approval(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual budget governance orchestration with C-suite leadership.

    Request body::

        {"department": "Marketing", "amount": 500000, "justification": "Q2 campaign"}
    """
    return await StrategicWorkflows.budget_approval(request)


@aos_app.on_orchestration_update("strategic-review")
async def handle_strategic_review_update(update) -> None:
    """Handle intermediate updates from strategic review orchestrations."""
    await OrchestrationUpdateHandlers.strategic_review(update)
