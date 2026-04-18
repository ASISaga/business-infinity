"""Azure Function blueprints for BusinessInfinity.

Each domain exposes its own ``func.Blueprint`` instance:

- ``boardroom_blueprint`` — workflow listing and detail endpoints
- ``seo_blueprint`` — SEO taxonomy summary and category endpoints
- ``health_blueprint`` — liveness probe
"""

from business_infinity.blueprints.boardroom_api import (
    boardroom_blueprint,
    boardroom_workflow_details,
    boardroom_workflows,
)
from business_infinity.blueprints.health import health_blueprint
from business_infinity.blueprints.seo_api import (
    seo_blueprint,
    seo_category_details,
    seo_summary,
)

__all__ = [
    "boardroom_blueprint",
    "boardroom_workflow_details",
    "boardroom_workflows",
    "health_blueprint",
    "seo_blueprint",
    "seo_category_details",
    "seo_summary",
]
