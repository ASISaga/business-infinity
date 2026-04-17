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
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Set

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
# Agent Manas (memory) files live in ``boardroom/mind/{agent_id}/Manas/``.
# Agent Buddhi (intellect) files live in ``boardroom/mind/{agent_id}/Buddhi/``.
# Agent Ahankara (identity) files live in ``boardroom/mind/{agent_id}/Ahankara/``.
# Agent Chitta (pure intelligence) files live in ``boardroom/mind/{agent_id}/Chitta/``.
# Shared collective state files live in ``boardroom/mind/collective/``.


class BoardroomStateManager:
    """Manages segregated boardroom state documents.

    Agent state is stored with two explicit layers:

    - ``context``: static, read-only identity and mandate information.
    - ``content``: dynamic, writable working memory and active intent.

    Each layer also carries its own management metadata so read-only context is
    never updated through the same path as mutable content.
    """

    #: Path to the ``boardroom/mind/collective/`` directory (shared state).
    _STATE_DIR: Path = Path(__file__).parent.parent.parent / "boardroom" / "mind" / "collective"

    #: Path to the ``boardroom/mind/`` directory relative to the project root.
    _MIND_DIR: Path = Path(__file__).parent.parent.parent / "boardroom" / "mind"

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
    # Each entry maps a (dimension, filename) key to the required keys that
    # BoardroomStateManager validates when loading that mind file.  The
    # authoritative JSON Schema files live in boardroom/mind/schemas/.
    #
    # Key format: "{Dimension}/{filename}"  e.g. "Buddhi/buddhi.jsonld"
    # Special key "Manas/{agent_id}.jsonld" is represented as "Manas/state"
    # because the filename varies per agent.
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
    _SCHEMAS_DIR: Path = (
        Path(__file__).parent.parent.parent / "boardroom" / "mind" / "schemas"
    )

    @classmethod
    def _state_path(cls, filename: str) -> Path:
        """Resolve an agent state filename stem to its absolute path.

        Looks in ``boardroom/mind/{filename}/Manas/{filename}.jsonld``.

        Raises :class:`FileNotFoundError` if the file does not exist.
        """
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
        """Load JSON-LD ``@graph`` records from a ``.jsonld`` document.

        Parses the document and extracts the ``@graph`` array.  Raises
        :class:`ValueError` if the document does not contain ``@graph``.
        """
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

        # "jsonld_graph" mode: data is a list extracted from a JSON-LD @graph document
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
        """Load the full segregated state for an agent.

        Returns ``context`` and ``content`` plus compatibility aliases
        ``innate_essence`` and ``executive_function``.
        """
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
        """Load the intellect (Buddhi) for an agent from its Buddhi directory.

        Returns the JSON-LD Buddhi document from
        ``boardroom/mind/{agent_id}/Buddhi/buddhi.jsonld``.

        Raises :class:`ValueError` for unknown agents.
        Raises :class:`FileNotFoundError` if the Buddhi file is absent.
        """
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / "Buddhi" / "buddhi.jsonld"
        return cls._load_json_document(path)

    @classmethod
    def load_agent_ahankara(cls, agent_id: str) -> Dict[str, Any]:
        """Load the identity (Ahankara) for an agent from its Ahankara directory.

        Ahankara is the ego/identity dimension of the mind — the sense of self
        that gives the intellect its contextual axis.  The intellect (Buddhi)
        can only function along the axis defined by Ahankara.

        Returns the JSON-LD Ahankara document from
        ``boardroom/mind/{agent_id}/Ahankara/ahankara.jsonld``.

        Raises :class:`ValueError` for unknown agents.
        Raises :class:`FileNotFoundError` if the Ahankara file is absent.
        """
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / "Ahankara" / "ahankara.jsonld"
        return cls._load_json_document(path)

    @classmethod
    def load_agent_chitta(cls, agent_id: str) -> Dict[str, Any]:
        """Load the pure intelligence (Chitta) for an agent from its Chitta directory.

        Chitta is mind without memory — pure cosmic intelligence.  It connects
        the agent to the basis of creation and transcends both identity (Ahankara)
        and the memory-bound intellect (Buddhi).

        Returns the JSON-LD Chitta document from
        ``boardroom/mind/{agent_id}/Chitta/chitta.jsonld``.

        Raises :class:`ValueError` for unknown agents.
        Raises :class:`FileNotFoundError` if the Chitta file is absent.
        """
        if agent_id not in cls._AGENT_FILES:
            raise ValueError(
                f"Unknown agent ID '{agent_id}'. "
                f"Registered agents: {cls.get_registered_agent_ids()}"
            )
        path = cls._MIND_DIR / agent_id / "Chitta" / "chitta.jsonld"
        return cls._load_json_document(path)

    @classmethod
    def _resolve_mind_schema_key(cls, dimension: str, filename: str) -> str:
        """Return the ``_MIND_FILE_SCHEMAS`` key for a given dimension/filename pair.

        Special cases:
        - ``Manas`` + ``{agent_id}.jsonld`` → ``"Manas/state"``
        - ``Manas/context`` + any ``.jsonld`` → ``"Manas/context/entity"``
        - ``Manas/content`` + any ``.jsonld`` → ``"Manas/content/entity"``
        - Other dimensions use ``"{dimension}/{filename}"`` directly.
        """
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
        """Validate a mind file document against its registered schema.

        Uses the lightweight required-key validation consistent with
        :meth:`_validate_required_keys`.  The schema key must be present in
        :attr:`_MIND_FILE_SCHEMAS`.
        """
        schema = cls._MIND_FILE_SCHEMAS.get(key)
        if schema is None:
            return  # No schema registered — skip validation
        cls._validate_required_keys(data, schema["required_keys"], label)

    @classmethod
    def load_mind_file(
        cls,
        agent_id: str,
        dimension: str,
        filename: str,
    ) -> Dict[str, Any]:
        """Load and schema-validate a single mind file for an agent.

        This is the generic schema-based file loader for the purpose-driven
        agent mind.  Given an agent ID, a dimension name (``Buddhi``,
        ``Ahankara``, ``Chitta``, ``Manas``, ``Manas/context``,
        ``Manas/content``), and a filename, it:

        1. Resolves the absolute path under ``boardroom/mind/{agent_id}/``.
        2. Loads the JSON-LD document.
        3. Validates it against the registered schema (required keys).
        4. Returns the validated document.

        **Supported dimension/filename combinations:**

        =============================  ===============================
        dimension                      filename
        =============================  ===============================
        ``Buddhi``                     ``buddhi.jsonld``
        ``Buddhi``                     ``action-plan.jsonld``
        ``Ahankara``                   ``ahankara.jsonld``
        ``Chitta``                     ``chitta.jsonld``
        ``Manas``                      ``{agent_id}.jsonld``
        ``Manas/context``              ``company.jsonld``
        ``Manas/context``              ``business-infinity.jsonld``
        ``Manas/content``              ``company.jsonld``
        ``Manas/content``              ``business-infinity.jsonld``
        =============================  ===============================

        Raises :class:`ValueError` for unknown agents.
        Raises :class:`FileNotFoundError` if the file is absent.
        Raises :class:`ValueError` if required schema keys are missing.
        """
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
        """Load all four mind dimensions for an agent.

        Returns a dict with keys ``"Manas"``, ``"Buddhi"``, ``"Ahankara"``,
        and ``"Chitta"``, each containing the loaded and schema-validated
        document for that dimension.

        The Buddhi entry is the ``buddhi.jsonld`` document; the Manas entry is
        the agent state document (``{agent_id}.jsonld``).  Each is validated
        against its registered schema.

        Raises :class:`ValueError` for unknown agents.
        Raises :class:`FileNotFoundError` if any dimension file is absent.
        """
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
        """Update the collective boardroom state.

        Permitted top-level update keys: ``status``, ``current_topic``,
        ``resonance_ledger``, ``active_directives``.  JSON-LD metadata keys
        (``@context``, ``@id``, ``@type``) are passed through unchanged.

        Returns the full updated boardroom state.

        Raises :class:`ValueError` for unrecognised keys.
        """
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
    "founder_sovereignty": {
        "owner": "ceo",
        "purpose": (
            "Consult a burnt-out founder or scaling CEO on reclaiming strategic "
            "sovereignty by offloading the Complexity Tax to a perpetual boardroom "
            "of legendary CXO agents, restoring 20+ hours per week of focused "
            "leadership time."
        ),
        "scope": (
            "Founder sovereignty consultation: complexity tax diagnosis, "
            "strategy-execution gap identification, legendary CXO offloading, "
            "resonance governance introduction, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/founder-sovereignty.yaml",
    },
    "knowledge_continuity": {
        "owner": "chro",
        "purpose": (
            "Help a company facing key-person fragility and institutional amnesia "
            "preserve its strategic DNA permanently through the boardroom's "
            "four-dimensional agent mind, ensuring critical wisdom survives "
            "any departure."
        ),
        "scope": (
            "Knowledge continuity consultation: veteran departure risk diagnosis, "
            "reinvention tax quantification, wisdom-vs-documentation gap framing, "
            "perpetual agent memory introduction, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/knowledge-continuity.yaml",
    },
    "resilience_consultation": {
        "owner": "cso",
        "purpose": (
            "Guide a company exposed to supply-chain chaos or geopolitical "
            "disruption through the Business Infinity resilience model: spontaneous "
            "boardroom war room, cross-domain convergence, and antifragility by "
            "design."
        ),
        "scope": (
            "Resilience consultation: cascade failure diagnosis, response gap "
            "analysis, spontaneous war room demonstration, cross-domain convergence "
            "walkthrough, antifragility framing, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/resilience-consultation.yaml",
    },
    "data_synthesis": {
        "owner": "cmo",
        "purpose": (
            "Help a data-rich but insight-poor CEO replace disconnected dashboards "
            "with a unified boardroom synthesis layer that reads across all connected "
            "systems and surfaces the decisions that matter most."
        ),
        "scope": (
            "Data synthesis consultation: dashboard trap diagnosis, inter-silo "
            "silence framing, synthesis gap analysis, cross-system truth "
            "demonstration, legend-as-synthesizer walkthrough, and onboarding "
            "call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/data-synthesis.yaml",
    },
    "complexity_governance": {
        "owner": "coo",
        "purpose": (
            "Help a scaling company overwhelmed by organizational entropy replace "
            "committee-driven governance with purpose-driven coordination intelligence, "
            "eliminating the alignment meetings and coordination overhead that consume "
            "40% of headcount at scale."
        ),
        "scope": (
            "Complexity governance consultation: hiring paradox diagnosis, entropy "
            "tax quantification, coordination overhead analysis, unified consciousness "
            "introduction, purpose-as-constitution framing, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/complexity-governance.yaml",
    },
    "strategy_execution": {
        "owner": "ceo",
        "purpose": (
            "Close the strategy-execution divorce for companies where board-approved "
            "strategy diverges from daily execution, using spec-driven governance and "
            "real-time integrity gap detection across all connected systems."
        ),
        "scope": (
            "Strategy-execution consultation: boardroom fiction diagnosis, shadow "
            "project exposure, promise gap analysis, spec-driven governance "
            "introduction, integrity gap detection walkthrough, and onboarding "
            "call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/strategy-execution.yaml",
    },
    "culture_integrity": {
        "owner": "chro",
        "purpose": (
            "Help a rapidly growing company preserve its founding culture at scale "
            "by activating the Drucker agent as a cultural guardian that monitors "
            "engagement integrity and enforces people-centric governance through "
            "purpose resonance."
        ),
        "scope": (
            "Culture integrity consultation: soul-fade diagnosis, bozo explosion "
            "framing, quiet quitting detection, Drucker agent introduction, "
            "culture-at-scale governance, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/culture-integrity.yaml",
    },
    "ai_governance": {
        "owner": "cto",
        "purpose": (
            "Help a CEO facing AI sprawl and agentic risk bring all autonomous "
            "agents under unified governance through AOS, with resonance-based "
            "scoring, explainable decision trails, and full audit compliance."
        ),
        "scope": (
            "AI governance consultation: sprawl diagnosis, black box exposure, "
            "accountability framing, resonance governance introduction, AOS "
            "architecture walkthrough, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/ai-governance.yaml",
    },
    "exit_readiness": {
        "owner": "cfo",
        "purpose": (
            "Help a founder facing exit or due-diligence anxiety achieve permanent "
            "audit readiness through the boardroom's versioned decision trail, "
            "institutional memory, and instant compliance reporting."
        ),
        "scope": (
            "Exit readiness consultation: due-diligence anxiety diagnosis, house-of-cards "
            "exposure, valuation discount framing, permanent audit readiness "
            "introduction, instant answer demonstration, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/exit-readiness.yaml",
    },
    "innovation_velocity": {
        "owner": "cto",
        "purpose": (
            "Help a company trapped in the innovation-vs-maintenance deadlock restore "
            "engineering velocity by eliminating the Maintenance Tax, the Reinvention "
            "Tax, and cross-domain context blindness through spec-driven development."
        ),
        "scope": (
            "Innovation velocity consultation: velocity paradox diagnosis, maintenance "
            "tax quantification, reinvention wheel exposure, spec-driven prevention "
            "introduction, innovation guard walkthrough, and onboarding call-to-action."
        ),
        "yaml_path": "docs/workflow/samples/innovation-velocity.yaml",
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
