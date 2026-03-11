"""Tests for BusinessInfinity workflows."""

import pytest

from business_infinity.workflows import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    app,
    select_c_suite_agents,
)
from business_infinity.boardroom import (
    BOARDROOM_DEBATE_PURPOSE,
    BOARDROOM_DEBATE_SCOPE,
    CXO_DOMAINS,
    CXO_PATHWAY_TYPES,
)


class TestCSuiteSelection:
    """Test C-suite agent selection logic."""

    def test_c_suite_agent_ids(self):
        assert "ceo" in C_SUITE_AGENT_IDS
        assert "cfo" in C_SUITE_AGENT_IDS
        assert "cmo" in C_SUITE_AGENT_IDS
        assert "coo" in C_SUITE_AGENT_IDS
        assert "cto" in C_SUITE_AGENT_IDS
        assert "cso" in C_SUITE_AGENT_IDS
        assert "chro" in C_SUITE_AGENT_IDS

    def test_c_suite_types(self):
        assert "LeadershipAgent" in C_SUITE_TYPES
        assert "CMOAgent" in C_SUITE_TYPES
        assert "CEOAgent" in C_SUITE_TYPES
        assert "CFOAgent" in C_SUITE_TYPES
        assert "COOAgent" in C_SUITE_TYPES
        assert "CHROAgent" in C_SUITE_TYPES
        assert "CTOAgent" in C_SUITE_TYPES
        assert "CSOAgent" in C_SUITE_TYPES


class TestAOSAppWorkflows:
    """Test AOSApp workflow registration."""

    def test_app_name(self):
        assert app.name == "business-infinity"

    def test_workflows_registered(self):
        names = app.get_workflow_names()
        assert "strategic-review" in names
        assert "market-analysis" in names
        assert "budget-approval" in names

    def test_workflow_count(self):
        assert len(app.get_workflow_names()) == 11

    def test_new_workflows_registered(self):
        names = app.get_workflow_names()
        assert "knowledge-search" in names
        assert "risk-register" in names
        assert "risk-assess" in names
        assert "log-decision" in names
        assert "covenant-create" in names
        assert "ask-agent" in names
        assert "mcp-orchestration" in names
        assert "boardroom-debate" in names

    def test_foundry_workflows_removed(self):
        """Foundry is internal — no separate foundry-* workflows."""
        names = app.get_workflow_names()
        assert "foundry-orchestration" not in names
        assert "foundry-agent-create" not in names
        assert "foundry-connection" not in names

    def test_update_handler_registered(self):
        assert "strategic-review" in app.get_update_handler_names()
        assert "boardroom-debate" in app.get_update_handler_names()

    def test_mcp_tool_registered(self):
        assert "erp-search" in app.get_mcp_tool_names()

    def test_observability_configured(self):
        assert app.observability is not None


class TestBoardroomPhilosophy:
    """Test boardroom philosophy constants and domain mappings."""

    def test_cxo_domains_cover_all_agent_ids(self):
        """Every C-suite agent ID has a domain mapping."""
        for agent_id in C_SUITE_AGENT_IDS:
            assert agent_id in CXO_DOMAINS, f"{agent_id} missing from CXO_DOMAINS"

    def test_cxo_domain_keys(self):
        """Each CXO domain entry has the required keys."""
        required_keys = {"archetype", "title", "domain", "pathway", "description"}
        for agent_id, domain in CXO_DOMAINS.items():
            assert set(domain.keys()) == required_keys, (
                f"{agent_id} domain missing keys: {required_keys - set(domain.keys())}"
            )

    def test_philosophy_archetypes(self):
        """Verify the legendary archetypes from the philosophy."""
        assert CXO_DOMAINS["ceo"]["archetype"] == "Jobs"
        assert CXO_DOMAINS["cfo"]["archetype"] == "Buffett"
        assert CXO_DOMAINS["coo"]["archetype"] == "Deming"
        assert CXO_DOMAINS["cmo"]["archetype"] == "Ogilvy"
        assert CXO_DOMAINS["chro"]["archetype"] == "Drucker"
        assert CXO_DOMAINS["cto"]["archetype"] == "Turing"
        assert CXO_DOMAINS["cso"]["archetype"] == "Sun Tzu"

    def test_pathway_types(self):
        """Verify pathway types are derived from domain mappings."""
        assert "narrative" in CXO_PATHWAY_TYPES
        assert "resource-allocation" in CXO_PATHWAY_TYPES
        assert "workflow" in CXO_PATHWAY_TYPES
        assert "communication" in CXO_PATHWAY_TYPES
        assert "people-centric" in CXO_PATHWAY_TYPES

    def test_boardroom_debate_purpose(self):
        """Purpose constant is non-empty and encodes the debate process."""
        assert len(BOARDROOM_DEBATE_PURPOSE) > 0
        assert "decision tree" in BOARDROOM_DEBATE_PURPOSE.lower()
        assert "resonance" in BOARDROOM_DEBATE_PURPOSE.lower()

    def test_boardroom_debate_scope(self):
        """Scope constant is non-empty and covers full boardroom convergence."""
        assert len(BOARDROOM_DEBATE_SCOPE) > 0
        assert "convergence" in BOARDROOM_DEBATE_SCOPE.lower()
