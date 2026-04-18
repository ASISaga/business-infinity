"""Tests for BusinessInfinity workflows."""

import pytest

import function_app
from business_infinity.workflows import (
    C_SUITE_AGENT_IDS,
    C_SUITE_TYPES,
    app,
    select_c_suite_agents,
)
from business_infinity.boardroom import (
    BOARDROOM_DEBATE_PURPOSE,
    BOARDROOM_DEBATE_SCOPE,
    BoardroomStateManager,
    CXO_DOMAINS,
    CXO_PATHWAY_TYPES,
    PITCH_ORCHESTRATION_PURPOSE,
    PITCH_ORCHESTRATION_SCOPE,
    PITCH_STEP_IDS,
    WORKFLOW_REGISTRY,
    WorkflowRegistryManager,
    WorkflowYAMLManager,
)


class AgentDouble:
    """Minimal agent test double."""

    def __init__(self, agent_id):
        self.agent_id = agent_id


class CaptureClient:
    """Async client double that captures orchestration kwargs."""

    def __init__(self):
        self.kwargs = None
        self.agents = []

    async def list_agents(self):
        return self.agents

    async def start_orchestration(self, **kwargs):
        self.kwargs = kwargs
        return type(
            "Status",
            (),
            {
                "orchestration_id": "orch-test",
                "status": type("Running", (), {"value": "running"})(),
            },
        )()


class RequestDouble:
    """Minimal workflow request test double."""

    def __init__(self, body, client):
        self.body = body
        self.client = client


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
        assert len(app.get_workflow_names()) == 16

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

    def test_function_app_exposes_azure_function_app_instance(self):
        """The runtime-discoverable app object is an Azure FunctionApp registered via blueprint."""
        from azure.functions.decorators.function_app import FunctionApp
        assert isinstance(function_app.app, FunctionApp)
        assert not hasattr(function_app, "functions")


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
        assert "founder_sovereignty" in WORKFLOW_REGISTRY
        assert "knowledge_continuity" in WORKFLOW_REGISTRY
        assert "resilience_consultation" in WORKFLOW_REGISTRY
        assert "data_synthesis" in WORKFLOW_REGISTRY
        assert "complexity_governance" in WORKFLOW_REGISTRY
        assert "strategy_execution" in WORKFLOW_REGISTRY
        assert "culture_integrity" in WORKFLOW_REGISTRY
        assert "ai_governance" in WORKFLOW_REGISTRY
        assert "exit_readiness" in WORKFLOW_REGISTRY
        assert "innovation_velocity" in WORKFLOW_REGISTRY

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
        assert WORKFLOW_REGISTRY["founder_sovereignty"]["owner"] == "ceo"
        assert WORKFLOW_REGISTRY["knowledge_continuity"]["owner"] == "chro"
        assert WORKFLOW_REGISTRY["resilience_consultation"]["owner"] == "cso"
        assert WORKFLOW_REGISTRY["data_synthesis"]["owner"] == "cmo"
        assert WORKFLOW_REGISTRY["complexity_governance"]["owner"] == "coo"
        assert WORKFLOW_REGISTRY["strategy_execution"]["owner"] == "ceo"
        assert WORKFLOW_REGISTRY["culture_integrity"]["owner"] == "chro"
        assert WORKFLOW_REGISTRY["ai_governance"]["owner"] == "cto"
        assert WORKFLOW_REGISTRY["exit_readiness"]["owner"] == "cfo"
        assert WORKFLOW_REGISTRY["innovation_velocity"]["owner"] == "cto"

    def test_get_workflow_metadata(self):
        """get_workflow_metadata returns correct entry."""
        meta = WorkflowRegistryManager.get_metadata("pitch_business_infinity")
        assert meta["owner"] == "founder"
        assert "pitch" in meta["purpose"].lower()

    def test_get_workflow_metadata_unknown(self):
        """get_workflow_metadata raises KeyError for unknown workflows."""
        with pytest.raises(KeyError):
            WorkflowRegistryManager.get_metadata("nonexistent_workflow")

    def test_get_workflow_step_ids_pitch(self):
        """Pitch workflow returns step IDs for backward compatibility."""
        step_ids = WorkflowRegistryManager.get_step_ids("pitch_business_infinity")
        assert len(step_ids) == 9
        assert step_ids[0] == "paul_graham_intro"
        assert step_ids[-1] == "final_reveal"

    def test_list_registered_workflows(self):
        """list_registered_workflows returns a copy of the registry."""
        result = WorkflowRegistryManager.list_all()
        assert len(result) == 16
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

class TestWorkflowEditor:
    """Test workflow editor endpoint registration and YAML I/O helpers."""

    def test_editor_endpoints_registered(self):
        """All three workflow editor endpoints are registered."""
        names = app.get_workflow_names()
        assert "workflow-editor-list" in names
        assert "workflow-editor-get" in names
        assert "workflow-editor-save" in names

    def test_load_workflow_yaml_pitch(self):
        """load_workflow_yaml returns full structured data for pitch workflow."""
        data = WorkflowYAMLManager.load("pitch_business_infinity")
        assert data["workflow_id"] == "pitch_business_infinity"
        assert data["owner"] == "founder"
        assert "steps" in data
        assert len(data["steps"]) == 9
        assert "paul_graham_intro" in data["steps"]
        assert "final_reveal" in data["steps"]

    def test_load_workflow_yaml_step_fields(self):
        """Each step has narrative, response, actions, and navigation."""
        data = WorkflowYAMLManager.load("pitch_business_infinity")
        for step_id, step in data["steps"].items():
            assert "narrative" in step, f"{step_id} missing narrative"
            assert "response" in step, f"{step_id} missing response"
            assert "actions" in step, f"{step_id} missing actions"
            assert isinstance(step["actions"], list), f"{step_id} actions not a list"

    def test_load_workflow_yaml_all_workflows(self):
        """load_workflow_yaml works for all registered workflows."""
        for workflow_id in WORKFLOW_REGISTRY:
            data = WorkflowYAMLManager.load(workflow_id)
            assert data["workflow_id"] == workflow_id
            assert "steps" in data
            assert len(data["steps"]) > 0

    def test_load_workflow_yaml_unknown(self):
        """load_workflow_yaml raises KeyError for an unknown workflow."""
        with pytest.raises(KeyError):
            WorkflowYAMLManager.load("nonexistent_workflow")

    def test_save_workflow_yaml_roundtrip(self, tmp_path, monkeypatch):
        """save_workflow_yaml writes valid data that load_workflow_yaml can read back."""
        import shutil
        from pathlib import Path
        import business_infinity.boardroom.yaml_manager as yaml_manager_module

        # Copy the real YAML into a temp project layout
        real_yaml = Path(__file__).parent.parent / "docs/workflow/samples/pitch.yaml"
        fake_project = tmp_path / "project"
        fake_samples = fake_project / "docs" / "workflow" / "samples"
        fake_samples.mkdir(parents=True)
        shutil.copy(real_yaml, fake_samples / "pitch.yaml")

        # Patch PROJECT_ROOT where yaml_manager imported it.
        monkeypatch.setattr(yaml_manager_module, "PROJECT_ROOT", fake_project)

        original = WorkflowYAMLManager.load("pitch_business_infinity")
        # Mutate one step's narrative
        original["steps"]["paul_graham_intro"]["narrative"] = "Updated narrative"
        WorkflowYAMLManager.save("pitch_business_infinity", original)

        reloaded = WorkflowYAMLManager.load("pitch_business_infinity")
        assert reloaded["steps"]["paul_graham_intro"]["narrative"] == "Updated narrative"

    def test_save_workflow_yaml_missing_workflow_id(self):
        """save_workflow_yaml raises ValueError when workflow_id is absent."""
        with pytest.raises(ValueError, match="workflow_id"):
            WorkflowYAMLManager.save("pitch_business_infinity", {"steps": {}})

    def test_save_workflow_yaml_invalid_step(self):
        """save_workflow_yaml raises ValueError for a step missing required fields."""
        bad_data = {
            "workflow_id": "pitch_business_infinity",
            "steps": {
                "bad_step": {"narrative": "ok"},  # missing response + actions
            },
        }
        with pytest.raises(ValueError, match="response"):
            WorkflowYAMLManager.save("pitch_business_infinity", bad_data)


class TestBoardroomStateManager:
    """Test BoardroomStateManager for JSON-LD agent and boardroom state."""

    def test_get_boardroom_state_returns_dict(self):
        """get_boardroom_state returns a dict with required collective keys."""
        state = BoardroomStateManager.get_boardroom_state()
        assert isinstance(state, dict)
        assert "status" in state
        assert "current_topic" in state

    def test_get_boardroom_state_jsonld_keys(self):
        """Boardroom state has JSON-LD @context and @type."""
        state = BoardroomStateManager.get_boardroom_state()
        assert "@context" in state
        assert "@type" in state

    def test_load_agent_state_founder(self):
        """load_agent_state returns segregated context/content plus aliases."""
        state = BoardroomStateManager.load_agent_state("founder")
        assert "context" in state
        assert "content" in state
        assert "context_management" in state
        assert "content_management" in state
        assert "innate_essence" in state
        assert "executive_function" in state

    def test_load_agent_state_cmo(self):
        """load_agent_state works for CMO agent."""
        state = BoardroomStateManager.load_agent_state("cmo")
        assert "name" in state["context"]
        assert "current_focus" in state["content"]

    def test_load_agent_state_cto(self):
        """load_agent_state works for CTO agent — legend: Alan Turing."""
        state = BoardroomStateManager.load_agent_state("cto")
        assert state["context"]["name"] == "Alan Turing"
        assert "core_logic" in state["context"]
        assert "active_strategy" in state["content"]

    def test_load_agent_state_ceo(self):
        """load_agent_state works for CEO agent."""
        state = BoardroomStateManager.load_agent_state("ceo")
        assert state["@type"] == "CEOAgent"
        assert "fixed_mandate" in state["context"]

    def test_load_agent_state_cfo(self):
        """load_agent_state works for CFO agent."""
        state = BoardroomStateManager.load_agent_state("cfo")
        assert state["@type"] == "CFOAgent"
        assert state["context"]["name"] == "Warren Buffett"

    def test_load_agent_state_coo(self):
        """load_agent_state works for COO agent."""
        state = BoardroomStateManager.load_agent_state("coo")
        assert state["@type"] == "COOAgent"
        assert state["context"]["name"] == "W. Edwards Deming"

    def test_load_agent_state_chro(self):
        """load_agent_state works for CHRO agent."""
        state = BoardroomStateManager.load_agent_state("chro")
        assert state["@type"] == "CHROAgent"
        assert state["context"]["name"] == "Peter Drucker"

    def test_load_agent_state_cso(self):
        """load_agent_state works for CSO agent — legend: Sun Tzu."""
        state = BoardroomStateManager.load_agent_state("cso")
        assert state["context"]["name"] == "Sun Tzu"
        assert "context" in state
        assert "content" in state

    def test_load_agent_context_returns_read_only_layer(self):
        """load_agent_context returns only the static context section."""
        context = BoardroomStateManager.load_agent_context("ceo")
        assert "fixed_mandate" in context
        assert "current_focus" not in context

    def test_all_agent_contexts_have_enrichment_fields(self):
        """Every agent context has the legend-derived enrichment fields from boardroom-agents spec."""
        enrichment_fields = ("domain_knowledge", "skills", "persona", "language")
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            ctx = BoardroomStateManager.load_agent_context(agent_id)
            for field in enrichment_fields:
                assert field in ctx, f"{agent_id} context missing '{field}'"

    def test_context_enrichment_types(self):
        """domain_knowledge and skills are lists of 4–5 items; persona and language are strings."""
        ctx = BoardroomStateManager.load_agent_context("ceo")
        assert isinstance(ctx["domain_knowledge"], list)
        assert 4 <= len(ctx["domain_knowledge"]) <= 5
        assert isinstance(ctx["skills"], list)
        assert 4 <= len(ctx["skills"]) <= 5
        assert isinstance(ctx["persona"], str)
        assert isinstance(ctx["language"], str)

    def test_load_agent_content_returns_dynamic_layer(self):
        """load_agent_content returns only the dynamic content section."""
        content = BoardroomStateManager.load_agent_content("ceo")
        assert "current_focus" in content
        assert "fixed_mandate" not in content
        assert "company_state" in content
        assert "product_state" in content

    def test_load_agent_company_state_returns_perspective(self):
        """load_agent_company_state returns the ASI Saga perspective payload."""
        state = BoardroomStateManager.load_agent_company_state("ceo")
        assert state["entity_name"] == "ASI Saga"
        assert "software_interfaces" in state

    def test_load_agent_product_state_returns_perspective(self):
        """load_agent_product_state returns the Business Infinity perspective payload."""
        state = BoardroomStateManager.load_agent_product_state("ceo")
        assert state["entity_name"] == "Business Infinity"
        assert "domain_knowledge" in state

    def test_load_agent_state_unknown_raises(self):
        """load_agent_state raises ValueError for an unregistered agent ID."""
        with pytest.raises(ValueError, match="Unknown agent ID"):
            BoardroomStateManager.load_agent_state("unknown_agent")

    def test_get_all_agent_states_returns_dict(self):
        """get_all_agent_states returns a dict keyed by agent ID."""
        states = BoardroomStateManager.get_all_agent_states()
        assert isinstance(states, dict)
        # At minimum, founders and core roles should be loaded
        assert len(states) > 0

    def test_get_all_agent_states_covers_c_suite(self):
        """get_all_agent_states includes all C-suite roles with state files."""
        states = BoardroomStateManager.get_all_agent_states()
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            assert agent_id in states, f"{agent_id} missing from get_all_agent_states()"

    def test_get_all_agent_states_have_innate_essence(self):
        """Every returned agent state has segregated context/content."""
        states = BoardroomStateManager.get_all_agent_states()
        for agent_id, state in states.items():
            assert "context" in state, f"{agent_id} missing context"
            assert "content" in state, f"{agent_id} missing content"

    def test_get_all_agent_contexts_returns_all_contexts(self):
        """get_all_agent_contexts returns only static agent layers."""
        contexts = BoardroomStateManager.get_all_agent_contexts()
        assert "ceo" in contexts
        assert "fixed_mandate" in contexts["ceo"]
        assert "current_focus" not in contexts["ceo"]

    def test_get_all_agent_contents_returns_all_contents(self):
        """get_all_agent_contents returns only dynamic agent layers."""
        contents = BoardroomStateManager.get_all_agent_contents()
        assert "ceo" in contents
        assert "current_focus" in contents["ceo"]
        assert "fixed_mandate" not in contents["ceo"]

    def test_get_all_agent_company_states_returns_all_perspectives(self):
        """get_all_agent_company_states returns ASI Saga perspectives."""
        states = BoardroomStateManager.get_all_agent_company_states()
        assert "ceo" in states
        assert states["ceo"]["entity_name"] == "ASI Saga"

    def test_get_all_agent_product_states_returns_all_perspectives(self):
        """get_all_agent_product_states returns Business Infinity perspectives."""
        states = BoardroomStateManager.get_all_agent_product_states()
        assert "ceo" in states
        assert states["ceo"]["entity_name"] == "Business Infinity"

    def test_agent_files_mapping_covers_c_suite(self):
        """The public agent registry covers all C-suite agent IDs."""
        registered_agent_ids = BoardroomStateManager.get_registered_agent_ids()
        for agent_id in C_SUITE_AGENT_IDS:
            assert agent_id in registered_agent_ids, (
                f"{agent_id} missing from BoardroomStateManager.get_registered_agent_ids()"
            )

    def test_update_executive_function_persists_changes(self, tmp_path, monkeypatch):
        """Legacy update_executive_function alias persists changes to content."""
        import shutil

        import business_infinity.boardroom as boardroom_module

        # Copy real CEO state file into a temp Manas directory
        real_state = boardroom_module.BoardroomStateManager.get_mind_dir() / "ceo" / "Manas" / "ceo.jsonld"
        fake_mind_dir = tmp_path / "boardroom" / "mind"
        fake_manas_dir = fake_mind_dir / "ceo" / "Manas"
        fake_manas_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_manas_dir / "ceo.jsonld")

        # Patch _MIND_DIR to point at the temp directory
        monkeypatch.setattr(BoardroomStateManager, "_MIND_DIR", fake_mind_dir)

        updated = BoardroomStateManager.update_executive_function(
            "ceo",
            {"current_focus": "Validated executive update"},
        )
        assert updated["executive_function"]["current_focus"] == "Validated executive update"
        assert updated["content"]["current_focus"] == "Validated executive update"

        reloaded = BoardroomStateManager.load_agent_state("ceo")
        assert reloaded["executive_function"]["current_focus"] == "Validated executive update"
        assert reloaded["content"]["current_focus"] == "Validated executive update"
        assert "name" in reloaded["context"]

    def test_update_agent_content_roundtrip(self, tmp_path, monkeypatch):
        """update_agent_content persists changes to the dynamic layer."""
        import shutil

        import business_infinity.boardroom as boardroom_module

        real_state = boardroom_module.BoardroomStateManager.get_mind_dir() / "founder" / "Manas" / "founder.jsonld"
        fake_mind_dir = tmp_path / "boardroom" / "mind"
        fake_manas_dir = fake_mind_dir / "founder" / "Manas"
        fake_manas_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_manas_dir / "founder.jsonld")

        monkeypatch.setattr(BoardroomStateManager, "_MIND_DIR", fake_mind_dir)

        updated = BoardroomStateManager.update_agent_content(
            "founder", {"spontaneous_intent": "Updated founder intent"}
        )
        assert updated["content"]["spontaneous_intent"] == "Updated founder intent"

        reloaded = BoardroomStateManager.load_agent_state("founder")
        assert reloaded["content"]["spontaneous_intent"] == "Updated founder intent"

    def test_update_boardroom_state_roundtrip(self, tmp_path, monkeypatch):
        """update_boardroom_state persists changes that get_boardroom_state reads back."""
        import shutil

        import business_infinity.boardroom as boardroom_module

        real_state = (
            boardroom_module.BoardroomStateManager.get_state_dir() / "boardroom.jsonld"
        )
        fake_state_dir = tmp_path / "boardroom" / "state"
        fake_state_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_state_dir / "boardroom.jsonld")

        monkeypatch.setattr(BoardroomStateManager, "_STATE_DIR", fake_state_dir)

        updated = BoardroomStateManager.update_boardroom_state(
            {"current_topic": "Validated boardroom update", "status": "Active"}
        )
        assert updated["current_topic"] == "Validated boardroom update"
        assert updated["status"] == "Active"

        reloaded = BoardroomStateManager.get_boardroom_state()
        assert reloaded["current_topic"] == "Validated boardroom update"

    def test_update_boardroom_state_rejects_unknown_keys(self):
        """update_boardroom_state raises ValueError for unrecognised keys."""
        with pytest.raises(ValueError, match="unrecognised keys"):
            BoardroomStateManager.update_boardroom_state({"bad_key": "value"})

    def test_update_agent_context_rejected(self):
        """Agent context is explicitly read-only."""
        with pytest.raises(PermissionError, match="read-only"):
            BoardroomStateManager.update_agent_context(
                "ceo", {"fixed_mandate": "Should not change"}
            )

    def test_context_preserved_after_content_update(self, tmp_path, monkeypatch):
        """Static context is unchanged after a content update."""
        import shutil

        import business_infinity.boardroom as boardroom_module

        real_state = boardroom_module.BoardroomStateManager.get_mind_dir() / "cfo" / "Manas" / "cfo.jsonld"
        fake_mind_dir = tmp_path / "boardroom" / "mind"
        fake_manas_dir = fake_mind_dir / "cfo" / "Manas"
        fake_manas_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_manas_dir / "cfo.jsonld")

        monkeypatch.setattr(BoardroomStateManager, "_MIND_DIR", fake_mind_dir)

        original = BoardroomStateManager.load_agent_state("cfo")
        original_name = original["context"]["name"]
        original_mandate = original["context"]["fixed_mandate"]

        BoardroomStateManager.update_agent_content(
            "cfo", {"current_focus": "New CFO focus"}
        )

        reloaded = BoardroomStateManager.load_agent_state("cfo")
        assert reloaded["context"]["name"] == original_name
        assert reloaded["context"]["fixed_mandate"] == original_mandate
        assert reloaded["content"]["current_focus"] == "New CFO focus"

    def test_load_environment_schema_validated(self):
        """load_state_records validates environment.jsonld."""
        state = BoardroomStateManager.load_state_records("environment.jsonld")
        assert state["@type"] == "InfrastructureManifest"
        assert "cloud_provider" in state

    def test_load_company_manifest_schema_validated(self):
        """load_company_manifest validates company.jsonld."""
        state = BoardroomStateManager.load_company_manifest()
        assert state["@id"] == "asi:saga"
        assert "portfolio" in state

    def test_company_manifest_context_enrichment(self):
        """company.jsonld context has legend-derived enrichment fields."""
        state = BoardroomStateManager.load_company_manifest()
        ctx = state.get("context", {})
        for field in ("domain_knowledge", "skills", "persona", "language"):
            assert field in ctx, f"company context missing '{field}'"
        assert isinstance(ctx["domain_knowledge"], list)
        assert 4 <= len(ctx["domain_knowledge"]) <= 5
        assert isinstance(ctx["skills"], list)
        assert 4 <= len(ctx["skills"]) <= 5

    def test_company_manifest_content_block(self):
        """company.jsonld content has current phase and active initiatives."""
        state = BoardroomStateManager.load_company_manifest()
        content = state.get("content", {})
        assert "current_phase" in content
        assert "active_initiatives" in content
        assert isinstance(content["active_initiatives"], list)
        assert "boardroom_activation" in content

    def test_load_product_manifest_schema_validated(self):
        """load_product_manifest validates business-infinity.jsonld."""
        records = BoardroomStateManager.load_product_manifest()
        assert len(records) == 5
        assert any(record["@id"] == "bi:product:core" for record in records)

    def test_product_manifest_core_enrichment(self):
        """bi:product:core has legend-derived enrichment fields."""
        records = BoardroomStateManager.load_product_manifest()
        core = next(r for r in records if r["@id"] == "bi:product:core")
        for field in ("domain_knowledge", "skills", "persona", "language"):
            assert field in core, f"bi:product:core missing '{field}'"
        assert isinstance(core["domain_knowledge"], list)
        assert 4 <= len(core["domain_knowledge"]) <= 5

    def test_product_manifest_architecture_enrichment(self):
        """bi:arch:modular has rationale and principles."""
        records = BoardroomStateManager.load_product_manifest()
        arch = next(r for r in records if r["@id"] == "bi:arch:modular")
        assert "rationale" in arch
        assert "principles" in arch
        assert isinstance(arch["principles"], list)

    def test_product_manifest_all_records_enriched(self):
        """All 5 product records have been enriched with at least one extra field."""
        records = BoardroomStateManager.load_product_manifest()
        extra_fields = {"domain_knowledge", "rationale", "description", "capabilities", "algorithm"}
        for record in records:
            assert extra_fields & set(record.keys()), (
                f"{record['@id']} has no enrichment fields"
            )

    def test_load_mvp_schema_validated(self):
        """load_state_records validates mvp.jsonld record structure."""
        records = BoardroomStateManager.load_state_records("mvp.jsonld")
        assert len(records) > 0
        assert all("@type" in record for record in records)

    def test_load_agent_buddhi_returns_intellect_document(self):
        """load_agent_buddhi returns the Buddhi intellect document for each agent."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            buddhi = BoardroomStateManager.load_agent_buddhi(agent_id)
            assert buddhi["@type"] == "Buddhi", f"{agent_id} Buddhi missing @type"
            assert buddhi["agent_id"] == agent_id
            for field in ("domain_knowledge", "skills", "persona", "language"):
                assert field in buddhi, f"{agent_id} Buddhi missing '{field}'"

    def test_load_agent_buddhi_intellect_fields_are_non_empty(self):
        """Buddhi intellect fields are non-empty lists/strings for all agents."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            buddhi = BoardroomStateManager.load_agent_buddhi(agent_id)
            assert isinstance(buddhi["domain_knowledge"], list)
            assert len(buddhi["domain_knowledge"]) >= 4
            assert isinstance(buddhi["skills"], list)
            assert len(buddhi["skills"]) >= 4
            assert isinstance(buddhi["persona"], str) and buddhi["persona"]
            assert isinstance(buddhi["language"], str) and buddhi["language"]

    def test_load_agent_buddhi_unknown_agent_raises(self):
        """load_agent_buddhi raises ValueError for unknown agent IDs."""
        with pytest.raises(ValueError, match="Unknown agent ID"):
            BoardroomStateManager.load_agent_buddhi("unknown_agent")

    def test_mind_dir_points_to_boardroom_mind(self):
        """get_mind_dir returns the boardroom/mind directory path."""
        mind_dir = BoardroomStateManager.get_mind_dir()
        assert mind_dir.name == "mind"
        assert mind_dir.parent.name == "boardroom"

    def test_agent_manas_files_in_mind_directory(self):
        """All agent Manas files exist under boardroom/mind/{agent}/Manas/."""
        mind_dir = BoardroomStateManager.get_mind_dir()
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            manas_dir = mind_dir / agent_id / "Manas"
            assert manas_dir.is_dir(), f"{agent_id} Manas directory missing"
            manas_files = list(manas_dir.iterdir())
            assert len(manas_files) >= 1, f"{agent_id} Manas directory is empty"

    def test_agent_buddhi_files_in_mind_directory(self):
        """All agent Buddhi files exist under boardroom/mind/{agent}/Buddhi/."""
        mind_dir = BoardroomStateManager.get_mind_dir()
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            buddhi_path = mind_dir / agent_id / "Buddhi" / "buddhi.jsonld"
            assert buddhi_path.exists(), f"{agent_id} Buddhi file missing at {buddhi_path}"

    def test_buddhi_context_aligns_with_manas_context(self):
        """Buddhi domain_knowledge and skills align with the agent's Manas context layer."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            ctx = BoardroomStateManager.load_agent_context(agent_id)
            buddhi = BoardroomStateManager.load_agent_buddhi(agent_id)
            assert buddhi["domain_knowledge"] == ctx["domain_knowledge"], (
                f"{agent_id} Buddhi domain_knowledge diverges from Manas context"
            )
            assert buddhi["skills"] == ctx["skills"], (
                f"{agent_id} Buddhi skills diverge from Manas context"
            )


class TestMindFileSchemas:
    """Test the schema registry and schema-based file loading mechanism."""

    def test_schemas_dir_exists(self):
        """get_schemas_dir returns an existing boardroom/mind/schemas/ directory."""
        schemas_dir = BoardroomStateManager.get_schemas_dir()
        assert schemas_dir.is_dir(), f"Schemas directory missing at {schemas_dir}"
        assert schemas_dir.name == "schemas"
        assert schemas_dir.parent.name == "mind"

    def test_all_expected_schema_files_present(self):
        """All seven mind schema files exist in the schemas directory."""
        schemas_dir = BoardroomStateManager.get_schemas_dir()
        expected = [
            "manas.schema.json",
            "buddhi.schema.json",
            "action-plan.schema.json",
            "ahankara.schema.json",
            "chitta.schema.json",
            "entity-context.schema.json",
            "entity-content.schema.json",
        ]
        for name in expected:
            path = schemas_dir / name
            assert path.exists(), f"Schema file missing: {path}"

    def test_mind_file_schemas_keys_registered(self):
        """_MIND_FILE_SCHEMAS contains all expected dimension keys."""
        schemas = BoardroomStateManager._MIND_FILE_SCHEMAS
        expected_keys = {
            "Manas/state",
            "Buddhi/buddhi.jsonld",
            "Buddhi/action-plan.jsonld",
            "Ahankara/ahankara.jsonld",
            "Chitta/chitta.jsonld",
            "Manas/context/entity",
            "Manas/content/entity",
        }
        assert expected_keys == set(schemas.keys())

    def test_load_mind_file_buddhi(self):
        """load_mind_file loads and validates buddhi.jsonld for each agent."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            doc = BoardroomStateManager.load_mind_file(
                agent_id, "Buddhi", "buddhi.jsonld"
            )
            assert doc["@type"] == "Buddhi", f"{agent_id}: missing @type"
            assert doc["agent_id"] == agent_id

    def test_load_mind_file_ahankara(self):
        """load_mind_file loads and validates ahankara.jsonld for each agent."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            doc = BoardroomStateManager.load_mind_file(
                agent_id, "Ahankara", "ahankara.jsonld"
            )
            assert doc["@type"] == "Ahankara", f"{agent_id}: missing @type"
            assert doc["agent_id"] == agent_id
            for field in (
                "identity",
                "contextual_axis",
                "non_negotiables",
                "identity_markers",
                "intellect_constraint",
            ):
                assert field in doc, f"{agent_id} Ahankara missing '{field}'"

    def test_load_mind_file_chitta(self):
        """load_mind_file loads and validates chitta.jsonld for each agent."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            doc = BoardroomStateManager.load_mind_file(
                agent_id, "Chitta", "chitta.jsonld"
            )
            assert doc["@type"] == "Chitta", f"{agent_id}: missing @type"
            assert doc["agent_id"] == agent_id
            for field in (
                "intelligence_nature",
                "cosmic_intelligence",
                "beyond_identity",
                "consciousness_basis",
            ):
                assert field in doc, f"{agent_id} Chitta missing '{field}'"

    def test_load_mind_file_action_plan(self):
        """load_mind_file loads and validates action-plan.jsonld for each agent."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            doc = BoardroomStateManager.load_mind_file(
                agent_id, "Buddhi", "action-plan.jsonld"
            )
            assert "@type" in doc, f"{agent_id}: action-plan missing @type"
            assert "actionSteps" in doc
            assert len(doc["actionSteps"]) >= 1

    def test_load_mind_file_entity_context(self):
        """load_mind_file loads and validates Manas/context entity files."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            for entity_file in ("company.jsonld", "business-infinity.jsonld"):
                doc = BoardroomStateManager.load_mind_file(
                    agent_id, "Manas/context", entity_file
                )
                assert "agent_perspective" in doc, (
                    f"{agent_id} context/{entity_file} missing 'agent_perspective'"
                )
                assert "domain_knowledge" in doc
                assert "skills" in doc

    def test_load_mind_file_entity_content(self):
        """load_mind_file loads and validates Manas/content entity files."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            for entity_file in ("company.jsonld", "business-infinity.jsonld"):
                doc = BoardroomStateManager.load_mind_file(
                    agent_id, "Manas/content", entity_file
                )
                assert "agent_perspective" in doc, (
                    f"{agent_id} content/{entity_file} missing 'agent_perspective'"
                )
                assert "perspective" in doc
                assert "current_signals" in doc

    def test_load_mind_file_unknown_agent_raises(self):
        """load_mind_file raises ValueError for unknown agent IDs."""
        with pytest.raises(ValueError, match="Unknown agent ID"):
            BoardroomStateManager.load_mind_file(
                "unknown_agent", "Buddhi", "buddhi.jsonld"
            )

    def test_load_agent_mind_returns_all_dimensions(self):
        """load_agent_mind returns all four dimensions for each agent."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            mind = BoardroomStateManager.load_agent_mind(agent_id)
            assert set(mind.keys()) == {"Manas", "Buddhi", "Ahankara", "Chitta"}, (
                f"{agent_id}: load_agent_mind missing dimensions"
            )

    def test_load_agent_mind_manas_matches_load_agent_state(self):
        """load_agent_mind Manas matches load_agent_state for all agents."""
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            mind = BoardroomStateManager.load_agent_mind(agent_id)
            state = BoardroomStateManager.load_agent_state(agent_id)
            assert mind["Manas"]["@id"] == state["@id"], (
                f"{agent_id}: load_agent_mind Manas @id mismatch"
            )

    def test_load_agent_mind_unknown_agent_raises(self):
        """load_agent_mind raises ValueError for unknown agent IDs."""
        with pytest.raises(ValueError, match="Unknown agent ID"):
            BoardroomStateManager.load_agent_mind("unknown_agent")

    def test_per_agent_readme_files_exist(self):
        """Each agent directory contains a Readme.md file."""
        mind_dir = BoardroomStateManager.get_mind_dir()
        for agent_id in BoardroomStateManager.get_registered_agent_ids():
            readme = mind_dir / agent_id / "Readme.md"
            assert readme.exists(), f"{agent_id}: Readme.md missing at {readme}"


class TestBoardroomWorkflowContext:
    """Test that workflow payloads include per-agent company/product state."""

    @pytest.mark.asyncio
    async def test_boardroom_debate_includes_agent_perspective_states(
        self, monkeypatch
    ):
        """boardroom_debate passes company/product state for all agents."""
        import business_infinity.workflows as workflows_module

        async def fake_select_c_suite_agents(client):
            return [AgentDouble("ceo"), AgentDouble("cfo"), AgentDouble("cmo")]

        monkeypatch.setattr(
            workflows_module,
            "select_c_suite_agents",
            fake_select_c_suite_agents,
        )

        client = CaptureClient()
        request = RequestDouble(
            {
                "event": "Market shift",
                "event_source": "market",
                "company_purpose": "Build purposeful autonomous operating systems",
                "context": {"segment": "B2B"},
            },
            client,
        )

        result = await workflows_module.boardroom_debate(request)

        assert result["status"] == "running"
        context = client.kwargs["context"]
        assert "agent_company_states" in context
        assert "agent_product_states" in context
        assert context["agent_company_states"]["ceo"]["entity_name"] == "ASI Saga"
        assert (
            context["agent_product_states"]["cfo"]["entity_name"]
            == "Business Infinity"
        )

    @pytest.mark.asyncio
    async def test_workflow_orchestration_includes_owner_perspective_states(self):
        """workflow_orchestration passes owner company/product state."""
        import business_infinity.workflows as workflows_module

        client = CaptureClient()
        client.agents = [AgentDouble("founder"), AgentDouble("ceo")]
        request = RequestDouble(
            {
                "workflow_id": "pitch_business_infinity",
                "company_purpose": "Deliver reliable innovation that earns trust",
            },
            client,
        )

        result = await workflows_module.workflow_orchestration(request)

        assert result["owner"] == "founder"
        context = client.kwargs["context"]
        assert context["owner_company_state"]["entity_name"] == "ASI Saga"
        assert context["owner_product_state"]["entity_name"] == "Business Infinity"
        assert "company_manifest" in context
        assert "product_manifest" in context
