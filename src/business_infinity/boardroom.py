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

from typing import Any, Dict, List

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
    """
    if workflow_id == "pitch_business_infinity":
        return list(_PITCH_STEP_IDS)
    # For other workflows, step IDs are resolved at runtime from YAML
    # by the aos-client-sdk YAML loader.  This function returns an empty
    # list as a placeholder until the SDK provides the loader.
    return []


def list_registered_workflows() -> Dict[str, Dict[str, str]]:
    """Return the full workflow registry."""
    return dict(WORKFLOW_REGISTRY)


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
