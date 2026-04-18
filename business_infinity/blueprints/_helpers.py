"""Shared helpers for Azure Function blueprint endpoints."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional, Tuple

import azure.functions as func


def json_response(payload: Dict[str, Any], status_code: int = 200) -> func.HttpResponse:
    """Create a JSON HTTP response."""
    return func.HttpResponse(
        body=json.dumps(payload),
        status_code=status_code,
        mimetype="application/json",
    )


def require_route_param(
    req: func.HttpRequest, param_name: str
) -> Tuple[Optional[str], Optional[func.HttpResponse]]:
    """Return a required route parameter value or a 400 response."""
    value = req.route_params.get(param_name)
    if not value:
        return None, json_response(
            {"error": f"{param_name} route parameter is required"}, 400
        )
    return value, None
