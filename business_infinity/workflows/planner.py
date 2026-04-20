"""Microsoft Planner workflow wrappers for BusinessInfinity.

Exposes two AOS workflows that allow CXOs (or automated agents) to plan and
monitor responsibilities via Microsoft Planner / Microsoft Graph:

``sync-responsibilities``
    Create or update Planner plans, buckets, and tasks from the JSON-LD
    responsibility files owned by a given CXO agent.

``get-responsibilities-status``
    Query task completion progress for a CXO's responsibility plan and
    return an aggregate summary.

Request body schema (``sync-responsibilities``)
------------------------------------------------
.. code-block:: json

    {
        "agent_id": "ceo",
        "group_id": "<microsoft-365-group-id>",
        "dimension": "entrepreneur"
    }

``agent_id`` is required.  ``group_id`` defaults to the ``PLANNER_GROUP_ID``
or ``PLANNER_GROUP_ID_{ROLE}`` environment variable.  ``dimension`` is optional;
omit to sync all three dimensions.

Request body schema (``get-responsibilities-status``)
------------------------------------------------------
.. code-block:: json

    {
        "role": "CEO",
        "plan_id": "<planner-plan-id>"
    }

Provide either ``role`` (resolved to the matching plan title) or ``plan_id``
directly.
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any, Dict, Optional

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app
from business_infinity.planner import PlannerClient, PlannerMonitor, PlannerSync

logger = logging.getLogger(__name__)


# ── Workflow classes ──────────────────────────────────────────────────────────


class PlannerWorkflows:
    """Business logic for Planner planning and monitoring workflows."""

    @staticmethod
    async def sync_responsibilities(request: WorkflowRequest) -> Dict[str, Any]:
        """Sync CXO responsibilities from JSON-LD files into Microsoft Planner.

        Reads ``agent_id``, ``group_id`` (optional), and ``dimension``
        (optional) from ``request.body``.
        """
        agent_id: str = request.body["agent_id"]
        group_id: Optional[str] = request.body.get("group_id")
        dimension: Optional[str] = request.body.get("dimension")

        client = PlannerClient()
        syncer = PlannerSync(client)

        if dimension:
            result = await syncer.sync_dimension(agent_id, dimension, group_id=group_id)
        else:
            result = await syncer.sync_agent(agent_id, group_id=group_id)

        return asdict(result)

    @staticmethod
    async def get_responsibilities_status(request: WorkflowRequest) -> Dict[str, Any]:
        """Query task completion progress for a CXO responsibility plan.

        Reads ``role`` or ``plan_id`` from ``request.body``.
        """
        role: Optional[str] = request.body.get("role")
        plan_id: Optional[str] = request.body.get("plan_id")

        if not role and not plan_id:
            raise ValueError("Request body must include 'role' or 'plan_id'.")

        client = PlannerClient()
        monitor = PlannerMonitor(client)

        if plan_id:
            statuses = await monitor.get_plan_status(plan_id)
        else:
            statuses = await monitor.get_agent_status(role)

        if statuses is None:
            return {
                "found": False,
                "role": role,
                "message": f"No Planner plan found for role: {role}",
            }

        summary = PlannerMonitor.summarise(statuses)
        return {
            "found": True,
            "role": role,
            "plan_id": plan_id,
            "tasks": [asdict(s) for s in statuses],
            "summary": summary,
        }


# ── AOS workflow registrations ────────────────────────────────────────────────


@aos_app.workflow("sync-responsibilities")
async def sync_responsibilities(request: WorkflowRequest) -> Dict[str, Any]:
    """Sync CXO responsibilities to Microsoft Planner."""
    return await PlannerWorkflows.sync_responsibilities(request)


@aos_app.workflow("get-responsibilities-status")
async def get_responsibilities_status(request: WorkflowRequest) -> Dict[str, Any]:
    """Get task completion status for a CXO responsibility plan."""
    return await PlannerWorkflows.get_responsibilities_status(request)
