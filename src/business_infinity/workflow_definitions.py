"""BusinessInfinity workflows — purpose-driven perpetual orchestrations.

Each workflow is implemented as a class with static methods encapsulating the
business logic.  The AOS Client SDK ``@app.workflow`` / ``@app.on_orchestration_update``
/ ``@app.mcp_tool`` decorators register thin module-level wrappers that delegate
to these classes.

Orchestrations are **perpetual and purpose-driven**: each workflow starts an
ongoing orchestration guided by a purpose.  Agents work toward the purpose
continuously — there is no finite task to complete.

All multi-agent orchestration is managed internally by the Foundry Agent
Service (v7.0.0).  This is transparent to workflows — clients use the
standard ``start_orchestration`` / ``submit_orchestration`` API.

Enterprise capabilities demonstrate the SDK APIs for knowledge management,
risk registry, audit trails, covenants, analytics, MCP integration, agent
interaction, and network discovery.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List

from aos_client import (
    AOSClient,
    AgentDescriptor,
    MCPServerConfig,
    OrchestrationPurpose,
    OrchestrationRequest,
    WorkflowRequest,
    workflow_template,
)

from business_infinity.app_instance import aos_app
from business_infinity.boardroom import (
    BOARDROOM_DEBATE_PURPOSE,
    BOARDROOM_DEBATE_SCOPE,
    BoardroomStateManager,
    CXO_DOMAINS,
    PITCH_ORCHESTRATION_PURPOSE,
    PITCH_ORCHESTRATION_SCOPE,
    PITCH_STEP_IDS,
    WORKFLOW_REGISTRY,
    WorkflowRegistryManager,
    WorkflowYAMLManager,
    get_workflow_metadata,
    get_workflow_step_ids,
    list_registered_workflows,
    load_workflow_yaml,
    save_workflow_yaml,
)

logger = logging.getLogger(__name__)
app = aos_app  # pylint: disable=invalid-name


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


@app.workflow("strategic-review")
async def strategic_review(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual strategic review orchestration with C-suite agents.

    Request body::

        {"quarter": "Q1-2026", "focus_areas": ["revenue", "growth"]}
    """
    return await StrategicWorkflows.strategic_review(request)


@app.workflow("market-analysis")
async def market_analysis(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual market analysis orchestration led by the CMO agent.

    Request body::

        {"market": "EU SaaS", "competitors": ["AcmeCorp", "Globex"]}
    """
    return await StrategicWorkflows.market_analysis(request)


@app.workflow("budget-approval")
async def budget_approval(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual budget governance orchestration with C-suite leadership.

    Request body::

        {"department": "Marketing", "amount": 500000, "justification": "Q2 campaign"}
    """
    return await StrategicWorkflows.budget_approval(request)


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


@app.workflow("boardroom-debate")
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


@app.on_orchestration_update("boardroom-debate")
async def handle_boardroom_debate_update(update) -> None:
    """Handle intermediate updates from boardroom debate orchestrations."""
    await BoardroomDebateWorkflows.handle_update(update)


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


@app.workflow("knowledge-search")
async def knowledge_search(request: WorkflowRequest) -> Dict[str, Any]:
    """Search the knowledge base.

    Request body::

        {"query": "sustainability policy", "doc_type": "policy", "limit": 5}
    """
    return await EnterpriseWorkflows.knowledge_search(request)


@app.workflow("risk-register")
async def risk_register(request: WorkflowRequest) -> Dict[str, Any]:
    """Register a new risk.

    Request body::

        {"title": "Supply chain disruption", "description": "...",
         "category": "operational", "owner": "coo"}
    """
    return await EnterpriseWorkflows.risk_register(request)


@app.workflow("risk-assess")
async def risk_assess(request: WorkflowRequest) -> Dict[str, Any]:
    """Assess an existing risk.

    Request body::

        {"risk_id": "risk-abc", "likelihood": 0.7, "impact": 0.9}
    """
    return await EnterpriseWorkflows.risk_assess(request)


@app.workflow("log-decision")
async def log_decision_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Log a boardroom decision.

    Request body::

        {"title": "Expand to EU", "rationale": "Market opportunity",
         "agent_id": "ceo"}
    """
    return await EnterpriseWorkflows.log_decision(request)


@app.workflow("covenant-create")
async def covenant_create(request: WorkflowRequest) -> Dict[str, Any]:
    """Create a business covenant.

    Request body::

        {"title": "Ethics Covenant", "parties": ["business-infinity"]}
    """
    return await EnterpriseWorkflows.covenant_create(request)


@app.workflow("ask-agent")
async def ask_agent_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Ask a single agent a question.

    Request body::

        {"agent_id": "ceo", "message": "What is the Q2 strategy?"}
    """
    return await EnterpriseWorkflows.ask_agent(request)


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


@app.on_orchestration_update("strategic-review")
async def handle_strategic_review_update(update) -> None:
    """Handle intermediate updates from strategic review orchestrations."""
    await OrchestrationUpdateHandlers.strategic_review(update)


# ── MCP Orchestration Workflows ──────────────────────────────────────────────


class MCPOrchestrationWorkflows:
    """MCP-integrated orchestration business logic.

    Handles orchestrations that require per-agent MCP server selection
    with client-managed secrets.
    """

    @staticmethod
    async def orchestrate(request: WorkflowRequest) -> Dict[str, Any]:
        """Start a purpose-driven orchestration with per-agent MCP server selection."""
        agents = await CSuiteAgentSelector.select(request.client)
        ceo_ids = [a.agent_id for a in agents if a.agent_id == "ceo"]
        cmo_ids = [a.agent_id for a in agents if a.agent_id == "cmo"]
        agent_ids = ceo_ids + cmo_ids
        if not agent_ids:
            raise ValueError(
                "CEO and/or CMO agents not available in the catalog"
            )

        purpose_text = request.body.get(
            "purpose",
            "Drive strategic growth with real-time ERP and CRM data",
        )

        mcp_servers: Dict[str, List[MCPServerConfig]] = {}
        for aid in ceo_ids:
            erp_secrets = (
                {"api_key": request.body["erp_api_key"]}
                if request.body.get("erp_api_key")
                else {}
            )
            mcp_servers[aid] = [
                MCPServerConfig(server_name="erp", secrets=erp_secrets)
            ]
        for aid in cmo_ids:
            crm_secrets = (
                {"token": request.body["crm_token"]}
                if request.body.get("crm_token")
                else {}
            )
            mcp_servers[aid] = [
                MCPServerConfig(server_name="crm", secrets=crm_secrets),
                MCPServerConfig(server_name="analytics"),
            ]

        req = OrchestrationRequest(
            agent_ids=agent_ids,
            purpose=OrchestrationPurpose(
                purpose=purpose_text,
                purpose_scope="C-suite strategic operations with live tool access",
            ),
            context=request.body,
            mcp_servers=mcp_servers,
        )
        status = await request.client.submit_orchestration(req)
        configured_servers = {
            aid: [s.server_name for s in cfgs]
            for aid, cfgs in mcp_servers.items()
        }
        logger.info(
            "MCP orchestration started: %s | agents=%s | mcp_servers=%s",
            status.orchestration_id,
            agent_ids,
            list(mcp_servers.keys()),
        )
        return {
            "orchestration_id": status.orchestration_id,
            "status": status.status.value,
            "mcp_servers_configured": configured_servers,
        }

    @staticmethod
    async def erp_search(request) -> Any:
        """Search ERP via MCP server."""
        return await request.client.call_mcp_tool(
            "erpnext", "search", request.body
        )


@app.workflow("mcp-orchestration")
async def mcp_orchestration(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a purpose-driven orchestration with per-agent MCP server selection.

    Request body::

        {
            "purpose": "Drive strategic growth with real-time data",
            "erp_api_key": "secret-erp-key",
            "crm_token": "secret-crm-token"
        }
    """
    return await MCPOrchestrationWorkflows.orchestrate(request)


@app.mcp_tool("erp-search")
async def erp_search(request) -> Any:
    """Search ERP via MCP server."""
    return await MCPOrchestrationWorkflows.erp_search(request)


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


@app.workflow("pitch-orchestration")
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


@app.on_orchestration_update("pitch-orchestration")
async def handle_pitch_update(update) -> None:
    """Handle intermediate updates from pitch orchestrations."""
    await PitchWorkflows.handle_update(update)


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


@app.workflow("workflow-orchestration")
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


@app.on_orchestration_update("workflow-orchestration")
async def handle_workflow_update(update) -> None:
    """Handle intermediate updates from generic workflow orchestrations."""
    await GenericWorkflowOrchestration.handle_update(update)


# ── Workflow Editor Service ──────────────────────────────────────────────────


class WorkflowEditorService:
    """Workflow editor endpoint business logic.

    Provides list, get, and save operations for step-wise editing of
    workflow YAML files through the website frontend.
    """

    @staticmethod
    async def list_workflows(request: WorkflowRequest) -> Dict[str, Any]:
        """Return metadata for all registered workflows."""
        workflows = [
            {
                "workflow_id": wf_id,
                "owner": meta["owner"],
                "yaml_path": meta["yaml_path"],
            }
            for wf_id, meta in WorkflowRegistryManager.list_all().items()
        ]
        logger.info(
            "Workflow editor list requested: %d workflows", len(workflows)
        )
        return {"workflows": workflows}

    @staticmethod
    async def get_workflow(request: WorkflowRequest) -> Dict[str, Any]:
        """Return the full structured content of a workflow for editing."""
        workflow_id = request.body.get("workflow_id", "")
        if not workflow_id:
            raise ValueError("workflow_id is required in request body")
        try:
            data = WorkflowYAMLManager.load(workflow_id)
        except KeyError:
            registered = list(WORKFLOW_REGISTRY.keys())
            raise ValueError(
                f"Unknown workflow_id '{workflow_id}'. "
                f"Registered workflows: {registered}"
            )
        logger.info(
            "Workflow editor get: %s (%d steps)",
            workflow_id,
            len(data.get("steps", {})),
        )
        return data

    @staticmethod
    async def save_workflow(request: WorkflowRequest) -> Dict[str, Any]:
        """Validate and save an updated workflow structure to its YAML file."""
        workflow_id = request.body.get("workflow_id", "")
        if not workflow_id:
            raise ValueError("workflow_id is required in request body")
        try:
            WorkflowYAMLManager.save(workflow_id, request.body)
        except KeyError:
            registered = list(WORKFLOW_REGISTRY.keys())
            raise ValueError(
                f"Unknown workflow_id '{workflow_id}'. "
                f"Registered workflows: {registered}"
            )
        step_count = len(request.body.get("steps", {}))
        logger.info(
            "Workflow editor save: %s (%d steps)",
            workflow_id,
            step_count,
        )
        return {
            "status": "saved",
            "workflow_id": workflow_id,
            "step_count": step_count,
        }


@app.workflow("workflow-editor-list")
async def workflow_editor_list(request: WorkflowRequest) -> Dict[str, Any]:
    """Return metadata for all registered workflows.

    Response::

        {
            "workflows": [
                {
                    "workflow_id": "pitch_business_infinity",
                    "owner": "founder",
                    "yaml_path": "docs/workflow/samples/pitch.yaml"
                },
                ...
            ]
        }
    """
    return await WorkflowEditorService.list_workflows(request)


@app.workflow("workflow-editor-get")
async def workflow_editor_get(request: WorkflowRequest) -> Dict[str, Any]:
    """Return the full structured content of a workflow for step-wise editing.

    Request body::

        {"workflow_id": "pitch_business_infinity"}
    """
    return await WorkflowEditorService.get_workflow(request)


@app.workflow("workflow-editor-save")
async def workflow_editor_save(request: WorkflowRequest) -> Dict[str, Any]:
    """Validate and save an updated workflow structure to its YAML file.

    Request body mirrors the boardroom YAML schema::

        {
            "workflow_id": "pitch_business_infinity",
            "version": "1.0.0",
            "owner": "founder",
            "steps": { ... }
        }

    Response::

        {"status": "saved", "workflow_id": "pitch_business_infinity", "step_count": 9}
    """
    return await WorkflowEditorService.save_workflow(request)
