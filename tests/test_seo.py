"""Tests for the Business Infinity SEO module — The Entropy Index.

Validates the canonical SEO taxonomy, JSON-LD structured data, parametric
deep-links, and generated website output.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

import pytest

from business_infinity.seo import (
    CHATROOM_URL,
    GITHUB_REPO,
    PAIN_TAXONOMY,
    SITE_URL,
    chatroom_deep_link,
    generate_faq_jsonld,
    generate_knowledge_graph_jsonld,
    generate_workflow_spec_jsonld,
    get_category_by_number,
    get_category_by_slug,
    github_yaml_url,
    pillar_page_url,
    render_jsonld_script,
    spec_page_url,
    total_query_count,
)

# ── Taxonomy Structure ───────────────────────────────────────────────────────


class TestPainTaxonomy:
    """Validate the canonical pain taxonomy data structure."""

    def test_exactly_ten_categories(self) -> None:
        assert len(PAIN_TAXONOMY) == 10

    def test_categories_numbered_one_through_ten(self) -> None:
        numbers = [cat["number"] for cat in PAIN_TAXONOMY]
        assert numbers == list(range(1, 11))

    def test_all_slugs_are_unique(self) -> None:
        slugs = [cat["slug"] for cat in PAIN_TAXONOMY]
        assert len(slugs) == len(set(slugs))

    def test_all_slugs_are_url_safe(self) -> None:
        for cat in PAIN_TAXONOMY:
            assert re.match(r"^[a-z0-9-]+$", cat["slug"]), (
                f"slug {cat['slug']!r} is not URL-safe"
            )

    def test_all_workflow_ids_are_unique(self) -> None:
        ids = [cat["workflow_id"] for cat in PAIN_TAXONOMY]
        assert len(ids) == len(set(ids))

    def test_all_required_fields_present(self) -> None:
        required = {
            "number", "slug", "title", "owner_agent", "owner_legend",
            "owner_title", "disease", "symptom", "workflow_id",
            "yaml_path", "queries",
        }
        for cat in PAIN_TAXONOMY:
            missing = required - set(cat.keys())
            assert not missing, (
                f"Category {cat['number']} missing fields: {missing}"
            )

    def test_total_queries_exceeds_100(self) -> None:
        """The Entropy Index must index 100+ raw panic-driven queries."""
        assert total_query_count() > 100

    def test_each_category_has_at_least_7_queries(self) -> None:
        for cat in PAIN_TAXONOMY:
            assert len(cat["queries"]) >= 7, (
                f"Category {cat['number']} ({cat['title']}) has only "
                f"{len(cat['queries'])} queries"
            )

    def test_query_dialects_are_valid(self) -> None:
        valid = {"technical", "emotional", "financial"}
        for cat in PAIN_TAXONOMY:
            for q in cat["queries"]:
                assert q["dialect"] in valid, (
                    f"Invalid dialect {q['dialect']!r} for query {q['q']!r}"
                )

    def test_all_three_dialects_represented_per_category(self) -> None:
        """Each category should weave in technical, emotional, and financial."""
        for cat in PAIN_TAXONOMY:
            dialects = {q["dialect"] for q in cat["queries"]}
            # At least 2 of 3 dialects should be present per category
            assert len(dialects) >= 2, (
                f"Category {cat['number']} ({cat['title']}) has only "
                f"dialects {dialects}"
            )

    def test_query_diagnostics_are_two_sentences(self) -> None:
        """Each diagnostic should be roughly 2 sentences (at least 2 periods)."""
        for cat in PAIN_TAXONOMY:
            for q in cat["queries"]:
                sentences = [
                    s.strip() for s in q["diagnostic"].split(".")
                    if s.strip()
                ]
                assert len(sentences) >= 2, (
                    f"Diagnostic for {q['q']!r} has only {len(sentences)} "
                    f"sentence(s)"
                )

    def test_yaml_paths_exist_on_disk(self) -> None:
        root = Path(__file__).resolve().parent.parent
        for cat in PAIN_TAXONOMY:
            yaml_path = root / cat["yaml_path"]
            assert yaml_path.exists(), (
                f"YAML file missing for category {cat['number']}: "
                f"{cat['yaml_path']}"
            )


class TestCategoryLookups:
    """Validate category lookup helpers."""

    def test_get_by_slug_returns_correct_category(self) -> None:
        cat = get_category_by_slug("culture-dilution-at-scale")
        assert cat["number"] == 6
        assert cat["owner_legend"] == "Peter Drucker"

    def test_get_by_number_returns_correct_category(self) -> None:
        cat = get_category_by_number(8)
        assert cat["slug"] == "exit-due-diligence-anxiety"
        assert cat["owner_legend"] == "Warren Buffett"

    def test_get_by_slug_raises_on_unknown(self) -> None:
        with pytest.raises(KeyError):
            get_category_by_slug("nonexistent")

    def test_get_by_number_raises_on_unknown(self) -> None:
        with pytest.raises(KeyError):
            get_category_by_number(99)


# ── Parametric Deep-Links ────────────────────────────────────────────────────


class TestDeepLinks:
    """Validate parametric chatroom deep-links."""

    def test_chatroom_deep_link_format(self) -> None:
        link = chatroom_deep_link("exit_readiness", "cfo")
        assert link == f"{CHATROOM_URL}?workflow=exit_readiness&agent=cfo"

    def test_github_yaml_url_format(self) -> None:
        url = github_yaml_url("docs/workflow/samples/pitch.yaml")
        assert url == f"{GITHUB_REPO}/blob/main/docs/workflow/samples/pitch.yaml"

    def test_spec_page_url_format(self) -> None:
        url = spec_page_url("founder_sovereignty")
        assert url == f"{SITE_URL}/specs/founder-sovereignty"

    def test_pillar_page_url_format(self) -> None:
        url = pillar_page_url("ai-sprawl-agentic-risk")
        assert url == f"{SITE_URL}/entropy-index/ai-sprawl-agentic-risk"

    def test_every_category_produces_valid_deep_link(self) -> None:
        for cat in PAIN_TAXONOMY:
            link = chatroom_deep_link(cat["workflow_id"], cat["owner_agent"])
            assert "workflow=" in link
            assert "agent=" in link
            assert cat["workflow_id"] in link
            assert cat["owner_agent"] in link


# ── JSON-LD Structured Data ──────────────────────────────────────────────────


class TestFAQJsonLD:
    """Validate FAQ Schema JSON-LD generation."""

    def test_faq_type_is_faq_page(self) -> None:
        cat = PAIN_TAXONOMY[0]
        ld = generate_faq_jsonld(cat)
        assert ld["@type"] == "FAQPage"

    def test_faq_has_schema_context(self) -> None:
        cat = PAIN_TAXONOMY[0]
        ld = generate_faq_jsonld(cat)
        assert ld["@context"] == "https://schema.org"

    def test_faq_question_count_matches_queries(self) -> None:
        for cat in PAIN_TAXONOMY:
            ld = generate_faq_jsonld(cat)
            assert len(ld["mainEntity"]) == len(cat["queries"])

    def test_faq_questions_contain_raw_queries(self) -> None:
        cat = PAIN_TAXONOMY[5]  # Culture Dilution
        ld = generate_faq_jsonld(cat)
        query_texts = {q["name"] for q in ld["mainEntity"]}
        for q in cat["queries"]:
            assert q["q"] in query_texts

    def test_faq_answers_contain_diagnostics(self) -> None:
        cat = PAIN_TAXONOMY[7]  # Exit Readiness
        ld = generate_faq_jsonld(cat)
        for i, entity in enumerate(ld["mainEntity"]):
            assert entity["acceptedAnswer"]["text"] == cat["queries"][i]["diagnostic"]

    def test_faq_is_valid_json(self) -> None:
        for cat in PAIN_TAXONOMY:
            ld = generate_faq_jsonld(cat)
            # Should be serializable to valid JSON
            json.dumps(ld)


class TestKnowledgeGraphJsonLD:
    """Validate the site-wide Knowledge Graph."""

    def test_knowledge_graph_type(self) -> None:
        kg = generate_knowledge_graph_jsonld()
        assert kg["@type"] == "ItemList"

    def test_knowledge_graph_has_10_items(self) -> None:
        kg = generate_knowledge_graph_jsonld()
        assert kg["numberOfItems"] == 10
        assert len(kg["itemListElement"]) == 10

    def test_knowledge_graph_items_are_services(self) -> None:
        kg = generate_knowledge_graph_jsonld()
        for item in kg["itemListElement"]:
            assert item["@type"] == "Service"

    def test_knowledge_graph_provider_is_asi_saga(self) -> None:
        kg = generate_knowledge_graph_jsonld()
        for item in kg["itemListElement"]:
            assert item["provider"]["name"] == "ASI Saga"

    def test_knowledge_graph_offers_contain_legends(self) -> None:
        kg = generate_knowledge_graph_jsonld()
        legend_names = {cat["owner_legend"] for cat in PAIN_TAXONOMY}
        for item in kg["itemListElement"]:
            offer_name = item["offers"]["name"]
            # Each offer should mention a legend name
            assert any(
                legend in offer_name for legend in legend_names
            ), f"Offer {offer_name!r} does not mention a legend"

    def test_knowledge_graph_is_valid_json(self) -> None:
        kg = generate_knowledge_graph_jsonld()
        json.dumps(kg)


class TestWorkflowSpecJsonLD:
    """Validate workflow spec JSON-LD."""

    def test_spec_type_is_software_source_code(self) -> None:
        cat = PAIN_TAXONOMY[0]
        ld = generate_workflow_spec_jsonld(cat)
        assert ld["@type"] == "SoftwareSourceCode"

    def test_spec_has_github_repository_link(self) -> None:
        for cat in PAIN_TAXONOMY:
            ld = generate_workflow_spec_jsonld(cat)
            assert GITHUB_REPO in ld["codeRepository"]

    def test_spec_language_is_yaml(self) -> None:
        cat = PAIN_TAXONOMY[0]
        ld = generate_workflow_spec_jsonld(cat)
        assert ld["programmingLanguage"] == "YAML"


# ── JSON-LD Rendering ────────────────────────────────────────────────────────


class TestRenderJsonLD:
    """Validate the HTML script tag renderer."""

    def test_renders_script_tag(self) -> None:
        data = {"@type": "Thing", "name": "Test"}
        result = render_jsonld_script(data)
        assert result.startswith('<script type="application/ld+json">')
        assert result.endswith("</script>")

    def test_contains_valid_json(self) -> None:
        data = {"@type": "FAQPage", "mainEntity": []}
        result = render_jsonld_script(data)
        # Extract JSON from between script tags
        json_str = result.split("\n", 1)[1].rsplit("\n", 1)[0]
        parsed = json.loads(json_str)
        assert parsed == data


# ── Generated Website Files ──────────────────────────────────────────────────


class TestGeneratedWebsite:
    """Validate generated website files (if they exist)."""

    _WEBSITE_DIR = Path(__file__).resolve().parent.parent / "website"

    def test_index_exists(self) -> None:
        assert (self._WEBSITE_DIR / "index.html").exists()

    def test_all_pillar_pages_exist(self) -> None:
        pillar_dir = self._WEBSITE_DIR / "entropy-index"
        for cat in PAIN_TAXONOMY:
            path = pillar_dir / f"{cat['slug']}.html"
            assert path.exists(), f"Missing pillar page: {path}"

    def test_all_spec_pages_exist(self) -> None:
        spec_dir = self._WEBSITE_DIR / "specs"
        for cat in PAIN_TAXONOMY:
            slug = cat["workflow_id"].replace("_", "-")
            path = spec_dir / f"{slug}.html"
            assert path.exists(), f"Missing spec page: {path}"

    def test_knowledge_graph_file_exists(self) -> None:
        path = self._WEBSITE_DIR / "knowledge-graph.jsonld"
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["@type"] == "ItemList"

    def test_pillar_pages_contain_faq_jsonld(self) -> None:
        pillar_dir = self._WEBSITE_DIR / "entropy-index"
        for cat in PAIN_TAXONOMY:
            path = pillar_dir / f"{cat['slug']}.html"
            content = path.read_text(encoding="utf-8")
            assert "application/ld+json" in content, (
                f"Pillar page {cat['slug']} missing JSON-LD"
            )
            # Validate the embedded JSON-LD
            matches = re.findall(
                r'<script type="application/ld\+json">\n(.*?)\n</script>',
                content,
                re.DOTALL,
            )
            assert len(matches) >= 1
            ld = json.loads(matches[0])
            assert ld["@type"] == "FAQPage"

    def test_pillar_pages_contain_deep_links(self) -> None:
        pillar_dir = self._WEBSITE_DIR / "entropy-index"
        for cat in PAIN_TAXONOMY:
            path = pillar_dir / f"{cat['slug']}.html"
            content = path.read_text(encoding="utf-8")
            assert f"workflow={cat['workflow_id']}" in content, (
                f"Pillar page {cat['slug']} missing deep-link"
            )
            assert f"agent={cat['owner_agent']}" in content, (
                f"Pillar page {cat['slug']} missing agent param"
            )

    def test_spec_pages_contain_github_links(self) -> None:
        spec_dir = self._WEBSITE_DIR / "specs"
        for cat in PAIN_TAXONOMY:
            slug = cat["workflow_id"].replace("_", "-")
            path = spec_dir / f"{slug}.html"
            content = path.read_text(encoding="utf-8")
            assert GITHUB_REPO in content, (
                f"Spec page {slug} missing GitHub link"
            )

    def test_spec_pages_contain_yaml_source(self) -> None:
        spec_dir = self._WEBSITE_DIR / "specs"
        for cat in PAIN_TAXONOMY:
            slug = cat["workflow_id"].replace("_", "-")
            path = spec_dir / f"{slug}.html"
            content = path.read_text(encoding="utf-8")
            assert "workflow_id:" in content, (
                f"Spec page {slug} missing YAML source display"
            )

    def test_all_pages_have_meta_description(self) -> None:
        for html_file in self._WEBSITE_DIR.rglob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            assert '<meta name="description"' in content, (
                f"Page {html_file.name} missing meta description"
            )

    def test_all_pages_have_canonical_link(self) -> None:
        for html_file in self._WEBSITE_DIR.rglob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            assert '<link rel="canonical"' in content, (
                f"Page {html_file.name} missing canonical link"
            )

    def test_pillar_pages_contain_all_three_dialect_tags(self) -> None:
        """Each pillar page should contain technical, emotional, and financial tags."""
        pillar_dir = self._WEBSITE_DIR / "entropy-index"
        for cat in PAIN_TAXONOMY:
            path = pillar_dir / f"{cat['slug']}.html"
            content = path.read_text(encoding="utf-8")
            dialects_in_page = {q["dialect"] for q in cat["queries"]}
            for dialect in dialects_in_page:
                assert f"tag--{dialect}" in content, (
                    f"Pillar {cat['slug']} missing dialect tag {dialect}"
                )
