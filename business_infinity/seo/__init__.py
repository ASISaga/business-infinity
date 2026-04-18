"""Business Infinity SEO — The Entropy Index.

Canonical SEO taxonomy, parametric deep-links, and JSON-LD structured data.
"""

from business_infinity.seo.deep_links import DeepLinkBuilder
from business_infinity.seo.jsonld import JsonLDGenerator
from business_infinity.seo.taxonomy import (
    CHATROOM_URL,
    GITHUB_REPO,
    PAIN_TAXONOMY,
    SITE_URL,
    PainTaxonomy,
)

__all__ = [
    "CHATROOM_URL",
    "DeepLinkBuilder",
    "GITHUB_REPO",
    "JsonLDGenerator",
    "PAIN_TAXONOMY",
    "PainTaxonomy",
    "SITE_URL",
]
