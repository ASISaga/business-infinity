"""MCP-integrated orchestration workflows for BusinessInfinity.

Handles orchestrations that require per-agent MCP server selection with
client-managed secrets, and exposes ERP search as an MCP tool.  Wrapped
with ``@aos_app.workflow`` and ``@aos_app.mcp_tool`` blueprint decorators
for Azure Functions registration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from aos_client import (
    MCPServerConfig,
    OrchestrationPurpose,
    OrchestrationRequest,
    WorkflowRequest,
)

from business_infinity.app_instance import aos_app
from business_infinity.workflow_utils import CSuiteAgentSelector

logger = logging.getLogger(__name__)


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


# ── Blueprint-wrapped Azure Functions registrations ──────────────────────────


@aos_app.workflow("mcp-orchestration")
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


@aos_app.mcp_tool("erp-search")
async def erp_search(request) -> Any:
    """Search ERP via MCP server."""
    return await MCPOrchestrationWorkflows.erp_search(request)
