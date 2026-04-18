"""JSON-LD structured data generators for SEO pages."""

from __future__ import annotations

import json
from typing import Any, Dict

from business_infinity.seo.deep_links import DeepLinkBuilder
from business_infinity.seo.taxonomy import PAIN_TAXONOMY, SITE_URL


class JsonLDGenerator:
    """Generate JSON-LD structured data for SEO pages."""

    @staticmethod
    def faq(category: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON-LD FAQPage schema for a single pain category."""
        main_entity = []
        for query in category["queries"]:
            main_entity.append({
                "@type": "Question",
                "name": query["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": query["diagnostic"],
                },
            })

        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "name": f"The Entropy Index — {category['title']}",
            "description": category["disease"],
            "mainEntity": main_entity,
        }

    @staticmethod
    def knowledge_graph() -> Dict[str, Any]:
        """Generate a comprehensive JSON-LD Knowledge Graph for the entire site."""
        items = []
        for cat in PAIN_TAXONOMY:
            items.append({
                "@type": "Service",
                "@id": f"{SITE_URL}/entropy-index/{cat['slug']}",
                "name": f"Business Infinity — {cat['title']}",
                "description": cat["disease"],
                "category": cat["title"],
                "provider": {
                    "@type": "Organization",
                    "name": "ASI Saga",
                    "url": "https://asisaga.com",
                },
                "serviceType": "Autonomous Strategic Governance",
                "areaServed": "Global",
                "offers": {
                    "@type": "Offer",
                    "name": (
                        f"{cat['owner_legend']} Agent — {cat['owner_title']}"
                    ),
                    "description": (
                        f"The {cat['owner_legend']} agent "
                        f"({cat['owner_title']}) addresses "
                        f"{cat['title'].lower()} through the "
                        f"{cat['workflow_id']} workflow."
                    ),
                    "url": DeepLinkBuilder.chatroom(
                        cat["workflow_id"], cat["owner_agent"]
                    ),
                },
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": f"Panic Queries — {cat['title']}",
                    "numberOfItems": len(cat["queries"]),
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": i + 1,
                            "name": q["q"],
                        }
                        for i, q in enumerate(cat["queries"])
                    ],
                },
            })

        return {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "@id": f"{SITE_URL}/entropy-index",
            "name": "The Entropy Index — Business Infinity Pain Taxonomy",
            "description": (
                "A comprehensive map of 10 organizational pain categories, "
                "each governed by a legendary CXO agent and backed by an "
                "executable workflow. Business Infinity meets founders at "
                "the exact moment their integrity is failing."
            ),
            "numberOfItems": len(PAIN_TAXONOMY),
            "itemListElement": items,
        }

    @staticmethod
    def workflow_spec(category: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON-LD SoftwareSourceCode schema for a workflow spec page."""
        return {
            "@context": "https://schema.org",
            "@type": "SoftwareSourceCode",
            "name": (
                f"{category['workflow_id']} — Business Infinity Workflow Spec"
            ),
            "description": category["disease"],
            "codeRepository": DeepLinkBuilder.github_yaml(
                category["yaml_path"]
            ),
            "programmingLanguage": "YAML",
            "targetProduct": {
                "@type": "SoftwareApplication",
                "name": "Business Infinity",
                "applicationCategory": "Autonomous Strategic Governance",
                "operatingSystem": "Agent Operating System (AOS)",
            },
            "author": {
                "@type": "Organization",
                "name": "ASI Saga",
                "url": "https://asisaga.com",
            },
        }

    @staticmethod
    def render_script(data: Dict[str, Any]) -> str:
        """Render a JSON-LD dict as an HTML ``<script>`` tag."""
        return (
            '<script type="application/ld+json">\n'
            + json.dumps(data, indent=2)
            + "\n</script>"
        )
