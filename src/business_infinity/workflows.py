"""BusinessInfinity workflows — purpose-driven perpetual orchestrations.

Each workflow function is decorated with ``@app.workflow`` from the AOS Client
SDK.  The SDK handles all Azure Functions scaffolding (HTTP triggers,
Service Bus triggers, authentication, health endpoints).

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
    AOSApp,
    AOSClient,
    AgentDescriptor,
    MCPServerConfig,
    OrchestrationPurpose,
    OrchestrationRequest,
    WorkflowRequest,
    workflow_template,
)
from aos_client.observability import ObservabilityConfig

from business_infinity.boardroom import (
    BOARDROOM_DEBATE_PURPOSE,
    BOARDROOM_DEBATE_SCOPE,
    BoardroomStateManager,
    CXO_DOMAINS,
    PITCH_ORCHESTRATION_PURPOSE,
    PITCH_ORCHESTRATION_SCOPE,
    PITCH_STEP_IDS,
    WORKFLOW_REGISTRY,
    get_workflow_metadata,
    get_workflow_step_ids,
    list_registered_workflows,
    load_workflow_yaml,
    save_workflow_yaml,
)

logger = logging.getLogger(__name__)

app = AOSApp(
    name="business-infinity",
    observability=ObservabilityConfig(
        structured_logging=True,
        correlation_tracking=True,
        health_checks=["aos", "service-bus"],
    ),
)

# ── C-Suite Agent Selection ──────────────────────────────────────────────────

#: Agent types considered part of the C-suite
C_SUITE_TYPES = {
    "LeadershipAgent",
    "CEOAgent",
    "CFOAgent",
    "COOAgent",
    "CMOAgent",
    "CHROAgent",
    "CTOAgent",
    "CSOAgent",
}

#: Preferred C-suite agent IDs for BusinessInfinity orchestrations
C_SUITE_AGENT_IDS = ["ceo", "cfo", "coo", "cmo", "chro", "cto", "cso"]


async def select_c_suite_agents(client: AOSClient) -> List[AgentDescriptor]:
    """Select C-suite agents from the RealmOfAgents catalog.

    Returns agents matching :data:`C_SUITE_AGENT_IDS` or, if not found,
    agents whose ``agent_type`` is in :data:`C_SUITE_TYPES`.
    """
    all_agents = await client.list_agents()

    # Prefer explicit IDs
    by_id = {a.agent_id: a for a in all_agents}
    selected = [by_id[aid] for aid in C_SUITE_AGENT_IDS if aid in by_id]

    if not selected:
        # Fall back to type-based selection
        selected = [a for a in all_agents if a.agent_type in C_SUITE_TYPES]

    logger.info("Selected %d C-suite agents: %s", len(selected), [a.agent_id for a in selected])
    return selected


# ── Workflow Template (Enhancement #11) ──────────────────────────────────────


@workflow_template
async def c_suite_orchestration(
    request: WorkflowRequest,
    agent_filter: Callable[[AgentDescriptor], bool],
    purpose: str,
    purpose_scope: str,
) -> Dict[str, Any]:
    """Reusable template for C-suite orchestrations."""
    agents = await select_c_suite_agents(request.client)
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


# ── Purpose-Driven Orchestrations ────────────────────────────────────────────


@app.workflow("strategic-review")
async def strategic_review(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual strategic review orchestration with C-suite agents.

    The orchestration continuously drives strategic alignment, review, and
    improvement across the organisation.  It does not complete — agents
    work toward the purpose indefinitely.

    Request body::

        {"quarter": "Q1-2026", "focus_areas": ["revenue", "growth"]}
    """
    return await c_suite_orchestration(
        request,
        agent_filter=lambda a: True,
        purpose="Drive strategic review and continuous organisational improvement",
        purpose_scope="C-suite strategic alignment and cross-functional coordination",
    )


@app.workflow("market-analysis")
async def market_analysis(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual market analysis orchestration led by the CMO agent.

    The orchestration continuously monitors markets, analyses competitors,
    and surfaces insights.  It does not complete — agents work toward the
    purpose indefinitely.

    Request body::

        {"market": "EU SaaS", "competitors": ["AcmeCorp", "Globex"]}
    """
    # Select CMO + supporting agents
    agents = await select_c_suite_agents(request.client)
    agent_ids = [a.agent_id for a in agents if a.agent_type == "CMOAgent"]

    # Add CEO for strategic oversight if available
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
    logger.info("Market analysis orchestration started: %s", status.orchestration_id)
    return {"orchestration_id": status.orchestration_id, "status": status.status.value}


@app.workflow("budget-approval")
async def budget_approval(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a perpetual budget governance orchestration with C-suite leadership.

    The orchestration continuously oversees budget allocation, monitors
    spend, and governs financial decisions.  It does not complete — agents
    work toward the purpose indefinitely.

    Request body::

        {"department": "Marketing", "amount": 500000, "justification": "Q2 campaign"}
    """
    agents = await select_c_suite_agents(request.client)
    # Budget governance: CEO + CFO
    agent_ids = [a.agent_id for a in agents if a.agent_id in ("ceo", "cfo")]

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
    return {"orchestration_id": status.orchestration_id, "status": status.status.value}


# ── Boardroom Debate (Philosophy Implementation) ────────────────────────────


@app.workflow("boardroom-debate")
async def boardroom_debate(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a purpose-driven boardroom debate orchestration.

    Implements the core BusinessInfinity philosophy: a decision tree debate
    where each CXO agent applies their domain leadership to propose pathways
    in response to a business event.  Pathways are debated, scored for
    resonance against the company's purpose, and the boardroom converges on
    an autonomous action.

    Request body::

        {
            "event": "Competitor launches aggressive campaign",
            "event_source": "market",
            "company_purpose": "Deliver reliable innovation that earns lasting trust",
            "context": {"churn_rate": 0.12, "market": "EU SaaS"}
        }
    """
    agents = await select_c_suite_agents(request.client)
    agent_ids = [a.agent_id for a in agents]

    if not agent_ids:
        raise ValueError("No C-suite agents available for boardroom debate")

    # Build domain context so each agent understands their role in the debate.
    domain_context = {
        aid: CXO_DOMAINS[aid]
        for aid in agent_ids
        if aid in CXO_DOMAINS
    }

    # Include current boardroom state and segregated agent context/content so
    # agents enter the debate with full situational awareness.
    boardroom_state = BoardroomStateManager.get_boardroom_state_or_default()
    agent_contexts = BoardroomStateManager.get_all_agent_contexts()
    agent_contents = BoardroomStateManager.get_all_agent_contents()

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
            "agent_contexts": agent_contexts,
            "agent_contents": agent_contents,
        },
    )
    logger.info(
        "Boardroom debate orchestration started: %s | agents=%s",
        status.orchestration_id,
        agent_ids,
    )
    return {"orchestration_id": status.orchestration_id, "status": status.status.value}


@app.on_orchestration_update("boardroom-debate")
async def handle_boardroom_debate_update(update) -> None:
    """Handle intermediate updates from boardroom debate orchestrations."""
    logger.info(
        "Boardroom debate update from agent %s: %s",
        getattr(update, "agent_id", "unknown"),
        getattr(update, "output", ""),
    )


# ── Enterprise Capability Workflows (Enhancement #1–#12) ────────────────────


@app.workflow("knowledge-search")
async def knowledge_search(request: WorkflowRequest) -> Dict[str, Any]:
    """Search the knowledge base.

    Request body::

        {"query": "sustainability policy", "doc_type": "policy", "limit": 5}
    """
    docs = await request.client.search_documents(
        query=request.body.get("query", ""),
        doc_type=request.body.get("doc_type"),
        limit=request.body.get("limit", 10),
    )
    return {"documents": [d.model_dump(mode="json") for d in docs]}


@app.workflow("risk-register")
async def risk_register(request: WorkflowRequest) -> Dict[str, Any]:
    """Register a new risk.

    Request body::

        {"title": "Supply chain disruption", "description": "...",
         "category": "operational", "owner": "coo"}
    """
    risk = await request.client.register_risk(request.body)
    return risk.model_dump(mode="json")


@app.workflow("risk-assess")
async def risk_assess(request: WorkflowRequest) -> Dict[str, Any]:
    """Assess an existing risk.

    Request body::

        {"risk_id": "risk-abc", "likelihood": 0.7, "impact": 0.9}
    """
    risk = await request.client.assess_risk(
        risk_id=request.body["risk_id"],
        likelihood=request.body["likelihood"],
        impact=request.body["impact"],
    )
    return risk.model_dump(mode="json")


@app.workflow("log-decision")
async def log_decision_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Log a boardroom decision.

    Request body::

        {"title": "Expand to EU", "rationale": "Market opportunity",
         "agent_id": "ceo"}
    """
    record = await request.client.log_decision(request.body)
    return record.model_dump(mode="json")


@app.workflow("covenant-create")
async def covenant_create(request: WorkflowRequest) -> Dict[str, Any]:
    """Create a business covenant.

    Request body::

        {"title": "Ethics Covenant", "parties": ["business-infinity"]}
    """
    covenant = await request.client.create_covenant(request.body)
    return covenant.model_dump(mode="json")


@app.workflow("ask-agent")
async def ask_agent_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Ask a single agent a question.

    Request body::

        {"agent_id": "ceo", "message": "What is the Q2 strategy?"}
    """
    response = await request.client.ask_agent(
        agent_id=request.body["agent_id"],
        message=request.body["message"],
        context=request.body.get("context"),
    )
    return response.model_dump(mode="json")


# ── Orchestration Update Handler (Enhancement #5) ───────────────────────────


@app.on_orchestration_update("strategic-review")
async def handle_strategic_review_update(update) -> None:
    """Handle intermediate updates from strategic review orchestrations."""
    logger.info(
        "Strategic review update from agent %s: %s",
        getattr(update, "agent_id", "unknown"),
        getattr(update, "output", ""),
    )


# ── MCP Server Selection in Orchestrations ───────────────────────────────────


@app.workflow("mcp-orchestration")
async def mcp_orchestration(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a purpose-driven orchestration with per-agent MCP server selection.

    Clients declare which pre-registered MCP servers each agent should use by
    providing :class:`~aos_client.MCPServerConfig` objects with a server name
    and optional client-managed secrets.  AOS looks up each server in its
    internal registry, injects the secrets, and connects the agents.  Transport
    details (URLs, protocols, gateway configuration) are managed by AOS and are
    never part of this request.

    Request body::

        {
            "purpose": "Drive strategic growth with real-time data",
            "erp_api_key": "secret-erp-key",
            "crm_token": "secret-crm-token"
        }
    """
    agents = await select_c_suite_agents(request.client)
    ceo_ids = [a.agent_id for a in agents if a.agent_id == "ceo"]
    cmo_ids = [a.agent_id for a in agents if a.agent_id == "cmo"]
    agent_ids = ceo_ids + cmo_ids
    if not agent_ids:
        raise ValueError("CEO and/or CMO agents not available in the catalog")

    purpose_text = request.body.get(
        "purpose", "Drive strategic growth with real-time ERP and CRM data"
    )

    # Declare per-agent MCP server selection.
    # Only server names and client secrets are provided; AOS handles everything else.
    mcp_servers: Dict[str, List[MCPServerConfig]] = {}
    for aid in ceo_ids:
        erp_secrets = {"api_key": request.body["erp_api_key"]} if request.body.get("erp_api_key") else {}
        mcp_servers[aid] = [MCPServerConfig(server_name="erp", secrets=erp_secrets)]
    for aid in cmo_ids:
        crm_secrets = {"token": request.body["crm_token"]} if request.body.get("crm_token") else {}
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


# ── Pitch Orchestration (Boardroom Interface) ───────────────────────────────


@app.workflow("pitch-orchestration")
async def pitch_orchestration(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a pitch delivery orchestration through the boardroom interface.

    Orchestrates the Business Infinity pitch as an interactive narrative
    delivered step-by-step through the ``<chatroom>`` Web Component on
    business-infinity.asisaga.com.  The Founder agent presents each step,
    with actions and navigation rendered via MCP app payloads.

    The pitch workflow steps are defined in
    ``docs/workflow/samples/pitch.yaml``.

    Request body::

        {
            "step_id": "paul_graham_intro",
            "session_id": "optional-session-id",
            "company_purpose": "Deliver reliable innovation that earns lasting trust"
        }
    """
    agents = await select_c_suite_agents(request.client)

    # The Founder agent delivers the pitch; fall back to CEO
    founder_ids = [a.agent_id for a in agents if a.agent_id == "founder"]
    ceo_ids = [a.agent_id for a in agents if a.agent_id == "ceo"]
    agent_ids = founder_ids or ceo_ids

    if not agent_ids:
        raise ValueError("Founder or CEO agent not available for pitch delivery")

    step_id = request.body.get("step_id", PITCH_STEP_IDS[0])

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


@app.on_orchestration_update("pitch-orchestration")
async def handle_pitch_update(update) -> None:
    """Handle intermediate updates from pitch orchestrations."""
    logger.info(
        "Pitch update from agent %s: step=%s",
        getattr(update, "agent_id", "unknown"),
        getattr(update, "output", ""),
    )


# ── Generic Workflow Orchestration ───────────────────────────────────────────
#
# A single generic endpoint that drives any registered structured workflow.
# The workflow_id in the request body selects which YAML-defined workflow to
# run.  The owner agent from the WORKFLOW_REGISTRY conducts the conversation.
# This replaces the need for per-workflow Python endpoints.


@app.workflow("workflow-orchestration")
async def workflow_orchestration(request: WorkflowRequest) -> Dict[str, Any]:
    """Start a structured workflow orchestration through the boardroom interface.

    This is the generic entry point for all YAML-defined boardroom workflows.
    The ``workflow_id`` in the request body determines which workflow to run.
    The owning agent (defined in the workflow registry) conducts the
    step-by-step conversation with the external entity.

    Supported workflow IDs are registered in
    ``src/business_infinity/boardroom.py`` → ``WORKFLOW_REGISTRY``.

    Request body::

        {
            "workflow_id": "pitch_business_infinity",
            "step_id": "paul_graham_intro",
            "session_id": "optional-session-id",
            "company_purpose": "Deliver reliable innovation that earns lasting trust"
        }
    """
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

    # Resolve the owner agent.  list_agents() returns all agents including
    # non-C-suite agents like "founder".  We call it once and filter.
    all_agents = await request.client.list_agents()
    all_by_id = {a.agent_id: a for a in all_agents}

    agent_ids = []
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
    step_id = request.body.get("step_id", step_ids[0] if step_ids else "")

    # Include current boardroom state so the owner agent enters the workflow
    # with full situational context.
    boardroom_state = BoardroomStateManager.get_boardroom_state_or_default()
    try:
        owner_context = BoardroomStateManager.load_agent_context(owner_agent_id)
        owner_content = BoardroomStateManager.load_agent_content(owner_agent_id)
    except KeyError:
        logger.warning(
            "Owner state unavailable because agent '%s' is not registered in workflow '%s'",
            owner_agent_id,
            workflow_id,
        )
        owner_context = {}
        owner_content = {}
    except FileNotFoundError:
        logger.warning(
            "Owner state file missing for agent '%s' in workflow '%s'",
            owner_agent_id,
            workflow_id,
        )
        owner_context = {}
        owner_content = {}

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
            "owner_context": owner_context,
            "owner_content": owner_content,
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


@app.on_orchestration_update("workflow-orchestration")
async def handle_workflow_update(update) -> None:
    """Handle intermediate updates from generic workflow orchestrations."""
    logger.info(
        "Workflow update from agent %s: %s",
        getattr(update, "agent_id", "unknown"),
        getattr(update, "output", ""),
    )


# ── MCP Tool Integration (Enhancement #7) ───────────────────────────────────


@app.mcp_tool("erp-search")
async def erp_search(request) -> Any:
    """Search ERP via MCP server."""
    return await request.client.call_mcp_tool("erpnext", "search", request.body)


# ── Workflow Editor Endpoints ─────────────────────────────────────────────────
#
# Three HTTP endpoints that enable step-wise, form-based editing of the
# workflow YAML files in docs/workflow/samples/ through the
# business-infinity.asisaga.com website.  Each endpoint is intentionally
# simple so the frontend can render a structured step editor rather than a
# free-text YAML editor.


@app.workflow("workflow-editor-list")
async def workflow_editor_list(request: WorkflowRequest) -> Dict[str, Any]:
    """Return metadata for all registered workflows.

    The frontend calls this endpoint to populate the workflow selection
    panel in the step-wise editor.

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
    workflows = [
        {
            "workflow_id": wf_id,
            "owner": meta["owner"],
            "yaml_path": meta["yaml_path"],
        }
        for wf_id, meta in list_registered_workflows().items()
    ]
    logger.info("Workflow editor list requested: %d workflows", len(workflows))
    return {"workflows": workflows}


@app.workflow("workflow-editor-get")
async def workflow_editor_get(request: WorkflowRequest) -> Dict[str, Any]:
    """Return the full structured content of a workflow for step-wise editing.

    The frontend calls this endpoint when the user selects a workflow to
    edit.  The response is the parsed YAML data — one step per key under
    ``steps`` — which the editor renders as individual forms rather than raw
    text.

    Request body::

        {"workflow_id": "pitch_business_infinity"}

    Response mirrors the boardroom YAML schema::

        {
            "workflow_id": "pitch_business_infinity",
            "version": "1.0.0",
            "owner": "founder",
            "steps": {
                "paul_graham_intro": {
                    "narrative": "...",
                    "response": "...",
                    "actions": [],
                    "navigation": {"next": "paul_graham_dataset"}
                },
                ...
            }
        }
    """
    workflow_id = request.body.get("workflow_id", "")
    if not workflow_id:
        raise ValueError("workflow_id is required in request body")
    try:
        data = load_workflow_yaml(workflow_id)
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


@app.workflow("workflow-editor-save")
async def workflow_editor_save(request: WorkflowRequest) -> Dict[str, Any]:
    """Validate and save an updated workflow structure to its YAML file.

    The frontend calls this endpoint when the user submits their edits from
    the step-wise editor.  The payload must contain the full workflow
    structure including all steps; partial updates are not supported.
    Validation is applied before writing so the file is never overwritten
    with a structurally invalid document.

    Request body mirrors the boardroom YAML schema (same shape as the
    response from ``workflow-editor-get``)::

        {
            "workflow_id": "pitch_business_infinity",
            "version": "1.0.0",
            "owner": "founder",
            "steps": {
                "paul_graham_intro": {
                    "narrative": "...",
                    "response": "...",
                    "actions": [],
                    "navigation": {"next": "paul_graham_dataset"}
                },
                ...
            }
        }

    Response::

        {"status": "saved", "workflow_id": "pitch_business_infinity", "step_count": 9}
    """
    workflow_id = request.body.get("workflow_id", "")
    if not workflow_id:
        raise ValueError("workflow_id is required in request body")
    try:
        save_workflow_yaml(workflow_id, request.body)
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
    return {"status": "saved", "workflow_id": workflow_id, "step_count": step_count}
