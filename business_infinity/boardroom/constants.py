"""CXO domain leadership constants and boardroom debate parameters.

Derived from the BusinessInfinity philosophy: a purpose-driven decision tree
debate where each CXO agent applies domain leadership to propose pathways.
"""

from __future__ import annotations

from typing import Dict


# ── CXO Domain Leadership ───────────────────────────────────────────────────

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
CXO_PATHWAY_TYPES = list(
    dict.fromkeys(domain["pathway"] for domain in CXO_DOMAINS.values())
)
