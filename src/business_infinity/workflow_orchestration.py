"""Generic workflow orchestration for BusinessInfinity.

A single entry point that drives any registered structured workflow.  The
``workflow_id`` in the request body selects which YAML-defined workflow to run.
The owner agent from the registry conducts the conversation.  Wrapped with
``@aos_app.workflow`` blueprint decorators for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app
from business_infinity.boardroom import (
    WORKFLOW_REGISTRY,
    BoardroomStateManager,
    get_workflow_metadata,
    get_workflow_step_ids,
)
from business_infinity.workflow_utils import OwnerStateLoader

logger = logging.getLogger(__name__)


# ── Generic Workflow Orchestration ───────────────────────────────────────────


class GenericWorkflowOrchestration:
    """Generic workflow orchestration business logic.

    A single entry point that drives any registered structured workflow.
    The workflow_id in the request body selects which YAML-defined workflow
    to run.  The owner agent from the registry conducts the conversation.
    """

    @staticmethod
    async def orchestrate(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a structured workflow orchestration through the boardroom interface."""
        workflow_id = request.body.get("workflow_id", "")
        if not workflow_id:
            raise ValueError("workflow_id is required in request body")

        try:
            metadata = get_workflow_metadata(workflow_id)
        except KeyError:
            registered = list(WORKFLOW_REGISTRY.keys())
            raise ValueError(
                f"Unknown workflow_id '{workflow_id}'. "
                f"Registered workflows: {registered}"
            )

        owner_agent_id = metadata["owner"]

        all_agents = await request.client.list_agents()
        all_by_id = {a.agent_id: a for a in all_agents}

        agent_ids: List[str] = []
        if owner_agent_id in all_by_id:
            agent_ids = [owner_agent_id]
        elif "ceo" in all_by_id:
            agent_ids = ["ceo"]
            logger.warning(
                "Owner agent '%s' not found; falling back to CEO for workflow '%s'",
                owner_agent_id,
                workflow_id,
            )

        if not agent_ids:
            raise ValueError(
                f"Owner agent '{owner_agent_id}' and CEO fallback not available "
                f"for workflow '{workflow_id}'"
            )

        try:
            step_ids = get_workflow_step_ids(workflow_id)
        except NotImplementedError:
            step_ids = []
        step_id = request.body.get(
            "step_id", step_ids[0] if step_ids else ""
        )

        boardroom_state = BoardroomStateManager.get_boardroom_state_or_default()
        company_manifest = BoardroomStateManager.load_company_manifest()
        product_manifest = BoardroomStateManager.load_product_manifest()
        owner_state = OwnerStateLoader.load_or_default(
            owner_agent_id, workflow_id
        )

        status = await request.client.start_orchestration(
            agent_ids=agent_ids,
            purpose=metadata["purpose"],
            purpose_scope=metadata["scope"],
            context={
                "workflow_id": workflow_id,
                "step_id": step_id,
                "step_ids": step_ids,
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
            "Workflow orchestration started: %s | workflow=%s | step=%s | agent=%s",
            status.orchestration_id,
            workflow_id,
            step_id,
            agent_ids,
        )
        return {
            "orchestration_id": status.orchestration_id,
            "status": status.status.value,
            "workflow_id": workflow_id,
            "owner": owner_agent_id,
            "step_id": step_id,
            "total_steps": len(step_ids),
        }

    @staticmethod
    async def handle_update(update) -> None:
        """Handle intermediate updates from generic workflow orchestrations."""
        logger.info(
            "Workflow update from agent %s: %s",
            getattr(update, "agent_id", "unknown"),
            getattr(update, "output", ""),
        )


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("workflow-orchestration")
async def workflow_orchestration(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a structured workflow orchestration through the boardroom interface.

    Request body::

        {
            "workflow_id": "pitch_business_infinity",
            "step_id": "paul_graham_intro",
            "session_id": "optional-session-id",
            "company_purpose": "Deliver reliable innovation that earns lasting trust"
        }
    """
    return await GenericWorkflowOrchestration.orchestrate(request)


@aos_app.on_orchestration_update("workflow-orchestration")
async def handle_workflow_update(update) -> None:
    """Handle intermediate updates from generic workflow orchestrations."""
    await GenericWorkflowOrchestration.handle_update(update)
