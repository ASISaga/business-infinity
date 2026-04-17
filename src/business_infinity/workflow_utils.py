"""Shared utilities for BusinessInfinity workflow registration.

Provides agent-selection helpers, owner-state loading, and the reusable
C-suite orchestration template used across all workflow modules.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List

from aos_client import (
    AOSClient,
    AgentDescriptor,
    WorkflowRequest,
    workflow_template,
)

logger = logging.getLogger(__name__)


# ── C-Suite Agent Selector ───────────────────────────────────────────────────


class CSuiteAgentSelector:
    """Manages C-suite agent identification and selection from the AOS catalog.

    Provides constants for agent type matching and selection logic that
    prefers explicit agent IDs with a fallback to type-based filtering.
    """

    #: Agent types considered part of the C-suite.
    TYPES = {
        "LeadershipAgent",
        "CEOAgent",
        "CFOAgent",
        "COOAgent",
        "CMOAgent",
        "CHROAgent",
        "CTOAgent",
        "CSOAgent",
    }

    #: Preferred C-suite agent IDs for BusinessInfinity orchestrations.
    IDS = ["ceo", "cfo", "coo", "cmo", "chro", "cto", "cso"]

    @classmethod
    async def select(cls, client: AOSClient) -> List[AgentDescriptor]:
        """Select C-suite agents from the RealmOfAgents catalog.

        Returns agents matching :data:`IDS` or, if not found,
        agents whose ``agent_type`` is in :data:`TYPES`.
        """
        all_agents = await client.list_agents()

        by_id = {a.agent_id: a for a in all_agents}
        selected = [by_id[aid] for aid in cls.IDS if aid in by_id]

        if not selected:
            selected = [a for a in all_agents if a.agent_type in cls.TYPES]

        logger.info(
            "Selected %d C-suite agents: %s",
            len(selected),
            [a.agent_id for a in selected],
        )
        return selected


# Backward-compatible aliases
C_SUITE_TYPES = CSuiteAgentSelector.TYPES
C_SUITE_AGENT_IDS = CSuiteAgentSelector.IDS


async def select_c_suite_agents(client: AOSClient) -> List[AgentDescriptor]:
    """Select C-suite agents from the RealmOfAgents catalog."""
    return await CSuiteAgentSelector.select(client)


# ── Workflow Template ────────────────────────────────────────────────────────


@workflow_template
async def c_suite_orchestration(
    request: WorkflowRequest,
    agent_filter: Callable[[AgentDescriptor], bool],
    purpose: str,
    purpose_scope: str,
) -> Dict[str, Any]:
    """Reusable template for C-suite orchestrations."""
    agents = await CSuiteAgentSelector.select(request.client)
    agent_ids = [a.agent_id for a in agents if agent_filter(a)]
    if not agent_ids:
        raise ValueError("No matching agents available in the catalog")
    status = await request.client.start_orchestration(
        agent_ids=agent_ids,
        purpose=purpose,
        purpose_scope=purpose_scope,
        context=request.body,
    )
    return {"orchestration_id": status.orchestration_id, "status": status.status.value}


# ── Owner State Helper ───────────────────────────────────────────────────────


class OwnerStateLoader:
    """Loads boardroom owner state for workflow context payloads."""

    @staticmethod
    def load_or_default(
        owner_agent_id: str, workflow_label: str
    ) -> Dict[str, Dict[str, Any]]:
        """Load owner state for workflow payloads with safe defaults."""
        from business_infinity.boardroom import BoardroomStateManager  # avoid circular

        try:
            return {
                "owner_context": BoardroomStateManager.load_agent_context(
                    owner_agent_id
                ),
                "owner_content": BoardroomStateManager.load_agent_content(
                    owner_agent_id
                ),
                "owner_company_state": BoardroomStateManager.load_agent_company_state(
                    owner_agent_id
                ),
                "owner_product_state": BoardroomStateManager.load_agent_product_state(
                    owner_agent_id
                ),
            }
        except ValueError:
            logger.warning(
                "Owner state unavailable because agent '%s' is not registered in '%s'",
                owner_agent_id,
                workflow_label,
            )
        except FileNotFoundError:
            logger.warning(
                "Owner state file missing for agent '%s' in '%s'",
                owner_agent_id,
                workflow_label,
            )
        return {
            "owner_context": {},
            "owner_content": {},
            "owner_company_state": {},
            "owner_product_state": {},
        }


def _load_owner_state_or_default(
    owner_agent_id: str, workflow_label: str
) -> Dict[str, Dict[str, Any]]:
    """Load owner state for workflow payloads with safe defaults."""
    return OwnerStateLoader.load_or_default(owner_agent_id, workflow_label)


# ── Orchestration Update Handlers ────────────────────────────────────────────


class OrchestrationUpdateHandlers:
    """Centralized orchestration update event handlers."""

    @staticmethod
    async def strategic_review(update) -> None:
        """Handle intermediate updates from strategic review orchestrations."""
        logger.info(
            "Strategic review update from agent %s: %s",
            getattr(update, "agent_id", "unknown"),
            getattr(update, "output", ""),
        )
