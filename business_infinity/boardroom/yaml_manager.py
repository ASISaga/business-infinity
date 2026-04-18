"""Workflow YAML I/O — loading, validation, and saving.

Handles YAML I/O for boardroom workflow definitions stored in
``docs/workflow/samples/``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from business_infinity._paths import PROJECT_ROOT
from business_infinity.boardroom.registry import WorkflowRegistryManager


class WorkflowYAMLManager:
    """Handles YAML I/O for boardroom workflow definitions."""

    @staticmethod
    def _resolve_yaml_path(yaml_path: str) -> Path:
        """Resolve a registry ``yaml_path`` to an absolute filesystem path."""
        return PROJECT_ROOT / yaml_path

    @staticmethod
    def _validate_data(data: Dict[str, Any]) -> None:
        """Validate a workflow data dict before saving."""
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
            for i, action in enumerate(step["actions"]):
                if not isinstance(action, dict):
                    raise ValueError(f"Step '{step_id}' action[{i}] must be a mapping")
                for field in ("label", "description", "url"):
                    if field not in action:
                        raise ValueError(
                            f"Step '{step_id}' action[{i}] missing required field '{field}'"
                        )

    @classmethod
    def load(cls, workflow_id: str) -> Dict[str, Any]:
        """Load and parse the YAML file for a registered workflow.

        Raises :class:`KeyError` if *workflow_id* is not registered.
        Raises :class:`FileNotFoundError` if the YAML file does not exist.
        Raises :class:`ValueError` if the YAML file is malformed.
        """
        metadata = WorkflowRegistryManager.get_metadata(workflow_id)
        yaml_path = cls._resolve_yaml_path(metadata["yaml_path"])
        with open(str(yaml_path), "r", encoding="utf-8") as fh:
            try:
                return yaml.safe_load(fh)
            except yaml.YAMLError as exc:
                raise ValueError(
                    f"Malformed YAML in workflow '{workflow_id}' "
                    f"({metadata['yaml_path']}): {exc}"
                ) from exc

    @classmethod
    def save(cls, workflow_id: str, data: Dict[str, Any]) -> None:
        """Validate and save an updated workflow structure to its YAML file.

        Raises :class:`KeyError` if *workflow_id* is not registered.
        Raises :class:`ValueError` if *data* fails validation.
        """
        metadata = WorkflowRegistryManager.get_metadata(workflow_id)
        cls._validate_data(data)
        yaml_path = cls._resolve_yaml_path(metadata["yaml_path"])
        with open(str(yaml_path), "w", encoding="utf-8") as fh:
            yaml.dump(
                data, fh, default_flow_style=False, sort_keys=False, allow_unicode=True
            )
