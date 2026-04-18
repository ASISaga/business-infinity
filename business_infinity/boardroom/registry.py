"""Structured workflow registry — metadata and step IDs.

Each structured workflow is owned by a boardroom agent and conducts a
step-by-step conversation with an external entity.  The registry maps
workflow IDs to their metadata.
"""

from __future__ import annotations

from typing import Dict, List


#: Registry of structured boardroom workflows.
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


class WorkflowRegistryManager:
    """Manages the structured workflow registry and metadata lookups."""

    _REGISTRY: Dict[str, Dict[str, str]] = WORKFLOW_REGISTRY

    #: Pitch step IDs in presentation order, matching ``pitch.yaml``.
    PITCH_STEP_IDS: List[str] = [
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

    @classmethod
    def get_metadata(cls, workflow_id: str) -> Dict[str, str]:
        """Return metadata for a registered structured workflow.

        Raises :class:`KeyError` if the workflow ID is not registered.
        """
        return cls._REGISTRY[workflow_id]

    @classmethod
    def get_step_ids(cls, workflow_id: str) -> List[str]:
        """Return ordered step IDs for a registered structured workflow."""
        if workflow_id == "pitch_business_infinity":
            return list(cls.PITCH_STEP_IDS)
        raise NotImplementedError(
            f"Runtime YAML step loading for '{workflow_id}' requires the "
            f"aos-client-sdk workflow loader (see docs/workflow/pr/aos-client-sdk/)."
        )

    @classmethod
    def list_all(cls) -> Dict[str, Dict[str, str]]:
        """Return a copy of the full workflow registry."""
        return dict(cls._REGISTRY)


# ── Pitch Constants ──────────────────────────────────────────────────────────

#: Purpose statement for pitch delivery through the boardroom interface.
PITCH_ORCHESTRATION_PURPOSE = WORKFLOW_REGISTRY["pitch_business_infinity"]["purpose"]

#: Scope of the pitch orchestration.
PITCH_ORCHESTRATION_SCOPE = WORKFLOW_REGISTRY["pitch_business_infinity"]["scope"]

#: Pitch step IDs in presentation order.
PITCH_STEP_IDS = list(WorkflowRegistryManager.PITCH_STEP_IDS)
