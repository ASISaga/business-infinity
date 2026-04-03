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
# The boardroom maintains two explicit layers of JSON-LD state for each agent:
#
#   - **Context** (immutable): fixed identity, mandate, and constraints — the
#     agent's read-only constitution.
#   - **Content** (mutable): active focus, strategy, short-term memory, and
#     spontaneous intent — the agent's writable working space.
#
# Collective boardroom state (topic, resonance scores, active directives) is
# stored separately in ``boardroom.jsonld``.
#
# All state files live in ``boardroom/state/`` at the project root.


class BoardroomStateManager:
    """Manages segregated boardroom state documents.

    Agent state is stored with two explicit layers:

    - ``context``: static, read-only identity and mandate information.
    - ``content``: dynamic, writable working memory and active intent.

    Each layer also carries its own management metadata so read-only context is
    never updated through the same path as mutable content.
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

    _AGENT_CONTEXT_KEYS = {
        "name",
        "fixed_mandate",
        "core_logic",
        "immutable_constraints",
    }

    _AGENT_CONTENT_KEYS = {
        "current_focus",
        "active_strategy",
        "short_term_memory",
        "spontaneous_intent",
    }

    _AGENT_LAYER_MANAGEMENT_KEYS = {
        "access",
        "mutability",
        "manager",
    }

    _DOCUMENT_SCHEMAS: Dict[str, Dict[str, Any]] = {
        "boardroom.jsonld": {
            "mode": "object",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "status",
                "current_topic",
                "resonance_ledger",
                "active_directives",
            },
        },
        "environment.jsonl": {
            "mode": "object",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "cloud_provider",
                "gitops_registry",
                "compliance_gate",
            },
        },
        "mvp.jsonl": {
            "mode": "jsonl",
            "required_keys": {"@context", "@id", "@type"},
        },
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
    def _read_text(cls, path: Path) -> str:
        """Read a state document from disk."""
        with open(str(path), "r", encoding="utf-8") as fh:
            return fh.read().strip()

    @classmethod
    def _load_json_document(cls, path: Path) -> Dict[str, Any]:
        """Load a single JSON document from *path*."""
        content = cls._read_text(path)
        first_line = content.split("\n")[0].strip()
        try:
            return json.loads(first_line)
        except json.JSONDecodeError:
            return json.loads(content)

    @classmethod
    def _load_jsonl_records(cls, path: Path) -> List[Dict[str, Any]]:
        """Load one-or-more JSON records from *path*."""
        content = cls._read_text(path)
        if not content:
            return []
        records: List[Dict[str, Any]] = []
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
        return records

    @classmethod
    def _write_json_document(cls, path: Path, data: Dict[str, Any]) -> None:
        """Write a single JSON document while preserving compact jsonl files."""
        with open(str(path), "w", encoding="utf-8") as fh:
            if path.suffix == ".jsonl":
                fh.write(json.dumps(data, ensure_ascii=False))
                fh.write("\n")
            else:
                json.dump(data, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    @classmethod
    def _default_context_management(cls) -> Dict[str, Any]:
        """Return the default management metadata for agent context."""
        return {
            "access": "read-only",
            "mutability": "immutable",
            "manager": "BoardroomStateManager.load_agent_context",
        }

    @classmethod
    def _default_content_management(cls) -> Dict[str, Any]:
        """Return the default management metadata for agent content."""
        return {
            "access": "full-control",
            "mutability": "mutable",
            "manager": "BoardroomStateManager.update_agent_content",
        }

    @classmethod
    def _validate_required_keys(
        cls,
        data: Dict[str, Any],
        required_keys: set[str],
        label: str,
    ) -> None:
        """Validate that *data* contains all *required_keys*."""
        missing = required_keys - set(data.keys())
        if missing:
            raise ValueError(f"{label} missing required keys: {sorted(missing)}")

    @classmethod
    def _normalize_agent_state(cls, state: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize legacy agent state into segregated context/content shape."""
        if "context" not in state and "innate_essence" in state:
            state["context"] = state.pop("innate_essence")
        if "content" not in state and "executive_function" in state:
            state["content"] = state.pop("executive_function")

        state.setdefault("schema_version", "2.0.0")
        state.setdefault("context_management", cls._default_context_management())
        state.setdefault("content_management", cls._default_content_management())

        cls._validate_required_keys(
            state,
            {
                "@context",
                "@id",
                "@type",
                "schema_version",
                "context",
                "context_management",
                "content",
                "content_management",
            },
            "agent state",
        )
        cls._validate_required_keys(
            state["context"],
            cls._AGENT_CONTEXT_KEYS,
            "agent context",
        )
        cls._validate_required_keys(
            state["content"],
            cls._AGENT_CONTENT_KEYS,
            "agent content",
        )
        cls._validate_required_keys(
            state["context_management"],
            cls._AGENT_LAYER_MANAGEMENT_KEYS,
            "context management",
        )
        cls._validate_required_keys(
            state["content_management"],
            cls._AGENT_LAYER_MANAGEMENT_KEYS,
            "content management",
        )

        state["innate_essence"] = dict(state["context"])
        state["executive_function"] = dict(state["content"])
        return state

    @classmethod
    def _validate_document_schema(cls, filename: str, data: Any) -> None:
        """Validate a non-agent state document against its lightweight schema."""
        schema = cls._DOCUMENT_SCHEMAS[filename]
        if schema["mode"] == "object":
            cls._validate_required_keys(data, schema["required_keys"], filename)
            return

        if not isinstance(data, list):
            raise ValueError(f"{filename} must contain a JSONL record list")
        for index, record in enumerate(data):
            cls._validate_required_keys(
                record,
                schema["required_keys"],
                f"{filename}[{index}]",
            )

    @classmethod
    def load_agent_state(cls, agent_id: str) -> Dict[str, Any]:
        """Load the full segregated state for an agent.

        Returns ``context`` and ``content`` plus compatibility aliases
        ``innate_essence`` and ``executive_function``.
        """
        filename = cls._AGENT_FILES[agent_id]
        path = cls._state_path(filename)
        return cls._normalize_agent_state(cls._load_json_document(path))

    @classmethod
    def load_agent_context(cls, agent_id: str) -> Dict[str, Any]:
        """Load static, read-only context for an agent."""
        return dict(cls.load_agent_state(agent_id)["context"])

    @classmethod
    def load_agent_content(cls, agent_id: str) -> Dict[str, Any]:
        """Load dynamic, mutable content for an agent."""
        return dict(cls.load_agent_state(agent_id)["content"])

    @classmethod
    def update_agent_content(
        cls, agent_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the mutable ``content`` section of an agent's state."""
        state = cls.load_agent_state(agent_id)
        filename = cls._AGENT_FILES[agent_id]
        path = cls._state_path(filename)

        content = state.get("content", {})
        content.update(updates)
        state["content"] = content
        state["executive_function"] = dict(content)

        persisted = {
            key: value
            for key, value in state.items()
            if key not in {"innate_essence", "executive_function"}
        }
        cls._write_json_document(path, persisted)
        return state

    @classmethod
    def update_agent_context(
        cls, agent_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Reject direct updates to agent context."""
        raise PermissionError(
            f"Agent context is read-only for '{agent_id}'; "
            "use content updates instead"
        )

    @classmethod
    def update_executive_function(
        cls, agent_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Backward-compatible alias for :meth:`update_agent_content`."""
        return cls.update_agent_content(agent_id, updates)

    @classmethod
    def get_boardroom_state(cls) -> Dict[str, Any]:
        """Return the current collective boardroom state from ``boardroom.jsonld``."""
        path = cls._STATE_DIR / "boardroom.jsonld"
        state = cls._load_json_document(path)
        cls._validate_document_schema("boardroom.jsonld", state)
        return state

    @classmethod
    def load_state_records(cls, filename: str) -> Any:
        """Load and validate a non-agent state document by filename."""
        path = cls._STATE_DIR / filename
        schema = cls._DOCUMENT_SCHEMAS[filename]
        if schema["mode"] == "jsonl":
            records = cls._load_jsonl_records(path)
            cls._validate_document_schema(filename, records)
            return records
        document = cls._load_json_document(path)
        cls._validate_document_schema(filename, document)
        return document

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
        cls._write_json_document(path, state)

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

    @classmethod
    def get_all_agent_contexts(cls) -> Dict[str, Dict[str, Any]]:
        """Return static context for all agents that have state files."""
        return {
            agent_id: state["context"]
            for agent_id, state in cls.get_all_agent_states().items()
        }

    @classmethod
    def get_all_agent_contents(cls) -> Dict[str, Dict[str, Any]]:
        """Return dynamic content for all agents that have state files."""
        return {
            agent_id: state["content"]
            for agent_id, state in cls.get_all_agent_states().items()
        }


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
