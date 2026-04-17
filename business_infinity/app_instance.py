"""Shared AOS app instance for workflow registration."""

from __future__ import annotations

from aos_client import AOSApp

_APP: AOSApp | None = None


def set_app(app: AOSApp) -> None:
    """Store the initialized AOS app instance."""
    global _APP  # pylint: disable=global-statement
    _APP = app


def get_app() -> AOSApp:
    """Return the initialized AOS app instance."""
    app = _APP
    if app is None:
        raise RuntimeError(
            "AOSApp has not been initialized. Import function_app before "
            "accessing workflow definitions (for example: `import function_app`)."
        )
    return app
