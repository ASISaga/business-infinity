"""BusinessInfinity Boardroom — philosophy-derived constants and domain mappings.

The boardroom encodes the core philosophy of BusinessInfinity: a purpose-driven
decision tree debate where each CXO agent applies domain leadership to propose
pathways, which are evaluated through resonance scoring against the company's
purpose, and synthesised into autonomous action.

The boardroom chat interface supports two modes through the same ``<chatroom>``
Web Component:

1. **Structured workflow** — A workflow-owner agent conducts a step-by-step
   conversation with an external entity (investor, customer, new business).
   Steps are loaded from YAML files in ``docs/workflow/samples/``.

2. **Dynamic discussion** — The full boardroom of CXO agents engages in
   purpose-driven debate for business decision-making.  No YAML steps; the
   conversation is orchestrated dynamically by AOS.

Both modes use MCP app payloads (``app_id: "boardroom_ui"``) delivered via
SSE through the Agent Operating System.  All conversations are persisted by
``subconscious.asisaga.com``.

See ``docs/philosophy.md`` for the full philosophy specification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

# ── CXO Domain Leadership ───────────────────────────────────────────────────
#
# Each C-suite agent leads a specific domain and proposes a characteristic
# pathway type during boardroom debates.  The mapping is derived from the
# philosophy's legendary CXO archetypes.


CXO_DOMAINS: Dict[str, Dict[str, str]] = {
    "ceo": {
        "archetype": "Jobs",
        "title": "Chief Executive Officer",
        "domain": "Vision & Strategy",
        "pathway": "narrative",
        "description": "Proposes narrative pathways that reframe challenges through the lens of the company's purpose and long-term vision.",
    },
    "cfo": {
        "archetype": "Buffett",
        "title": "Chief Financial Officer",
        "domain": "Finance & Resources",
        "pathway": "resource-allocation",
        "description": "Proposes resource allocation pathways grounded in fiscal discipline and long-term value creation.",
    },
    "coo": {
        "archetype": "Deming",
        "title": "Chief Operating Officer",
        "domain": "Operations & Workflow",
        "pathway": "workflow",
        "description": "Proposes workflow pathways that optimise operational processes and drive continuous improvement.",
    },
    "cmo": {
        "archetype": "Ogilvy",
        "title": "Chief Marketing Officer",
        "domain": "Market & Communication",
        "pathway": "communication",
        "description": "Proposes communication pathways that shape market perception and strengthen customer relationships.",
    },
    "chro": {
        "archetype": "Drucker",
        "title": "Chief Human Resources Officer",
        "domain": "People & Culture",
        "pathway": "people-centric",
        "description": "Proposes people-centric pathways that cultivate talent, culture, and authentic engagement.",
    },
    "cto": {
        "archetype": "Turing",
        "title": "Chief Technology Officer",
        "domain": "Technology & Innovation",
        "pathway": "technology",
        "description": "Proposes technology pathways that harness innovation and digital capability to advance the company's purpose.",
    },
    "cso": {
        "archetype": "Sun Tzu",
        "title": "Chief Strategy Officer",
        "domain": "Strategy & Competitive Intelligence",
        "pathway": "strategic",
        "description": "Proposes strategic pathways informed by competitive intelligence and long-range positioning.",
    },
}


# ── Boardroom Debate Constants ───────────────────────────────────────────────

#: Purpose statement for the boardroom debate orchestration.
BOARDROOM_DEBATE_PURPOSE = (
    "Conduct a purpose-driven decision tree debate where each CXO agent "
    "proposes domain-specific pathways in response to the triggering event, "
    "challenges and refines competing pathways through structured debate, "
    "scores each pathway for resonance with the company's purpose, and "
    "converges on an autonomous action that most fully embodies that purpose."
)

#: Scope of the boardroom debate orchestration.
BOARDROOM_DEBATE_SCOPE = (
    "Full C-suite boardroom convergence: event interpretation, multi-domain "
    "pathway proposals, cross-functional debate, resonance scoring at CXO and "
    "boardroom levels, and synthesis into a unified autonomous action."
)

#: All CXO pathway types derived from the philosophy.
CXO_PATHWAY_TYPES = list(dict.fromkeys(domain["pathway"] for domain in CXO_DOMAINS.values()))


# ── Boardroom State Manager ──────────────────────────────────────────────────
#
# The boardroom maintains two layers of JSON-LD state for each agent:
#
#   - **Innate Essence** (immutable): fixed identity, mandate, and constraints
#     — the agent's "constitution", never modified at runtime.
#   - **Executive Function** (mutable): active focus, strategy, short-term
#     memory, and spontaneous intent — the agent's conscious workspace.
#
# Collective boardroom state (topic, resonance scores, active directives) is
# stored separately in ``boardroom.jsonld``.
#
# All state files live in ``boardroom/state/`` at the project root.


class BoardroomStateManager:
    """Manages JSON-LD agent and boardroom state for the BusinessInfinity boardroom.

    State is stored as JSON-LD files in ``boardroom/state/``.  Each agent has
    its own file containing ``innate_essence`` (immutable) and
    ``executive_function`` (mutable).  The collective boardroom state lives in
    ``boardroom.jsonld``.

    Only the ``executive_function`` section of an agent file may be updated at
    runtime — ``innate_essence`` is the agent's permanent constitution and is
    never overwritten.
    """

    #: Path to the ``boardroom/state/`` directory relative to the project root.
    _STATE_DIR: Path = Path(__file__).parent.parent.parent / "boardroom" / "state"

    #: Mapping from agent ID to state filename stem (without extension).
    #: Extensions ``.jsonld`` and ``.jsonl`` are both supported.
    _AGENT_FILES: Dict[str, str] = {
        "ceo": "ceo",
        "cfo": "cfo",
        "coo": "coo",
        "cmo": "cmo",
        "chro": "chro",
        "cto": "cto",
        "cso": "cso",
        "founder": "founder",
    }

    @classmethod
    def _state_path(cls, filename: str) -> Path:
        """Resolve a state filename stem to its absolute path.

        Tries ``.jsonld`` first, then ``.jsonl``.

        Raises :class:`FileNotFoundError` if neither variant exists.
        """
        for ext in (".jsonld", ".jsonl"):
            path = cls._STATE_DIR / (filename + ext)
            if path.exists():
                return path
        raise FileNotFoundError(
            f"State file '{filename}' not found in {cls._STATE_DIR} "
            f"(tried .jsonld and .jsonl)"
        )

    @classmethod
    def load_agent_state(cls, agent_id: str) -> Dict[str, Any]:
        """Load the full state (innate_essence + executive_function) for an agent.

        Raises :class:`KeyError` if *agent_id* is not mapped to a state file.
        Raises :class:`FileNotFoundError` if the state file does not exist.
        """
        filename = cls._AGENT_FILES[agent_id]  # raises KeyError for unknown IDs
        path = cls._state_path(filename)
        with open(str(path), "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        # Support both single-object JSON (.jsonld) and line-delimited JSON (.jsonl).
        # For multi-object .jsonl files the first object is the agent's primary state.
        first_line = content.split("\n")[0].strip()
        try:
            return json.loads(first_line)
        except json.JSONDecodeError:
            return json.loads(content)

    @classmethod
    def update_executive_function(
        cls, agent_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the mutable ``executive_function`` section of an agent's state.

        Merges *updates* into the existing ``executive_function`` dict.  The
        ``innate_essence`` section is never touched.

        Returns the full updated agent state.

        Raises :class:`KeyError` if *agent_id* is not registered.
        Raises :class:`FileNotFoundError` if the state file does not exist.
        """
        state = cls.load_agent_state(agent_id)
        filename = cls._AGENT_FILES[agent_id]
        path = cls._state_path(filename)

        ef = state.get("executive_function", {})
        ef.update(updates)
        state["executive_function"] = ef

        with open(str(path), "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

        return state

    @classmethod
    def get_boardroom_state(cls) -> Dict[str, Any]:
        """Return the current collective boardroom state from ``boardroom.jsonld``."""
        path = cls._STATE_DIR / "boardroom.jsonld"
        with open(str(path), "r", encoding="utf-8") as fh:
            return json.load(fh)

    @classmethod
    def update_boardroom_state(cls, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update the collective boardroom state.

        Permitted top-level update keys: ``status``, ``current_topic``,
        ``resonance_ledger``, ``active_directives``.  JSON-LD metadata keys
        (``@context``, ``@id``, ``@type``) are passed through unchanged.

        Returns the full updated boardroom state.

        Raises :class:`ValueError` for unrecognised keys.
        """
        _allowed_keys = {"status", "current_topic", "resonance_ledger", "active_directives"}
        unknown = set(updates.keys()) - _allowed_keys - {"@context", "@id", "@type"}
        if unknown:
            raise ValueError(
                f"update_boardroom_state: unrecognised keys {unknown}. "
                f"Allowed: {_allowed_keys}"
            )

        state = cls.get_boardroom_state()
        state.update(updates)

        path = cls._STATE_DIR / "boardroom.jsonld"
        with open(str(path), "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

        return state

    @classmethod
    def get_all_agent_states(cls) -> Dict[str, Dict[str, Any]]:
        """Return state for all agents that have state files.

        Agents without a state file are silently omitted from the result.
        """
        states: Dict[str, Dict[str, Any]] = {}
        for agent_id in cls._AGENT_FILES:
            try:
                states[agent_id] = cls.load_agent_state(agent_id)
            except FileNotFoundError:
                pass
        return states


# ── Structured Workflow Registry ─────────────────────────────────────────────
#
# Each structured workflow is owned by a boardroom agent and conducts a
# step-by-step conversation with an external entity.  The registry maps
# workflow IDs to their metadata.  Steps are loaded from YAML at runtime.

#: Registry of structured boardroom workflows.
#: Each entry maps a workflow_id to its owner agent, purpose, scope, and
#: the path to its YAML definition.
WORKFLOW_REGISTRY: Dict[str, Dict[str, str]] = {
    "pitch_business_infinity": {
        "owner": "founder",
        "purpose": (
            "Deliver the Business Infinity pitch as an interactive, step-by-step "
            "narrative through the boardroom interface, progressively revealing the "
            "product philosophy from LoRA-based founder agents through a purpose-driven "
            "C-suite boardroom to the self-learning ASI Saga loop."
        ),
        "scope": (
            "Interactive pitch delivery: load pitch workflow steps, present narratives "
            "with action buttons and navigation through the boardroom UI via MCP app "
            "payloads, and conclude with a live product demonstration reveal."
        ),
        "yaml_path": "docs/workflow/samples/pitch.yaml",
    },
    "onboard_new_business": {
        "owner": "coo",
        "purpose": (
            "Onboard a new business to Business Infinity by guiding them through "
            "purpose definition, CXO agent selection, MCP system connections, "
            "resonance configuration, and their first live boardroom session."
        ),
        "scope": (
            "Interactive onboarding: define company purpose, select CXO agents, "
            "connect business systems via MCP, configure resonance thresholds, "
            "invite team members, and launch the first boardroom debate."
        ),
        "yaml_path": "docs/workflow/samples/onboarding.yaml",
    },
    "marketing_business_infinity": {
        "owner": "cmo",
        "purpose": (
            "Market Business Infinity to a potential customer by revealing the "
            "pain of slow decision-making, introducing the purpose-driven boardroom "
            "concept, and demonstrating live product capabilities."
        ),
        "scope": (
            "Interactive marketing narrative: problem framing, product vision, "
            "CXO agent introduction, MCP integration, resonance governance, "
            "live proof via ASI Saga self-loop, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/marketing.yaml",
    },
    "crisis_response": {
        "owner": "ceo",
        "purpose": (
            "Activate the boardroom in emergency mode to assess crisis impact "
            "across all CXO domains, propose containment pathways, conduct rapid "
            "debate, and execute autonomous response with purpose alignment."
        ),
        "scope": (
            "Crisis activation: cross-domain impact assessment, CXO containment "
            "proposals, rapid debate, resonance-scored convergence, autonomous "
            "execution across connected systems, and recovery monitoring."
        ),
        "yaml_path": "docs/workflow/samples/crisis-response.yaml",
    },
    "quarterly_strategic_review": {
        "owner": "ceo",
        "purpose": (
            "Conduct a quarterly strategic review where each CXO agent reports "
            "on their domain, proposes strategic pathways, debates cross-functionally, "
            "and converges on a unified direction scored for purpose resonance."
        ),
        "scope": (
            "Quarterly review: domain reports from all CXOs, multi-domain strategic "
            "debate, resonance scoring, boardroom convergence, and quarterly "
            "action plan with autonomous execution governance."
        ),
        "yaml_path": "docs/workflow/samples/strategic-review.yaml",
    },
    "product_launch": {
        "owner": "ceo",
        "purpose": (
            "Orchestrate a cross-functional product launch through the boardroom, "
            "assessing readiness across market, finance, technology, operations, "
            "people, and strategy domains before converging on a go-to-market plan."
        ),
        "scope": (
            "Product launch orchestration: domain readiness assessments, cross-CXO "
            "launch debate, resonance-scored convergence, and unified go-to-market "
            "execution across all connected business systems."
        ),
        "yaml_path": "docs/workflow/samples/product-launch.yaml",
    },
}


def get_workflow_metadata(workflow_id: str) -> Dict[str, str]:
    """Return metadata for a registered structured workflow.

    Raises :class:`KeyError` if the workflow ID is not registered.
    """
    return WORKFLOW_REGISTRY[workflow_id]


def get_workflow_step_ids(workflow_id: str) -> List[str]:
    """Return ordered step IDs for a registered structured workflow.

    This reads the YAML file at runtime to extract the step order.
    Falls back to :data:`_PITCH_STEP_IDS` for the pitch workflow
    to maintain backward compatibility during the transition.

    Raises :class:`NotImplementedError` for non-pitch workflows until
    the aos-client-sdk YAML loader is available.
    """
    if workflow_id == "pitch_business_infinity":
        return list(_PITCH_STEP_IDS)
    # For other workflows, step IDs will be resolved at runtime from YAML
    # by the aos-client-sdk YAML loader once it is available.
    raise NotImplementedError(
        f"Runtime YAML step loading for '{workflow_id}' requires the "
        f"aos-client-sdk workflow loader (see docs/workflow/pr/aos-client-sdk/)."
    )


def list_registered_workflows() -> Dict[str, Dict[str, str]]:
    """Return the full workflow registry."""
    return dict(WORKFLOW_REGISTRY)


# ── Workflow YAML I/O ────────────────────────────────────────────────────────


def _resolve_yaml_path(yaml_path: str) -> Path:
    """Resolve a registry ``yaml_path`` to an absolute filesystem path.

    The package lives at ``src/business_infinity/`` and the YAML files
    are stored under ``docs/workflow/samples/`` at the project root.
    This resolves the relative path from the registry against the project
    root (three levels up from this file).
    """
    return Path(__file__).parent.parent.parent / yaml_path


def _validate_workflow_data(data: Dict[str, Any]) -> None:
    """Validate a workflow data dict before saving.

    Raises :class:`ValueError` for any structural violation so the caller
    can return a clear error to the frontend without writing a corrupt file.
    """
    if "workflow_id" not in data:
        raise ValueError("workflow data must contain 'workflow_id'")
    if "steps" not in data or not isinstance(data["steps"], dict):
        raise ValueError("workflow data must contain a 'steps' dict")
    steps: Dict[str, Any] = data["steps"]
    for step_id, step in steps.items():
        if not isinstance(step, dict):
            raise ValueError(f"Step '{step_id}' must be a mapping")
        if "narrative" not in step:
            raise ValueError(f"Step '{step_id}' missing required field 'narrative'")
        if "response" not in step:
            raise ValueError(f"Step '{step_id}' missing required field 'response'")
        if "actions" not in step or not isinstance(step["actions"], list):
            raise ValueError(f"Step '{step_id}' missing required 'actions' list")
        # Validate each action entry
        for i, action in enumerate(step["actions"]):
            if not isinstance(action, dict):
                raise ValueError(f"Step '{step_id}' action[{i}] must be a mapping")
            for field in ("label", "description", "url"):
                if field not in action:
                    raise ValueError(
                        f"Step '{step_id}' action[{i}] missing required field '{field}'"
                    )


def load_workflow_yaml(workflow_id: str) -> Dict[str, Any]:
    """Load and parse the YAML file for a registered workflow.

    Returns the full structured workflow data including all steps, suitable
    for serialising to JSON and sending to the workflow editor frontend.

    Raises :class:`KeyError` if *workflow_id* is not registered.
    Raises :class:`FileNotFoundError` if the YAML file does not exist.
    Raises :class:`ValueError` if the YAML file is malformed.
    """
    metadata = get_workflow_metadata(workflow_id)
    yaml_path = _resolve_yaml_path(metadata["yaml_path"])
    with open(str(yaml_path), "r", encoding="utf-8") as fh:
        try:
            return yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Malformed YAML in workflow '{workflow_id}' "
                f"({metadata['yaml_path']}): {exc}"
            ) from exc


def save_workflow_yaml(workflow_id: str, data: Dict[str, Any]) -> None:
    """Validate and save an updated workflow structure to its YAML file.

    The *data* dict must match the boardroom YAML schema documented in
    ``docs/workflow/boardroom.yaml``.  Validation is applied before
    writing so the file is never overwritten with an invalid structure.

    Raises :class:`KeyError` if *workflow_id* is not registered.
    Raises :class:`ValueError` if *data* fails validation.
    Raises :class:`FileNotFoundError` if the YAML file path is unreachable.
    """
    metadata = get_workflow_metadata(workflow_id)
    _validate_workflow_data(data)
    yaml_path = _resolve_yaml_path(metadata["yaml_path"])
    with open(str(yaml_path), "w", encoding="utf-8") as fh:
        yaml.dump(data, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)


# ── Backward Compatibility ───────────────────────────────────────────────────
#
# The following constants are preserved for backward compatibility with
# existing tests and the current pitch-orchestration workflow.  New code
# should use WORKFLOW_REGISTRY and the helper functions above.

#: Purpose statement for pitch delivery through the boardroom interface.
PITCH_ORCHESTRATION_PURPOSE = WORKFLOW_REGISTRY["pitch_business_infinity"]["purpose"]

#: Scope of the pitch orchestration.
PITCH_ORCHESTRATION_SCOPE = WORKFLOW_REGISTRY["pitch_business_infinity"]["scope"]

#: Pitch step IDs in presentation order, matching ``pitch.yaml``.
_PITCH_STEP_IDS = [
    "paul_graham_intro",
    "paul_graham_dataset",
    "lora_paul_graham",
    "lora_werner_erhard",
    "founder_ai_agent",
    "boardroom_cxo",
    "business_infinity_resonance",
    "asi_saga_self_learning",
    "final_reveal",
]

PITCH_STEP_IDS = list(_PITCH_STEP_IDS)
