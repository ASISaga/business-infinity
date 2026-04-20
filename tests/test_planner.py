"""Tests for the Microsoft Planner integration modules.

Tests cover:
- ResponsibilitiesLoader — JSON-LD file loading and parsing
- PlannerSync — plan/bucket/task creation and idempotency
- PlannerMonitor — status query and summarise helper
- PlannerWorkflows — workflow entry points
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from business_infinity.planner.responsibilities import (
    Responsibility,
    ResponsibilitiesLoader,
    RoleResponsibilities,
)
from business_infinity.planner.sync import (
    PlannerMonitor,
    PlannerSync,
    SyncResult,
    TaskStatus,
)
from business_infinity.workflows.planner import PlannerWorkflows


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _make_responsibility_jsonld(agent_id: str, role: str, dimension: str, slug: str) -> dict:
    """Return a minimal valid responsibility JSON-LD dict."""
    return {
        "@context": "https://asisaga.com/contexts/responsibilities.jsonld",
        "@id": f"agent:{agent_id}/responsibilities/{slug}",
        "@type": "RoleResponsibilities",
        "role": role,
        "dimension": dimension,
        "dimension_frame": f"The {dimension} frame for {role}.",
        "erhard_principle": "I am the committed source of everything here.",
        "responsibilities": [
            {
                "@type": "Responsibility",
                "title": f"{role} {dimension} Responsibility A",
                "commitment": "I am the committed source of outcome A.",
                "scope": "The entire scope of domain A.",
                "accountability": "Measurable metric A is achieved.",
            },
            {
                "@type": "Responsibility",
                "title": f"{role} {dimension} Responsibility B",
                "commitment": "I am the committed source of outcome B.",
                "scope": "The entire scope of domain B.",
                "accountability": "Measurable metric B is achieved.",
            },
        ],
    }


@pytest.fixture()
def temp_mind_dir(tmp_path: Path) -> Path:
    """Create a temporary boardroom/mind directory with two test agents."""
    mind = tmp_path / "mind"
    mind.mkdir()
    for agent_id, role in [("ceo", "CEO"), ("cfo", "CFO")]:
        resp_dir = mind / agent_id / "Responsibilities"
        resp_dir.mkdir(parents=True)
        for slug, dimension in [
            ("entrepreneur", "Entrepreneur"),
            ("manager", "Manager"),
            ("domain-expert", "DomainExpert"),
        ]:
            data = _make_responsibility_jsonld(agent_id, role, dimension, slug)
            (resp_dir / f"{slug}.jsonld").write_text(json.dumps(data), encoding="utf-8")
    return mind


# ── ResponsibilitiesLoader tests ──────────────────────────────────────────────


class TestResponsibilitiesLoader:
    def test_available_agents(self, temp_mind_dir: Path) -> None:
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        agents = loader.available_agents()
        assert "ceo" in agents
        assert "cfo" in agents

    def test_load_agent_returns_three_dimensions(self, temp_mind_dir: Path) -> None:
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        dims = loader.load_agent("ceo")
        assert len(dims) == 3
        slugs = {d.dimension_slug for d in dims}
        assert slugs == {"entrepreneur", "manager", "domain-expert"}

    def test_load_dimension_parses_fields(self, temp_mind_dir: Path) -> None:
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        dim = loader.load_dimension("ceo", "entrepreneur")
        assert dim is not None
        assert dim.agent_id == "ceo"
        assert dim.role == "CEO"
        assert dim.dimension == "Entrepreneur"
        assert dim.dimension_slug == "entrepreneur"
        assert len(dim.responsibilities) == 2
        resp = dim.responsibilities[0]
        assert resp.title == "CEO Entrepreneur Responsibility A"
        assert resp.commitment.startswith("I am the committed source of")
        assert resp.scope
        assert resp.accountability

    def test_load_dimension_missing_file_returns_none(self, temp_mind_dir: Path) -> None:
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        result = loader.load_dimension("nonexistent_agent", "manager")
        assert result is None

    def test_load_dimension_invalid_slug_raises(self, temp_mind_dir: Path) -> None:
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        with pytest.raises(ValueError, match="Unknown dimension slug"):
            loader.load_dimension("ceo", "invalid-dimension")

    def test_load_agent_missing_agent_returns_empty(self, temp_mind_dir: Path) -> None:
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        dims = loader.load_agent("nonexistent_agent")
        assert dims == []

    def test_planner_task_id_parsed_when_present(self, temp_mind_dir: Path) -> None:
        """planner_task_id field is preserved when present in the JSON-LD file."""
        data = _make_responsibility_jsonld("ceo", "CEO", "Manager", "manager")
        data["responsibilities"][0]["planner_task_id"] = "task-abc-123"
        resp_path = temp_mind_dir / "ceo" / "Responsibilities" / "manager.jsonld"
        resp_path.write_text(json.dumps(data), encoding="utf-8")

        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        dim = loader.load_dimension("ceo", "manager")
        assert dim.responsibilities[0].planner_task_id == "task-abc-123"
        assert dim.responsibilities[1].planner_task_id is None


# ── PlannerSync tests ─────────────────────────────────────────────────────────


def _make_graph_task(task_id: str, title: str, bucket_id: str = "b1") -> MagicMock:
    task = MagicMock()
    task.id = task_id
    task.title = title
    task.bucket_id = bucket_id
    task.percent_complete = 0
    return task


def _make_graph_bucket(bucket_id: str, name: str) -> MagicMock:
    bucket = MagicMock()
    bucket.id = bucket_id
    bucket.name = name
    return bucket


def _make_graph_plan(plan_id: str, title: str) -> MagicMock:
    plan = MagicMock()
    plan.id = plan_id
    plan.title = title
    return plan


class TestPlannerSync:
    def _make_syncer(self, temp_mind_dir: Path, graph_mock: MagicMock) -> PlannerSync:
        planner_client = MagicMock()
        planner_client.graph = graph_mock
        loader = ResponsibilitiesLoader(mind_dir=temp_mind_dir)
        return PlannerSync(planner_client=planner_client, loader=loader)

    def _build_graph_mock(
        self,
        existing_plans: Optional[List] = None,
        existing_buckets: Optional[List] = None,
        existing_tasks: Optional[List] = None,
        created_plan_id: str = "plan-1",
        created_bucket_id: str = "bucket-1",
        created_task_id: str = "task-1",
    ) -> MagicMock:
        """Build a MagicMock graph client that mirrors the Graph SDK structure."""
        graph = MagicMock()

        # plans.get()
        plans_resp = MagicMock()
        plans_resp.value = existing_plans or []
        graph.planner.plans.get = AsyncMock(return_value=plans_resp)

        # plans.post()
        new_plan = MagicMock()
        new_plan.id = created_plan_id
        graph.planner.plans.post = AsyncMock(return_value=new_plan)

        # plans.by_id().buckets.get()
        buckets_resp = MagicMock()
        buckets_resp.value = existing_buckets or []
        plan_item = MagicMock()
        plan_item.buckets.get = AsyncMock(return_value=buckets_resp)
        plan_item.tasks.get = AsyncMock(
            return_value=MagicMock(value=existing_tasks or [])
        )
        graph.planner.plans.by_planner_plan_id = MagicMock(return_value=plan_item)

        # buckets.post()
        new_bucket = MagicMock()
        new_bucket.id = created_bucket_id
        graph.planner.buckets.post = AsyncMock(return_value=new_bucket)

        # tasks.post()
        new_task = MagicMock()
        new_task.id = created_task_id
        graph.planner.tasks.post = AsyncMock(return_value=new_task)

        # task details
        task_item = MagicMock()
        details_resp = MagicMock()
        details_resp.additional_data = {"@odata.etag": "W/\"etag-123\""}
        task_item.details.get = AsyncMock(return_value=details_resp)
        task_item.details.patch = AsyncMock(return_value=None)
        graph.planner.tasks.by_planner_task_id = MagicMock(return_value=task_item)

        return graph

    async def test_sync_agent_creates_plan_and_tasks(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-123")
        graph = self._build_graph_mock()
        syncer = self._make_syncer(temp_mind_dir, graph)

        result = await syncer.sync_agent("ceo")

        assert result.agent_id == "ceo"
        assert result.role == "CEO"
        assert result.plan_id == "plan-1"
        assert result.buckets_synced == 3  # entrepreneur, manager, domain-expert
        assert result.tasks_created > 0
        assert result.tasks_skipped == 0
        assert result.errors == []
        graph.planner.plans.post.assert_called_once()

    async def test_sync_agent_skips_existing_tasks(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-123")
        # Simulate a pre-existing plan with tasks for all three dimensions.
        existing_plan = _make_graph_plan("plan-existing", "CEO Responsibilities")
        all_tasks: List[MagicMock] = []
        for idx, (slug, dimension_name) in enumerate(
            [("entrepreneur", "Entrepreneur"), ("manager", "Manager"), ("domain-expert", "DomainExpert")]
        ):
            dim_data = _make_responsibility_jsonld("ceo", "CEO", dimension_name, slug)
            for resp_idx, resp in enumerate(dim_data["responsibilities"]):
                all_tasks.append(_make_graph_task(f"t{idx}{resp_idx}", resp["title"]))

        graph = self._build_graph_mock(
            existing_plans=[existing_plan],
            existing_tasks=all_tasks,
        )
        syncer = self._make_syncer(temp_mind_dir, graph)

        result = await syncer.sync_agent("ceo")

        # No new plan should be created.
        graph.planner.plans.post.assert_not_called()
        assert result.plan_id == "plan-existing"
        assert result.tasks_created == 0
        assert result.tasks_skipped > 0

    async def test_sync_dimension_only_syncs_one_dimension(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-123")
        graph = self._build_graph_mock()
        syncer = self._make_syncer(temp_mind_dir, graph)

        result = await syncer.sync_dimension("cfo", "manager")

        assert result.agent_id == "cfo"
        assert result.role == "CFO"
        assert result.buckets_synced == 1

    async def test_sync_agent_no_group_id_raises(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("PLANNER_GROUP_ID", raising=False)
        monkeypatch.delenv("PLANNER_GROUP_ID_CEO", raising=False)
        graph = self._build_graph_mock()
        syncer = self._make_syncer(temp_mind_dir, graph)

        with pytest.raises(EnvironmentError, match="PLANNER_GROUP_ID"):
            await syncer.sync_agent("ceo")

    async def test_sync_unknown_agent_raises(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-123")
        graph = self._build_graph_mock()
        syncer = self._make_syncer(temp_mind_dir, graph)

        with pytest.raises(ValueError, match="No responsibility files found"):
            await syncer.sync_agent("unknown_agent")

    async def test_task_creation_error_recorded_not_raised(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-123")
        graph = self._build_graph_mock()
        # Make task creation fail.
        graph.planner.tasks.post = AsyncMock(side_effect=RuntimeError("Graph API down"))
        syncer = self._make_syncer(temp_mind_dir, graph)

        result = await syncer.sync_agent("ceo")

        assert result.tasks_created == 0
        assert len(result.errors) > 0
        assert "Graph API down" in result.errors[0]


# ── PlannerMonitor tests ──────────────────────────────────────────────────────


class TestPlannerMonitor:
    def _make_monitor(self, graph_mock: MagicMock) -> PlannerMonitor:
        planner_client = MagicMock()
        planner_client.graph = graph_mock
        return PlannerMonitor(planner_client=planner_client)

    async def test_get_plan_status_returns_sorted_statuses(self) -> None:
        graph = MagicMock()

        tasks = [
            _make_graph_task("t1", "Vision Setting", "b1"),
            _make_graph_task("t2", "Budget Governance", "b2"),
        ]
        tasks[0].percent_complete = 100
        tasks[1].percent_complete = 50

        buckets = [
            _make_graph_bucket("b1", "Entrepreneur"),
            _make_graph_bucket("b2", "Manager"),
        ]

        plan_item = MagicMock()
        plan_item.tasks.get = AsyncMock(return_value=MagicMock(value=tasks))
        plan_item.buckets.get = AsyncMock(return_value=MagicMock(value=buckets))
        graph.planner.plans.by_planner_plan_id = MagicMock(return_value=plan_item)

        monitor = self._make_monitor(graph)
        statuses = await monitor.get_plan_status("plan-123")

        assert len(statuses) == 2
        # Sorted by dimension then title: Entrepreneur < Manager
        assert statuses[0].dimension == "Entrepreneur"
        assert statuses[1].dimension == "Manager"

    async def test_get_agent_status_resolves_by_role(self) -> None:
        graph = MagicMock()

        plans_resp = MagicMock()
        plans_resp.value = [
            _make_graph_plan("plan-ceo", "CEO Responsibilities"),
            _make_graph_plan("plan-cfo", "CFO Responsibilities"),
        ]
        graph.planner.plans.get = AsyncMock(return_value=plans_resp)

        plan_item = MagicMock()
        plan_item.tasks.get = AsyncMock(return_value=MagicMock(value=[]))
        plan_item.buckets.get = AsyncMock(return_value=MagicMock(value=[]))
        graph.planner.plans.by_planner_plan_id = MagicMock(return_value=plan_item)

        monitor = self._make_monitor(graph)
        statuses = await monitor.get_agent_status("CEO")

        assert statuses == []
        graph.planner.plans.by_planner_plan_id.assert_called_with("plan-ceo")

    async def test_get_agent_status_returns_none_when_not_found(self) -> None:
        graph = MagicMock()
        plans_resp = MagicMock()
        plans_resp.value = [_make_graph_plan("plan-cfo", "CFO Responsibilities")]
        graph.planner.plans.get = AsyncMock(return_value=plans_resp)

        monitor = self._make_monitor(graph)
        result = await monitor.get_agent_status("CEO")
        assert result is None

    def test_summarise_empty(self) -> None:
        summary = PlannerMonitor.summarise([])
        assert summary["total"] == 0
        assert summary["overall_percent"] == 0

    def test_summarise_mixed_statuses(self) -> None:
        statuses = [
            TaskStatus(title="A", task_id="t1", percent_complete=100, dimension="Entrepreneur"),
            TaskStatus(title="B", task_id="t2", percent_complete=50, dimension="Entrepreneur"),
            TaskStatus(title="C", task_id="t3", percent_complete=0, dimension="Manager"),
        ]
        summary = PlannerMonitor.summarise(statuses)
        assert summary["total"] == 3
        assert summary["complete"] == 1
        assert summary["in_progress"] == 1
        assert summary["not_started"] == 1
        assert summary["overall_percent"] == 50  # (100+50+0)/3 = 50
        by_dim = summary["by_dimension"]
        assert "Entrepreneur" in by_dim
        assert "Manager" in by_dim
        assert by_dim["Entrepreneur"]["complete"] == 1
        assert by_dim["Manager"]["complete"] == 0


# ── PlannerWorkflows tests ────────────────────────────────────────────────────


class TestPlannerWorkflows:
    """Test workflow entry-point routing and error handling."""

    def _make_request(self, body: Dict[str, Any]) -> MagicMock:
        req = MagicMock()
        req.body = body
        return req

    async def test_sync_responsibilities_calls_sync_agent(
        self, temp_mind_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-abc")

        sync_result = SyncResult(
            agent_id="ceo",
            role="CEO",
            plan_id="plan-1",
            plan_title="CEO Responsibilities",
            buckets_synced=3,
            tasks_created=18,
        )
        mock_syncer = MagicMock()
        mock_syncer.sync_agent = AsyncMock(return_value=sync_result)
        mock_syncer.sync_dimension = AsyncMock(return_value=sync_result)

        with patch("business_infinity.workflows.planner.PlannerClient"), \
             patch("business_infinity.workflows.planner.PlannerSync", return_value=mock_syncer):
            request = self._make_request({"agent_id": "ceo"})
            result = await PlannerWorkflows.sync_responsibilities(request)

        assert result["agent_id"] == "ceo"
        assert result["tasks_created"] == 18
        mock_syncer.sync_agent.assert_called_once_with("ceo", group_id=None)

    async def test_sync_responsibilities_with_dimension(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PLANNER_GROUP_ID", "group-abc")

        sync_result = SyncResult(
            agent_id="cfo",
            role="CFO",
            plan_id="plan-2",
            plan_title="CFO Responsibilities",
            buckets_synced=1,
            tasks_created=6,
        )
        mock_syncer = MagicMock()
        mock_syncer.sync_dimension = AsyncMock(return_value=sync_result)

        with patch("business_infinity.workflows.planner.PlannerClient"), \
             patch("business_infinity.workflows.planner.PlannerSync", return_value=mock_syncer):
            request = self._make_request(
                {"agent_id": "cfo", "dimension": "manager", "group_id": "grp-override"}
            )
            result = await PlannerWorkflows.sync_responsibilities(request)

        mock_syncer.sync_dimension.assert_called_once_with(
            "cfo", "manager", group_id="grp-override"
        )
        assert result["buckets_synced"] == 1

    async def test_get_responsibilities_status_by_role(self) -> None:
        statuses = [
            TaskStatus(title="Vision", task_id="t1", percent_complete=80, dimension="Entrepreneur")
        ]
        mock_monitor = MagicMock()
        mock_monitor.get_agent_status = AsyncMock(return_value=statuses)

        mock_monitor_cls = MagicMock(return_value=mock_monitor)
        mock_monitor_cls.summarise = MagicMock(return_value={"overall_percent": 80})

        with patch("business_infinity.workflows.planner.PlannerClient"), \
             patch("business_infinity.workflows.planner.PlannerMonitor", mock_monitor_cls):
            request = self._make_request({"role": "CEO"})
            result = await PlannerWorkflows.get_responsibilities_status(request)

        assert result["found"] is True
        assert result["role"] == "CEO"
        assert len(result["tasks"]) == 1
        assert result["summary"]["overall_percent"] == 80

    async def test_get_responsibilities_status_not_found(self) -> None:
        mock_monitor = MagicMock()
        mock_monitor.get_agent_status = AsyncMock(return_value=None)

        with patch("business_infinity.workflows.planner.PlannerClient"), \
             patch("business_infinity.workflows.planner.PlannerMonitor", return_value=mock_monitor):
            request = self._make_request({"role": "CSO"})
            result = await PlannerWorkflows.get_responsibilities_status(request)

        assert result["found"] is False
        assert "CSO" in result["message"]

    async def test_get_responsibilities_status_missing_args_raises(self) -> None:
        with patch("business_infinity.workflows.planner.PlannerClient"), \
             patch("business_infinity.workflows.planner.PlannerMonitor"):
            request = self._make_request({})
            with pytest.raises(ValueError, match="role.*plan_id"):
                await PlannerWorkflows.get_responsibilities_status(request)
