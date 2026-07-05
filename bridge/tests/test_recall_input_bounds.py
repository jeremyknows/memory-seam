from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest

from memory_seam_mcp import server as bridge_server


@dataclass
class RecordingRuntime:
    targets: list[str] = field(default_factory=list)

    def handle(self, request: Any) -> dict[str, Any]:
        self.targets.append(request.target)
        return {"status_code": 200, "body": {"endpoint": "recall"}}


@pytest.mark.parametrize(
    ("query", "error"),
    [
        ({"not": "a string"}, "invalid_query_type"),
        ("x" * (bridge_server.MAX_QUERY_CHARS + 1), "query_too_long"),
        (" ".join(f"t{i}" for i in range(bridge_server.MAX_QUERY_TERMS + 1)), "query_too_many_terms"),
    ],
)
def test_recall_rejects_bad_query_bounds(query: Any, error: str) -> None:
    runtime = RecordingRuntime()

    envelope = bridge_server.memory_seam_recall_envelope(runtime, query=query, n=5)

    assert envelope["status_code"] == 400
    assert envelope["body"]["endpoint"] == "recall"
    assert envelope["body"]["error"] == error
    assert envelope["body"]["contract_status"] == "bridge_input_rejected"
    assert envelope["bridge"]["transport"] == "stdio"
    assert runtime.targets == []


@pytest.mark.parametrize("n", ["5", 1.5, True, None])
def test_recall_rejects_non_integer_n(n: Any) -> None:
    runtime = RecordingRuntime()

    envelope = bridge_server.memory_seam_recall_envelope(runtime, query="runtime boundary", n=n)

    assert envelope["status_code"] == 400
    assert envelope["body"]["error"] == "invalid_n_type"
    assert runtime.targets == []


@pytest.mark.parametrize(
    ("requested_n", "effective_n"),
    [
        (0, bridge_server.MIN_RECALL_N),
        (-10, bridge_server.MIN_RECALL_N),
        (999, bridge_server.MAX_RECALL_N),
    ],
)
def test_recall_clamps_integer_n(requested_n: int, effective_n: int) -> None:
    runtime = RecordingRuntime()

    envelope = bridge_server.memory_seam_recall_envelope(runtime, query="runtime boundary", n=requested_n)

    assert envelope["status_code"] == 200
    assert len(runtime.targets) == 1
    params = parse_qs(urlsplit(runtime.targets[0]).query)
    assert params["n"] == [str(effective_n)]


def test_recall_accepts_core_query_length_limit() -> None:
    runtime = RecordingRuntime()

    envelope = bridge_server.memory_seam_recall_envelope(runtime, query="x" * bridge_server.MAX_QUERY_CHARS, n=5)

    assert envelope["status_code"] == 200
    assert len(runtime.targets) == 1
