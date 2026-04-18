"""Parametric deep-link builders for chatroom, GitHub, and site pages."""

from __future__ import annotations

from business_infinity.seo.taxonomy import CHATROOM_URL, GITHUB_REPO, SITE_URL


class DeepLinkBuilder:
    """Construct parametric URLs for chatroom, GitHub, and site pages."""

    @staticmethod
    def chatroom(workflow_id: str, agent: str) -> str:
        """Build a parametric chatroom URL that pre-loads a specific workflow."""
        return f"{CHATROOM_URL}?workflow={workflow_id}&agent={agent}"

    @staticmethod
    def github_yaml(yaml_path: str) -> str:
        """Build a GitHub URL for viewing the source YAML spec."""
        return f"{GITHUB_REPO}/blob/main/{yaml_path}"

    @staticmethod
    def spec_page(workflow_id: str) -> str:
        """Build a website URL for a workflow's public spec page."""
        slug = workflow_id.replace("_", "-")
        return f"{SITE_URL}/specs/{slug}"

    @staticmethod
    def pillar_page(category_slug: str) -> str:
        """Build a website URL for a pain category's pillar page."""
        return f"{SITE_URL}/entropy-index/{category_slug}"
