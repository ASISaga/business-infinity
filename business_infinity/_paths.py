"""Canonical project root and derived paths.

All modules that need to resolve paths relative to the project root should
import ``PROJECT_ROOT`` from here instead of computing it via ``__file__``.
"""

from __future__ import annotations

from pathlib import Path

#: Absolute path to the project root (the directory containing ``business_infinity/``).
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
