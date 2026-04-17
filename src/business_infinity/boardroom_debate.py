"""Boardroom debate orchestration workflows for BusinessInfinity.

Implements the core BusinessInfinity philosophy: decision-tree debates where
CXO agents propose domain-specific pathways, score them for resonance, and
converge on autonomous action.  Wrapped with ``@aos_app.workflow`` blueprint
decorators for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app
from business_infinity.boardroom import (
    BOARDROOM_DEBATE_PURPOSE,
    BOARDROOM_DEBATE_SCOPE,
    BoardroomStateManager,
    CXO_DOMAINS,
)
from business_infinity.workflow_utils import CSuiteAgentSelector

logger = logging.getLogger(__name__)


# ── Boardroom Debate Workflows ───────────────────────────────────────────────


class BoardroomDebateWorkflows:
    """Boardroom debate orchestration business logic.

    Implements the core BusinessInfinity philosophy: decision tree debates
    where CXO agents propose domain-specific pathways, score them for
    resonance, and converge on autonomous action.
    """

    @staticmethod
    async def debate(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a purpose-driven boardroom debate orchestration."""
        agents = await CSuiteAgentSelector.select(request.client)
        agent_ids = [a.agent_id for a in agents]

        if not agent_ids:
            raise ValueError("No C-suite agents available for boardroom debate")

        domain_context = {
            aid: CXO_DOMAINS[aid]
            for aid in agent_ids
            if aid in CXO_DOMAINS
        }

        boardroom_state = BoardroomStateManager.get_boardroom_state_or_default()
        company_manifest = BoardroomStateManager.load_company_manifest()
        product_manifest = BoardroomStateManager.load_product_manifest()
        agent_contexts = BoardroomStateManager.get_all_agent_contexts()
        agent_contents = BoardroomStateManager.get_all_agent_contents()
        agent_company_states = BoardroomStateManager.get_all_agent_company_states()
        agent_product_states = BoardroomStateManager.get_all_agent_product_states()

        status = await request.client.start_orchestration(
            agent_ids=agent_ids,
            purpose=BOARDROOM_DEBATE_PURPOSE,
            purpose_scope=BOARDROOM_DEBATE_SCOPE,
            context={
                "event": request.body.get("event", ""),
                "event_source": request.body.get("event_source", ""),
                "company_purpose": request.body.get("company_purpose", ""),
                "debate_context": request.body.get("context", {}),
                "cxo_domains": domain_context,
                "boardroom_state": boardroom_state,
                "company_manifest": company_manifest,
                "product_manifest": product_manifest,
                "agent_contexts": agent_contexts,
                "agent_contents": agent_contents,
                "agent_company_states": agent_company_states,
                "agent_product_states": agent_product_states,
            },
        )
        logger.info(
            "Boardroom debate orchestration started: %s | agents=%s",
            status.orchestration_id,
            agent_ids,
        )
        return {
            "orchestration_id": status.orchestration_id,
            "status": status.status.value,
        }

    @staticmethod
    async def handle_update(update) -> None:
        """Handle intermediate updates from boardroom debate orchestrations."""
        logger.info(
            "Boardroom debate update from agent %s: %s",
            getattr(update, "agent_id", "unknown"),
            getattr(update, "output", ""),
        )


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("boardroom-debate")
async def boardroom_debate(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a purpose-driven boardroom debate orchestration.

    Request body::

        {
            "event": "Competitor launches aggressive campaign",
            "event_source": "market",
            "company_purpose": "Deliver reliable innovation that earns lasting trust",
            "context": {"churn_rate": 0.12, "market": "EU SaaS"}
        }
    """
    return await BoardroomDebateWorkflows.debate(request)


@aos_app.on_orchestration_update("boardroom-debate")
async def handle_boardroom_debate_update(update) -> None:
    """Handle intermediate updates from boardroom debate orchestrations."""
    await BoardroomDebateWorkflows.handle_update(update)
