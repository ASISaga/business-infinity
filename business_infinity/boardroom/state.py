"""Boardroom state management — agent state, collective state, and mind files.

The boardroom maintains two explicit layers of JSON-LD state for each agent:

  - **Context** (immutable): fixed identity, mandate, and constraints — the
    agent's read-only constitution.
  - **Content** (mutable): active focus, strategy, short-term memory, and
    spontaneous intent — the agent's writable working space.

Collective boardroom state (topic, resonance scores, active directives) is
stored separately in ``boardroom.jsonld``.

Agent Manas (memory) files live in ``boardroom/mind/{agent_id}/Manas/``.
Agent Buddhi (intellect) files live in ``boardroom/mind/{agent_id}/Buddhi/``.
Agent Ahankara (identity) files live in ``boardroom/mind/{agent_id}/Ahankara/``.
Agent Chitta (pure intelligence) files live in ``boardroom/mind/{agent_id}/Chitta/``.
Shared collective state files live in ``boardroom/mind/collective/``.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Set

from business_infinity._paths import PROJECT_ROOT


class BoardroomStateManager:
    """Manages segregated boardroom state documents.

    Agent state is stored with two explicit layers:

    - ``context``: static, read-only identity and mandate information.
    - ``content``: dynamic, writable working memory and active intent.

    Each layer also carries its own management metadata so read-only context is
    never updated through the same path as mutable content.
    """

    #: Path to the ``boardroom/mind/collective/`` directory (shared state).
    _STATE_DIR: Path = PROJECT_ROOT / "boardroom" / "mind" / "collective"

    #: Path to the ``boardroom/mind/`` directory relative to the project root.
    _MIND_DIR: Path = PROJECT_ROOT / "boardroom" / "mind"

    #: Mapping from agent ID to state filename stem (without extension).
    #: All agent state files use the ``.jsonld`` extension.
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

    #: Required keys for an agent's immutable static context.
    _AGENT_CONTEXT_KEYS = {
        "name",
        "fixed_mandate",
        "core_logic",
        "immutable_constraints",
    }

    #: Required keys for an agent's mutable working content.
    _AGENT_CONTENT_KEYS = {
        "current_focus",
        "active_strategy",
        "short_term_memory",
        "spontaneous_intent",
        "company_state",
        "product_state",
    }

    #: Required keys for each company/product perspective projection.
    _AGENT_PERSPECTIVE_KEYS = {
        "entity_id",
        "entity_name",
        "perspective",
        "domain_knowledge",
        "skills",
        "persona",
        "language",
        "software_interfaces",
        "current_signals",
    }

    #: Management metadata required for each segregated state layer.
    _AGENT_LAYER_MANAGEMENT_KEYS = {
        "access",
        "mutability",
        "manager",
    }

    #: Core Business Infinity manifest records: product, architecture, UI,
    #: persistence, and orchestration logic.
    _PRODUCT_MANIFEST_RECORD_IDS = {
        "bi:product:core",
        "bi:arch:modular",
        "bi:engine:bento",
        "bi:layer:subconscious",
        "bi:logic:resonance",
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
        "company.jsonld": {
            "mode": "object",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "name",
                "vision",
                "transcendentPathway",
                "governance",
                "portfolio",
            },
        },
        "business-infinity.jsonld": {
            "mode": "jsonld_graph",
            "required_keys": {"@context", "@id", "@type"},
            "required_record_ids": _PRODUCT_MANIFEST_RECORD_IDS,
        },
        "environment.jsonld": {
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
        "mvp.jsonld": {
            "mode": "jsonld_graph",
            "required_keys": {"@context", "@id", "@type"},
        },
    }

    # ── Mind File Schemas ────────────────────────────────────────────────────
    _MIND_FILE_SCHEMAS: Dict[str, Dict[str, Any]] = {
        "Manas/state": {
            "description": "Agent memory state — context and content layers",
            "schema_file": "manas.schema.json",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "schema_version",
                "context",
                "context_management",
                "content",
                "content_management",
            },
        },
        "Buddhi/buddhi.jsonld": {
            "description": "Agent intellect — legend-derived domain wisdom",
            "schema_file": "buddhi.schema.json",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "schema_version",
                "agent_id",
                "name",
                "domain",
                "domain_knowledge",
                "skills",
                "persona",
                "language",
            },
        },
        "Buddhi/action-plan.jsonld": {
            "description": "Agent action plan — steps toward the initial company purpose",
            "schema_file": "action-plan.schema.json",
            "required_keys": {
                "@context",
                "@type",
                "name",
                "role",
                "anchor",
                "status",
                "overarchingPurpose",
                "actionSteps",
            },
        },
        "Ahankara/ahankara.jsonld": {
            "description": "Agent identity — the ego that constrains the intellect",
            "schema_file": "ahankara.schema.json",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "schema_version",
                "agent_id",
                "name",
                "identity",
                "contextual_axis",
                "non_negotiables",
                "identity_markers",
                "intellect_constraint",
            },
        },
        "Chitta/chitta.jsonld": {
            "description": "Pure intelligence — mind without memory, cosmic substrate",
            "schema_file": "chitta.schema.json",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "schema_version",
                "agent_id",
                "name",
                "intelligence_nature",
                "cosmic_intelligence",
                "beyond_identity",
                "consciousness_basis",
            },
        },
        "Manas/context/entity": {
            "description": "Immutable entity perspective (context layer)",
            "schema_file": "entity-context.schema.json",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "name",
                "agent_perspective",
                "legend",
                "domain_knowledge",
                "skills",
                "persona",
                "language",
            },
        },
        "Manas/content/entity": {
            "description": "Mutable entity perspective (content layer)",
            "schema_file": "entity-content.schema.json",
            "required_keys": {
                "@context",
                "@id",
                "@type",
                "name",
                "agent_perspective",
                "legend",
                "perspective",
                "software_interfaces",
                "current_signals",
            },
        },
    }

    #: Path to the ``boardroom/mind/schemas/`` directory.
    _SCHEMAS_DIR: Path = PROJECT_ROOT / "boardroom" / "mind" / "schemas"

    @classmethod
    def _state_path(cls, filename: str) -> Path:
        """Resolve an agent state filename stem to its absolute path."""
        path = cls._MIND_DIR / filename / "Manas" / (filename + ".jsonld")
        if path.exists():
            return path
        raise FileNotFoundError(
            f"State file '{filename}' not found at "
            f"{cls._MIND_DIR / filename / 'Manas'}/{filename}.jsonld"
        )

    @classmethod
    def _read_text(cls, path: Path) -> str:
        """Read a state document from disk."""
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read().strip()

    @classmethod
    def _load_json_document(cls, path: Path) -> Dict[str, Any]:
        """Load a single JSON document from *path*."""
        content = cls._read_text(path)
        first_line = content.partition("\n")[0].strip()
        try:
            return json.loads(first_line)
        except json.JSONDecodeError:
            try:
                return json.loads(content)
            except json.JSONDecodeError as full_error:
                raise ValueError(
                    f"Unable to parse JSON document at {path}: "
                    "single-line and full-content parsing both failed"
                ) from full_error

    @classmethod
    def _load_graph_records(cls, path: Path) -> List[Dict[str, Any]]:
        """Load JSON-LD ``@graph`` records from a ``.jsonld`` document."""
        document = cls._load_json_document(path)
        if "@graph" not in document:
            raise ValueError(
                f"JSON-LD document at {path} has no '@graph' key"
            )
        return list(document["@graph"])

    @classmethod
    def _write_json_document(cls, path: Path, data: Dict[str, Any]) -> None:
        """Write a single JSON-LD document to *path*."""
        with open(path, "w", encoding="utf-8") as fh:
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
        required_keys: Set[str],
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
            state["content"]["company_state"],
            cls._AGENT_PERSPECTIVE_KEYS,
            "agent company_state",
        )
        cls._validate_required_keys(
            state["content"]["product_state"],
            cls._AGENT_PERSPECTIVE_KEYS,
            "agent product_state",
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

        state["innate_essence"] = deepcopy(state["context"])
        state["executive_function"] = deepcopy(state["content"])
        return state

    @classmethod
    def _validate_document_schema(cls, filename: str, data: Any) -> None:
        """Validate a non-agent state document against its lightweight schema."""
        schema = cls._DOCUMENT_SCHEMAS[filename]
        if schema["mode"] == "object":
            cls._validate_required_keys(data, schema["required_keys"], filename)
            return

        if not isinstance(data, list):
            raise ValueError(f"{filename} must contain a list of @graph records")
        for index, record in enumerate(data):
            cls._validate_required_keys(
                record,
                schema["required_keys"],
                f"{filename}[{index}]",
            )
        if "required_record_ids" in schema:
            actual_ids = {record.get("@id") for record in data}
            missing_ids = schema["required_record_ids"] - actual_ids
            if missing_ids:
                raise ValueError(
                    f"{filename} missing required record ids: {sorted(missing_ids)}"
                )

    @classmethod
    def load_agent_state(cls, agent_id: str) -> Dict[str, Any]:
        """Load the full segregated state for an agent."""
        try:
            filename = cls._AGENT_FILES[agent_id]
        except KeyError as exc:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            ) from exc
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
    def load_agent_company_state(cls, agent_id: str) -> Dict[str, Any]:
        """Load an agent's company-state perspective."""
        return dict(cls.load_agent_content(agent_id)["company_state"])

    @classmethod
    def load_agent_product_state(cls, agent_id: str) -> Dict[str, Any]:
        """Load an agent's product-state perspective."""
        return dict(cls.load_agent_content(agent_id)["product_state"])

    @classmethod
    def load_agent_buddhi(cls, agent_id: str) -> Dict[str, Any]:
        """Load the intellect (Buddhi) for an agent."""
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / "Buddhi" / "buddhi.jsonld"
        return cls._load_json_document(path)

    @classmethod
    def load_agent_ahankara(cls, agent_id: str) -> Dict[str, Any]:
        """Load the identity (Ahankara) for an agent."""
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / "Ahankara" / "ahankara.jsonld"
        return cls._load_json_document(path)

    @classmethod
    def load_agent_chitta(cls, agent_id: str) -> Dict[str, Any]:
        """Load the pure intelligence (Chitta) for an agent."""
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / "Chitta" / "chitta.jsonld"
        return cls._load_json_document(path)

    @classmethod
    def _resolve_mind_schema_key(cls, dimension: str, filename: str) -> str:
        """Return the ``_MIND_FILE_SCHEMAS`` key for a given dimension/filename pair."""
        if dimension == "Manas" and filename.endswith(".jsonld") and "/" not in filename:
            return "Manas/state"
        if dimension in ("Manas/context", "Manas/content"):
            layer = "context" if dimension.endswith("context") else "content"
            return f"Manas/{layer}/entity"
        return f"{dimension}/{filename}"

    @classmethod
    def _validate_mind_file(
        cls, key: str, data: Dict[str, Any], label: str
    ) -> None:
        """Validate a mind file document against its registered schema."""
        schema = cls._MIND_FILE_SCHEMAS.get(key)
        if schema is None:
            return
        cls._validate_required_keys(data, schema["required_keys"], label)

    @classmethod
    def load_mind_file(
        cls,
        agent_id: str,
        dimension: str,
        filename: str,
    ) -> Dict[str, Any]:
        """Load and schema-validate a single mind file for an agent."""
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / dimension / filename
        document = cls._load_json_document(path)
        schema_key = cls._resolve_mind_schema_key(dimension, filename)
        cls._validate_mind_file(
            schema_key, document, f"{agent_id}/{dimension}/{filename}"
        )
        return document

    @classmethod
    def load_agent_mind(cls, agent_id: str) -> Dict[str, Dict[str, Any]]:
        """Load all four mind dimensions for an agent."""
        return {
            "Manas": cls.load_agent_state(agent_id),
            "Buddhi": cls.load_agent_buddhi(agent_id),
            "Ahankara": cls.load_agent_ahankara(agent_id),
            "Chitta": cls.load_agent_chitta(agent_id),
        }

    @classmethod
    def get_schemas_dir(cls) -> Path:
        """Return the directory containing mind file JSON schema definitions."""
        return cls._SCHEMAS_DIR

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
    def get_boardroom_state_or_default(
        cls, default: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Return boardroom state or *default* when the state file is absent."""
        try:
            return cls.get_boardroom_state()
        except FileNotFoundError:
            return {} if default is None else dict(default)

    @classmethod
    def get_state_dir(cls) -> Path:
        """Return the directory containing boardroom state files."""
        return cls._STATE_DIR

    @classmethod
    def get_mind_dir(cls) -> Path:
        """Return the directory containing agent mind structures."""
        return cls._MIND_DIR

    @classmethod
    def load_state_records(cls, filename: str) -> Any:
        """Load and validate a non-agent state document by filename."""
        path = cls._STATE_DIR / filename
        schema = cls._DOCUMENT_SCHEMAS[filename]
        if schema["mode"] == "jsonld_graph":
            records = cls._load_graph_records(path)
            cls._validate_document_schema(filename, records)
            return records
        document = cls._load_json_document(path)
        cls._validate_document_schema(filename, document)
        return document

    @classmethod
    def load_company_manifest(cls) -> Dict[str, Any]:
        """Load the canonical ASI Saga company manifest."""
        return cls.load_state_records("company.jsonld")

    @classmethod
    def load_product_manifest(cls) -> List[Dict[str, Any]]:
        """Load the canonical Business Infinity product manifest."""
        return cls.load_state_records("business-infinity.jsonld")

    @classmethod
    def update_boardroom_state(cls, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update the collective boardroom state."""
        _allowed_keys = (
            cls._DOCUMENT_SCHEMAS["boardroom.jsonld"]["required_keys"]
            - {"@context", "@id", "@type"}
        )
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
        """Return state for all agents that have state files."""
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

    @classmethod
    def get_all_agent_company_states(cls) -> Dict[str, Dict[str, Any]]:
        """Return company-state perspectives for all agents."""
        return {
            agent_id: state["content"]["company_state"]
            for agent_id, state in cls.get_all_agent_states().items()
        }

    @classmethod
    def get_all_agent_product_states(cls) -> Dict[str, Dict[str, Any]]:
        """Return product-state perspectives for all agents."""
        return {
            agent_id: state["content"]["product_state"]
            for agent_id, state in cls.get_all_agent_states().items()
        }

    @classmethod
    def get_registered_agent_ids(cls) -> List[str]:
        """Return the agent IDs managed by the boardroom state registry."""
        return list(cls._AGENT_FILES.keys())
