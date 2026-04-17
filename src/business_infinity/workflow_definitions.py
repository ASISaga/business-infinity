"""BusinessInfinity workflow definitions — aggregator module.

Imports all dedicated workflow modules to trigger ``@aos_app.workflow``,
``@aos_app.on_orchestration_update``, and ``@aos_app.mcp_tool`` decorator
registrations with the shared ``aos_app`` instance.

Re-exports shared utilities from :mod:`business_infinity.workflow_utils` for
backward compatibility with existing imports.
"""

from __future__ import annotations

# Import all workflow modules to register their decorators with aos_app.
# These side-effect imports are required: decorators execute at import time.
from business_infinity import strategic_workflows  # noqa: F401
from business_infinity import boardroom_debate  # noqa: F401
from business_infinity import enterprise_workflows  # noqa: F401
from business_infinity import mcp_workflows  # noqa: F401
from business_infinity import pitch_workflows  # noqa: F401
from business_infinity import workflow_orchestration  # noqa: F401
from business_infinity import workflow_editor  # noqa: F401

# Backward-compatible re-exports
from business_infinity.workflow_utils import (  # noqa: F401
    CSuiteAgentSelector,
    OwnerStateLoader,
    C_SUITE_TYPES,
    C_SUITE_AGENT_IDS,
    select_c_suite_agents,
)

__all__ = [
    "CSuiteAgentSelector",
    "OwnerStateLoader",
    "C_SUITE_TYPES",
    "C_SUITE_AGENT_IDS",
    "select_c_suite_agents",
]
