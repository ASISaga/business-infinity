"""Enterprise capability workflows for BusinessInfinity.

Provides knowledge management, risk registry, audit trail, covenant, and
agent interaction endpoints.  Each capability is wrapped with the
``@aos_app.workflow`` blueprint decorator for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from aos_client import WorkflowRequest

from business_infinity.app_instance import aos_app

logger = logging.getLogger(__name__)


# ── Enterprise Capability Workflows ──────────────────────────────────────────


class EnterpriseWorkflows:
    """Enterprise capability workflow business logic.

    Provides knowledge management, risk registry, audit trail, covenant,
    and agent interaction endpoints.
    """

    @staticmethod
    async def knowledge_search(request: WorkflowRequest) -> Dict[str, Any]:
        """Search the knowledge base."""
        docs = await request.client.search_documents(
            query=request.body.get("query", ""),
            doc_type=request.body.get("doc_type"),
            limit=request.body.get("limit", 10),
        )
        return {"documents": [d.model_dump(mode="json") for d in docs]}

    @staticmethod
    async def risk_register(request: WorkflowRequest) -> Dict[str, Any]:
        """Register a new risk."""
        risk = await request.client.register_risk(request.body)
        return risk.model_dump(mode="json")

    @staticmethod
    async def risk_assess(request: WorkflowRequest) -> Dict[str, Any]:
        """Assess an existing risk."""
        risk = await request.client.assess_risk(
            risk_id=request.body["risk_id"],
            likelihood=request.body["likelihood"],
            impact=request.body["impact"],
        )
        return risk.model_dump(mode="json")

    @staticmethod
    async def log_decision(request: WorkflowRequest) -> Dict[str, Any]:
        """Log a boardroom decision."""
        record = await request.client.log_decision(request.body)
        return record.model_dump(mode="json")

    @staticmethod
    async def covenant_create(request: WorkflowRequest) -> Dict[str, Any]:
        """Create a business covenant."""
        covenant = await request.client.create_covenant(request.body)
        return covenant.model_dump(mode="json")

    @staticmethod
    async def ask_agent(request: WorkflowRequest) -> Dict[str, Any]:
        """Ask a single agent a question."""
        response = await request.client.ask_agent(
            agent_id=request.body["agent_id"],
            message=request.body["message"],
            context=request.body.get("context"),
        )
        return response.model_dump(mode="json")


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("knowledge-search")
async def knowledge_search(request: WorkflowRequest) -> Dict[str, Any]:
    """Search the knowledge base.

    Request body::

        {"query": "sustainability policy", "doc_type": "policy", "limit": 5}
    """
    return await EnterpriseWorkflows.knowledge_search(request)


@aos_app.workflow("risk-register")
async def risk_register(request: WorkflowRequest) -> Dict[str, Any]:
    """Register a new risk.

    Request body::

        {"title": "Supply chain disruption", "description": "...",
         "category": "operational", "owner": "coo"}
    """
    return await EnterpriseWorkflows.risk_register(request)


@aos_app.workflow("risk-assess")
async def risk_assess(request: WorkflowRequest) -> Dict[str, Any]:
    """Assess an existing risk.

    Request body::

        {"risk_id": "risk-abc", "likelihood": 0.7, "impact": 0.9}
    """
    return await EnterpriseWorkflows.risk_assess(request)


@aos_app.workflow("log-decision")
async def log_decision_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Log a boardroom decision.

    Request body::

        {"title": "Expand to EU", "rationale": "Market opportunity",
         "agent_id": "ceo"}
    """
    return await EnterpriseWorkflows.log_decision(request)


@aos_app.workflow("covenant-create")
async def covenant_create(request: WorkflowRequest) -> Dict[str, Any]:
    """Create a business covenant.

    Request body::

        {"title": "Ethics Covenant", "parties": ["business-infinity"]}
    """
    return await EnterpriseWorkflows.covenant_create(request)


@aos_app.workflow("ask-agent")
async def ask_agent_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Ask a single agent a question.

    Request body::

        {"agent_id": "ceo", "message": "What is the Q2 strategy?"}
    """
    return await EnterpriseWorkflows.ask_agent(request)
