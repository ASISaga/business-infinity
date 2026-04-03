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
    BoardroomStateManager,
    CXO_DOMAINS,
    CXO_PATHWAY_TYPES,
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
        data = load_workflow_yaml("pitch_business_infinity")
        assert data["workflow_id"] == "pitch_business_infinity"
        assert data["owner"] == "founder"
        assert "steps" in data
        assert len(data["steps"]) == 9
        assert "paul_graham_intro" in data["steps"]
        assert "final_reveal" in data["steps"]

    def test_load_workflow_yaml_step_fields(self):
        """Each step has narrative, response, actions, and navigation."""
        data = load_workflow_yaml("pitch_business_infinity")
        for step_id, step in data["steps"].items():
            assert "narrative" in step, f"{step_id} missing narrative"
            assert "response" in step, f"{step_id} missing response"
            assert "actions" in step, f"{step_id} missing actions"
            assert isinstance(step["actions"], list), f"{step_id} actions not a list"

    def test_load_workflow_yaml_all_six(self):
        """load_workflow_yaml works for all six registered workflows."""
        for workflow_id in WORKFLOW_REGISTRY:
            data = load_workflow_yaml(workflow_id)
            assert data["workflow_id"] == workflow_id
            assert "steps" in data
            assert len(data["steps"]) > 0

    def test_load_workflow_yaml_unknown(self):
        """load_workflow_yaml raises KeyError for an unknown workflow."""
        with pytest.raises(KeyError):
            load_workflow_yaml("nonexistent_workflow")

    def test_save_workflow_yaml_roundtrip(self, tmp_path, monkeypatch):
        """save_workflow_yaml writes valid data that load_workflow_yaml can read back."""
        import shutil
        from pathlib import Path
        import business_infinity.boardroom as boardroom_module

        # Copy the real YAML into a temp project layout
        real_yaml = Path(__file__).parent.parent / "docs/workflow/samples/pitch.yaml"
        fake_project = tmp_path / "project"
        fake_samples = fake_project / "docs" / "workflow" / "samples"
        fake_samples.mkdir(parents=True)
        shutil.copy(real_yaml, fake_samples / "pitch.yaml")

        # Patch the boardroom module's __file__ so _resolve_yaml_path points at
        # our temp directory (two levels up from a fake src/business_infinity/).
        fake_pkg = fake_project / "src" / "business_infinity" / "boardroom.py"
        monkeypatch.setattr(boardroom_module, "__file__", str(fake_pkg))

        original = load_workflow_yaml("pitch_business_infinity")
        # Mutate one step's narrative
        original["steps"]["paul_graham_intro"]["narrative"] = "Updated narrative"
        save_workflow_yaml("pitch_business_infinity", original)

        reloaded = load_workflow_yaml("pitch_business_infinity")
        assert reloaded["steps"]["paul_graham_intro"]["narrative"] == "Updated narrative"

    def test_save_workflow_yaml_missing_workflow_id(self):
        """save_workflow_yaml raises ValueError when workflow_id is absent."""
        with pytest.raises(ValueError, match="workflow_id"):
            save_workflow_yaml("pitch_business_infinity", {"steps": {}})

    def test_save_workflow_yaml_invalid_step(self):
        """save_workflow_yaml raises ValueError for a step missing required fields."""
        bad_data = {
            "workflow_id": "pitch_business_infinity",
            "steps": {
                "bad_step": {"narrative": "ok"},  # missing response + actions
            },
        }
        with pytest.raises(ValueError, match="response"):
            save_workflow_yaml("pitch_business_infinity", bad_data)


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
        """load_agent_state works for CTO agent."""
        state = BoardroomStateManager.load_agent_state("cto")
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
        """load_agent_state works for CSO agent."""
        state = BoardroomStateManager.load_agent_state("cso")
        assert "context" in state
        assert "content" in state

    def test_load_agent_context_returns_read_only_layer(self):
        """load_agent_context returns only the static context section."""
        context = BoardroomStateManager.load_agent_context("ceo")
        assert "fixed_mandate" in context
        assert "current_focus" not in context

    def test_load_agent_content_returns_dynamic_layer(self):
        """load_agent_content returns only the dynamic content section."""
        content = BoardroomStateManager.load_agent_content("ceo")
        assert "current_focus" in content
        assert "fixed_mandate" not in content

    def test_load_agent_state_unknown_raises(self):
        """load_agent_state raises KeyError for an unregistered agent ID."""
        with pytest.raises(KeyError):
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

    def test_agent_files_mapping_covers_c_suite(self):
        """The public agent registry covers all C-suite agent IDs."""
        registered_agent_ids = BoardroomStateManager.get_registered_agent_ids()
        for agent_id in C_SUITE_AGENT_IDS:
            assert agent_id in registered_agent_ids, (
                f"{agent_id} missing from BoardroomStateManager.get_registered_agent_ids()"
            )

    def test_update_content_roundtrip_via_executive_function_alias(self, tmp_path, monkeypatch):
        """Legacy update_executive_function alias persists changes to content."""
        import shutil
        import business_infinity.boardroom as boardroom_module

        # Copy real CEO state file into a temp directory
        real_state = boardroom_module.BoardroomStateManager.get_state_dir() / "ceo.jsonld"
        fake_state_dir = tmp_path / "boardroom" / "state"
        fake_state_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_state_dir / "ceo.jsonld")

        # Patch _STATE_DIR to point at the temp directory
        monkeypatch.setattr(BoardroomStateManager, "_STATE_DIR", fake_state_dir)

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

        real_state = boardroom_module.BoardroomStateManager.get_state_dir() / "founder.jsonld"
        fake_state_dir = tmp_path / "boardroom" / "state"
        fake_state_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_state_dir / "founder.jsonld")

        monkeypatch.setattr(BoardroomStateManager, "_STATE_DIR", fake_state_dir)

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

        real_state = boardroom_module.BoardroomStateManager.get_state_dir() / "cfo.jsonld"
        fake_state_dir = tmp_path / "boardroom" / "state"
        fake_state_dir.mkdir(parents=True)
        shutil.copy(real_state, fake_state_dir / "cfo.jsonld")

        monkeypatch.setattr(BoardroomStateManager, "_STATE_DIR", fake_state_dir)

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
        """load_state_records validates environment.jsonl."""
        state = BoardroomStateManager.load_state_records("environment.jsonl")
        assert state["@type"] == "InfrastructureManifest"
        assert "cloud_provider" in state

    def test_load_mvp_schema_validated(self):
        """load_state_records validates mvp.jsonl record structure."""
        records = BoardroomStateManager.load_state_records("mvp.jsonl")
        assert len(records) > 0
        assert all("@type" in record for record in records)
