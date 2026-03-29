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
    PITCH_ORCHESTRATION_PURPOSE,
    PITCH_ORCHESTRATION_SCOPE,
    PITCH_STEP_IDS,
    WORKFLOW_REGISTRY,
    get_workflow_metadata,
    get_workflow_step_ids,
    list_registered_workflows,
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
        assert len(app.get_workflow_names()) == 13

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
        assert "pitch-orchestration" in names
        assert "workflow-orchestration" in names

    def test_foundry_workflows_removed(self):
        """Foundry is internal — no separate foundry-* workflows."""
        names = app.get_workflow_names()
        assert "foundry-orchestration" not in names
        assert "foundry-agent-create" not in names
        assert "foundry-connection" not in names

    def test_update_handler_registered(self):
        assert "strategic-review" in app.get_update_handler_names()
        assert "boardroom-debate" in app.get_update_handler_names()
        assert "pitch-orchestration" in app.get_update_handler_names()
        assert "workflow-orchestration" in app.get_update_handler_names()

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


class TestPitchOrchestration:
    """Test pitch orchestration constants and workflow registration."""

    def test_pitch_orchestration_purpose(self):
        """Purpose constant encodes interactive pitch delivery."""
        assert len(PITCH_ORCHESTRATION_PURPOSE) > 0
        assert "pitch" in PITCH_ORCHESTRATION_PURPOSE.lower()
        assert "boardroom" in PITCH_ORCHESTRATION_PURPOSE.lower()

    def test_pitch_orchestration_scope(self):
        """Scope constant covers pitch delivery via MCP."""
        assert len(PITCH_ORCHESTRATION_SCOPE) > 0
        assert "mcp" in PITCH_ORCHESTRATION_SCOPE.lower()

    def test_pitch_step_ids(self):
        """Pitch step IDs match the pitch.yaml workflow."""
        assert len(PITCH_STEP_IDS) == 9
        assert PITCH_STEP_IDS[0] == "paul_graham_intro"
        assert PITCH_STEP_IDS[-1] == "final_reveal"

    def test_pitch_step_ids_order(self):
        """Steps progress from intro through reveal."""
        assert "paul_graham_dataset" in PITCH_STEP_IDS
        assert "boardroom_cxo" in PITCH_STEP_IDS
        assert "business_infinity_resonance" in PITCH_STEP_IDS
        assert "asi_saga_self_learning" in PITCH_STEP_IDS

    def test_pitch_workflow_registered(self):
        """Pitch orchestration workflow is registered."""
        assert "pitch-orchestration" in app.get_workflow_names()

    def test_pitch_update_handler_registered(self):
        """Pitch update handler is registered."""
        assert "pitch-orchestration" in app.get_update_handler_names()


class TestWorkflowRegistry:
    """Test the generic workflow registry and helper functions."""

    def test_registry_contains_all_workflows(self):
        """All sample YAML workflows are registered."""
        assert "pitch_business_infinity" in WORKFLOW_REGISTRY
        assert "onboard_new_business" in WORKFLOW_REGISTRY
        assert "marketing_business_infinity" in WORKFLOW_REGISTRY
        assert "crisis_response" in WORKFLOW_REGISTRY
        assert "quarterly_strategic_review" in WORKFLOW_REGISTRY
        assert "product_launch" in WORKFLOW_REGISTRY

    def test_registry_entry_keys(self):
        """Each registry entry has the required keys."""
        required_keys = {"owner", "purpose", "scope", "yaml_path"}
        for wf_id, entry in WORKFLOW_REGISTRY.items():
            assert set(entry.keys()) == required_keys, (
                f"{wf_id} missing keys: {required_keys - set(entry.keys())}"
            )

    def test_workflow_owners(self):
        """Verify workflow owner assignments."""
        assert WORKFLOW_REGISTRY["pitch_business_infinity"]["owner"] == "founder"
        assert WORKFLOW_REGISTRY["onboard_new_business"]["owner"] == "coo"
        assert WORKFLOW_REGISTRY["marketing_business_infinity"]["owner"] == "cmo"
        assert WORKFLOW_REGISTRY["crisis_response"]["owner"] == "ceo"
        assert WORKFLOW_REGISTRY["quarterly_strategic_review"]["owner"] == "ceo"
        assert WORKFLOW_REGISTRY["product_launch"]["owner"] == "ceo"

    def test_get_workflow_metadata(self):
        """get_workflow_metadata returns correct entry."""
        meta = get_workflow_metadata("pitch_business_infinity")
        assert meta["owner"] == "founder"
        assert "pitch" in meta["purpose"].lower()

    def test_get_workflow_metadata_unknown(self):
        """get_workflow_metadata raises KeyError for unknown workflows."""
        with pytest.raises(KeyError):
            get_workflow_metadata("nonexistent_workflow")

    def test_get_workflow_step_ids_pitch(self):
        """Pitch workflow returns step IDs for backward compatibility."""
        step_ids = get_workflow_step_ids("pitch_business_infinity")
        assert len(step_ids) == 9
        assert step_ids[0] == "paul_graham_intro"
        assert step_ids[-1] == "final_reveal"

    def test_list_registered_workflows(self):
        """list_registered_workflows returns a copy of the registry."""
        result = list_registered_workflows()
        assert len(result) == 6
        assert result is not WORKFLOW_REGISTRY

    def test_pitch_backward_compatibility(self):
        """PITCH_* constants are derived from the registry."""
        assert PITCH_ORCHESTRATION_PURPOSE == WORKFLOW_REGISTRY["pitch_business_infinity"]["purpose"]
        assert PITCH_ORCHESTRATION_SCOPE == WORKFLOW_REGISTRY["pitch_business_infinity"]["scope"]

    def test_workflow_orchestration_registered(self):
        """Generic workflow-orchestration is registered as a workflow."""
        assert "workflow-orchestration" in app.get_workflow_names()

    def test_workflow_orchestration_update_handler(self):
        """Generic workflow-orchestration update handler is registered."""
        assert "workflow-orchestration" in app.get_update_handler_names()
