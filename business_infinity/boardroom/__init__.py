"""BusinessInfinity Boardroom — philosophy-derived constants, state, and registry.

The boardroom encodes the core philosophy of BusinessInfinity: a purpose-driven
decision tree debate where each CXO agent applies domain leadership to propose
pathways, which are evaluated through resonance scoring against the company's
purpose, and synthesised into autonomous action.
"""

from business_infinity.boardroom.constants import (
    BOARDROOM_DEBATE_PURPOSE,
    BOARDROOM_DEBATE_SCOPE,
    CXO_DOMAINS,
    CXO_PATHWAY_TYPES,
)
from business_infinity.boardroom.registry import (
    PITCH_ORCHESTRATION_PURPOSE,
    PITCH_ORCHESTRATION_SCOPE,
    PITCH_STEP_IDS,
    WORKFLOW_REGISTRY,
    WorkflowRegistryManager,
)
from business_infinity.boardroom.state import BoardroomStateManager
from business_infinity.boardroom.yaml_manager import WorkflowYAMLManager

__all__ = [
    "BOARDROOM_DEBATE_PURPOSE",
    "BOARDROOM_DEBATE_SCOPE",
    "BoardroomStateManager",
    "CXO_DOMAINS",
    "CXO_PATHWAY_TYPES",
    "PITCH_ORCHESTRATION_PURPOSE",
    "PITCH_ORCHESTRATION_SCOPE",
    "PITCH_STEP_IDS",
    "WORKFLOW_REGISTRY",
    "WorkflowRegistryManager",
    "WorkflowYAMLManager",
]
