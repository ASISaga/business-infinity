"""Pitch delivery orchestration workflows for BusinessInfinity.

Orchestrates the Business Infinity pitch as an interactive narrative delivered
step-by-step through the boardroom interface.  Wrapped with ``@aos_app.workflow``
blueprint decorators for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app
from business_infinity.boardroom import (
    PITCH_ORCHESTRATION_PURPOSE,
    PITCH_ORCHESTRATION_SCOPE,
    PITCH_STEP_IDS,
    BoardroomStateManager,
)
from business_infinity.workflows._utils import CSuiteAgentSelector, OwnerStateLoader

logger = logging.getLogger(__name__)


# ── Pitch Orchestration Workflows ────────────────────────────────────────────


class PitchWorkflows:
    """Pitch delivery orchestration business logic.

    Orchestrates the Business Infinity pitch as an interactive narrative
    delivered step-by-step through the boardroom interface.
    """

    @staticmethod
    async def orchestrate(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a pitch delivery orchestration through the boardroom interface."""
        agents = await CSuiteAgentSelector.select(request.client)

        founder_ids = [
            a.agent_id for a in agents if a.agent_id == "founder"
        ]
        ceo_ids = [a.agent_id for a in agents if a.agent_id == "ceo"]
        agent_ids = founder_ids or ceo_ids

        if not agent_ids:
            raise ValueError(
                "Founder or CEO agent not available for pitch delivery"
            )

        step_id = request.body.get("step_id", PITCH_STEP_IDS[0])
        boardroom_state = BoardroomStateManager.get_boardroom_state_or_default()
        company_manifest = BoardroomStateManager.load_company_manifest()
        product_manifest = BoardroomStateManager.load_product_manifest()
        owner_agent_id = agent_ids[0]
        owner_state = OwnerStateLoader.load_or_default(
            owner_agent_id, "pitch-orchestration"
        )

        status = await request.client.start_orchestration(
            agent_ids=agent_ids,
            purpose=PITCH_ORCHESTRATION_PURPOSE,
            purpose_scope=PITCH_ORCHESTRATION_SCOPE,
            context={
                "workflow_id": "pitch_business_infinity",
                "step_id": step_id,
                "step_ids": PITCH_STEP_IDS,
                "session_id": request.body.get("session_id", ""),
                "company_purpose": request.body.get("company_purpose", ""),
                "app_id": "boardroom_ui",
                "boardroom_state": boardroom_state,
                "company_manifest": company_manifest,
                "product_manifest": product_manifest,
                **owner_state,
            },
        )
        logger.info(
            "Pitch orchestration started: %s | step=%s | agent=%s",
            status.orchestration_id,
            step_id,
            agent_ids,
        )
        return {
            "orchestration_id": status.orchestration_id,
            "status": status.status.value,
            "step_id": step_id,
            "total_steps": len(PITCH_STEP_IDS),
        }

    @staticmethod
    async def handle_update(update) -> None:
        """Handle intermediate updates from pitch orchestrations."""
        logger.info(
            "Pitch update from agent %s: step=%s",
            getattr(update, "agent_id", "unknown"),
            getattr(update, "output", ""),
        )


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("pitch-orchestration")
async def pitch_orchestration(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a pitch delivery orchestration through the boardroom interface.

    Request body::

        {
            "step_id": "paul_graham_intro",
            "session_id": "optional-session-id",
            "company_purpose": "Deliver reliable innovation that earns lasting trust"
        }
    """
    return await PitchWorkflows.orchestrate(request)


@aos_app.on_orchestration_update("pitch-orchestration")
async def handle_pitch_update(update) -> None:
    """Handle intermediate updates from pitch orchestrations."""
    await PitchWorkflows.handle_update(update)
