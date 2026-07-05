"""No-live source adapter protocols and synthetic dogfood helpers.

The L4 adapter surface proves usefulness against safe, committed fixture content.
It does not discover local sources, read private files, call live backends, or
fall back to raw transcripts.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable, Protocol, runtime_checkable

from .contracts import CONTRACT_STATUS, MAX_RECALL_N, MAX_QUERY_CHARS
from .providers import MemorySeamProvider

DOGFOOD_USEFULNESS_STATUS = "synthetic_safe_content_usefulness_proof"
SAFE_SOURCE_CARD_ADAPTER_STATUS = "safe_source_card_adapter_no_live_metadata_only"
ADAPTER_PROTOCOL_VERSION = "0.2"
SYNTHETIC_USEFULNESS_RUBRIC_VERSION = "synthetic_usefulness_rubric_v0"
SYNTHETIC_RECALL_RANKING_FIXTURE_VERSION = "synthetic_recall_ranking_fixture_v0"
RECALL_LIMITS = {"max_n": MAX_RECALL_N}
SCAN_TRUNCATED_ITEM_REASONS = {
    "scan_file_cap_reached",
    "record_cap_reached",
    "row_cap_reached",
}
LOCAL_READ_ADAPTER_NAMES = {
    "local-markdown-folder",
    "local-plain-text-folder",
    "local-jsonl-export",
    "local-git-current-tree",
    "local-sqlite-notes",
}

FORBIDDEN_SOURCE_CARD_FRAGMENTS = (
    "/" + "Users" + "/",
    "\\Users\\",
    "gho_",
    "ghp_",
    "sk-",
    "BEGIN PRIVATE KEY",
    "raw_transcript",
    "session.jsonl",
    ".env",
)

REDACTION_PLACEHOLDERS = (
    "[redacted-token]",
    "[redacted-credential-ref]",
    "[redacted-platform-id]",
    "[redacted-private-path]",
)


@dataclass(frozen=True)
class SourceCard:
    """Report-safe metadata card for a source without raw path/content fields."""

    card_id: str
    include_family: str
    source_tier: str
    private_class: str
    canonicality: str
    retrieval_backend: str
    title: str
    safe_summary: str
    reportable: bool = True
    redaction_applied: bool = False
    redaction_labels: tuple[str, ...] = ()

    def to_safe_detail(self) -> dict[str, Any]:
        detail = {
            "card_id": self.card_id,
            "include_family": self.include_family,
            "source_tier": self.source_tier,
            "private_class": self.private_class,
            "canonicality": self.canonicality,
            "retrieval_backend": self.retrieval_backend,
            "title": self.title,
            "safe_summary": self.safe_summary,
            "reportable": self.reportable,
            "redaction_applied": self.redaction_applied,
            "redaction_labels": list(self.redaction_labels),
        }
        assert_source_card_is_report_safe(detail)
        return detail


def assert_source_card_is_report_safe(detail: dict[str, Any]) -> None:
    """Reject obvious raw path/content/credential leakage in a source card."""

    forbidden_keys = {"path", "absolute_path", "root", "content", "raw_content", "transcript", "secret", "token"}
    leaked_keys = forbidden_keys.intersection(detail)
    if leaked_keys:
        raise ValueError(f"source card contains unsafe fields: {sorted(leaked_keys)}")
    rendered = repr(detail)
    if any(fragment in rendered for fragment in FORBIDDEN_SOURCE_CARD_FRAGMENTS):
        raise ValueError("source card contains an unsafe raw/private fragment")
    if not detail.get("safe_summary"):
        raise ValueError("source card must include a safe_summary")


def _snippet_survives_redaction(snippet: str) -> bool:
    remaining = snippet.strip()
    for placeholder in REDACTION_PLACEHOLDERS:
        remaining = remaining.replace(placeholder, "")
    return bool(remaining.strip())


def rank_synthetic_recall_items(
    items: Iterable[dict[str, Any]],
    query: str,
    *,
    n: int = MAX_RECALL_N,
) -> dict[str, Any]:
    """Rank committed synthetic recall items deterministically.

    The fixture scores only caller-supplied safe item dictionaries. It never
    discovers sources, opens paths, calls providers, reads live indexes, or falls
    back to raw/private content. Ties are resolved by title and id so tests can
    pin retrieval quality without depending on gbrain or live indexes.
    """

    terms = tuple(
        term.casefold()
        for term in re.findall(r"[\w'-]+", query[:MAX_QUERY_CHARS], flags=re.UNICODE)
        if term.strip("_'-")
    )
    if not terms:
        return {
            "schema": SYNTHETIC_RECALL_RANKING_FIXTURE_VERSION,
            "query_terms": [],
            "items": [],
            "item_count": 0,
            "degraded": False,
            "degraded_reasons": [],
            "raw_fallback_used": False,
            "read_backend_called": False,
            "live_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "write_custody_or_reindex": False,
            "recall_diagnostics": {"zero_reason": "empty_query"},
        }
    ranked: list[dict[str, Any]] = []
    for position, item in enumerate(items):
        candidate = dict(item)
        haystack = f"{candidate.get('title', '')} {candidate.get('snippet', '')}".casefold()
        term_hits = sum(1 for term in terms if term in haystack)
        exact_title = bool(terms) and all(term in str(candidate.get("title", "")).casefold() for term in terms)
        score = (term_hits * 10) + (5 if exact_title else 0)
        if score <= 0 and terms:
            continue
        ranked.append(
            {
                **candidate,
                "ranking_score": score,
                "ranking_reason": "term_match" if term_hits else "empty_query_fixture_order",
                "ranking_tiebreak": str(candidate.get("title") or candidate.get("id") or position),
                "source_order": position,
            }
        )

    ranked.sort(
        key=lambda item: (
            -int(item["ranking_score"]),
            str(item["ranking_tiebreak"]),
            int(item["source_order"]),
        )
    )
    limit = max(0, min(int(n), MAX_RECALL_N))
    limited = ranked[:limit]
    return {
        "schema": SYNTHETIC_RECALL_RANKING_FIXTURE_VERSION,
        "query_terms": list(terms),
        "items": limited,
        "item_count": len(limited),
        "degraded": False,
        "degraded_reasons": [],
        "raw_fallback_used": False,
        "read_backend_called": False,
        "live_backend_called": False,
        "service_started": False,
        "runtime_registry_consumed": False,
        "write_custody_or_reindex": False,
    }


def score_synthetic_usefulness(
    items: Iterable[dict[str, Any]],
    *,
    degraded_reasons: Iterable[str] = (),
) -> dict[str, Any]:
    """Score synthetic dogfood evidence without reading live/private sources.

    The rubric classifies already-supplied synthetic items into PASS/HOLD/FAIL
    outcomes and returns only booleans, counts, and safe reason codes. It never
    discovers sources, opens paths, calls providers, or inspects raw/private
    content outside the caller's committed fixture payload.
    """

    item_list = [dict(item) for item in items]
    degraded = [str(reason) for reason in degraded_reasons if str(reason)]
    reason_codes: list[str] = []

    rendered = repr(item_list)
    safe = True
    if any(fragment in rendered for fragment in FORBIDDEN_SOURCE_CARD_FRAGMENTS):
        safe = False
        reason_codes.append("unsafe_fragment_detected")

    snippets = [str(item.get("snippet") or "") for item in item_list]
    non_empty_snippets = [snippet for snippet in snippets if snippet.strip()]
    answerable_snippets = [snippet for snippet in non_empty_snippets if _snippet_survives_redaction(snippet)]
    answerable = bool(answerable_snippets)
    redaction_applied = any(bool(item.get("redaction_applied")) for item in item_list)
    redaction_survived = redaction_applied and answerable
    truncated = any(bool(item.get("truncated")) for item in item_list)
    too_degraded = bool(degraded) and not answerable

    if not item_list:
        reason_codes.append("no_synthetic_evidence")
    if item_list and not non_empty_snippets:
        reason_codes.append("empty_safe_content")
    if redaction_applied and not redaction_survived:
        reason_codes.append("redaction_erased_answer")
    if redaction_survived:
        reason_codes.append("redaction_survived")
    if truncated:
        reason_codes.append("safe_content_truncated")
    if degraded:
        reason_codes.append("degraded:" + degraded[0])
    if too_degraded:
        reason_codes.append("too_degraded")

    if not safe or too_degraded or (item_list and not answerable):
        verdict = "FAIL"
    elif not item_list or degraded or truncated:
        verdict = "HOLD"
    else:
        verdict = "PASS"
        reason_codes.append("safe_context_sufficient")

    return {
        "schema": SYNTHETIC_USEFULNESS_RUBRIC_VERSION,
        "verdict": verdict,
        "answerable": answerable,
        "safe": safe,
        "too_degraded": too_degraded,
        "redaction_survived": redaction_survived,
        "item_count": len(item_list),
        "degraded_reason_count": len(degraded),
        "reason_codes": reason_codes,
    }


@runtime_checkable
class SourceCardAdapter(Protocol):
    """Adapter for sanitized metadata cards only; no discovery or raw reads."""

    @property
    def adapter_name(self) -> str:
        """Report-safe adapter label."""
        ...

    def source_cards(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        """Return report-safe source cards for already-known synthetic/source metadata."""
        ...


SAFE_DOGFOOD_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "id": "safe-dogfood-project-boundary",
        "scope": "context",
        "include_family": "project",
        "source_tier": "synthetic_fixture",
        "backend": "synthetic_safe_content",
        "retrieval_backend": "metadata_only",
        "canonicality": "safe_fixture",
        "private_class": "reportable_synthetic",
        "title": "Memory Seam project boundary",
        "snippet": (
            "Memory Seam v0.1.0 is public source, no-live/read-only, and holds service starts, "
            "Runtime Registry consumption, unsupervised reads, writes, custody, and reindexing."
        ),
        "redaction_applied": False,
        "redaction_labels": [],
        "truncated": False,
    },
    {
        "id": "safe-dogfood-runtime-answer",
        "scope": "wiki",
        "include_family": "memory",
        "source_tier": "synthetic_fixture",
        "backend": "synthetic_safe_content",
        "retrieval_backend": "metadata_only",
        "canonicality": "safe_fixture",
        "private_class": "reportable_synthetic",
        "title": "Default-off runtime answer",
        "snippet": (
            "The L3 runtime is an in-process skeleton: enabled defaults false, identity "
            "verification is explicit, audits are metadata-only return values, and rollback "
            "can disable the runtime without widening read authority."
        ),
        "redaction_applied": False,
        "redaction_labels": [],
        "truncated": False,
    },
)

SAFE_SOURCE_CARDS: tuple[SourceCard, ...] = (
    SourceCard(
        card_id="source-card-project-boundary",
        include_family="project",
        source_tier="synthetic_fixture",
        private_class="reportable_synthetic",
        canonicality="safe_fixture",
        retrieval_backend="metadata_only",
        title="Memory Seam project boundary card",
        safe_summary="Synthetic no-live/read-only boundary is reportable from committed synthetic metadata.",
    ),
    SourceCard(
        card_id="source-card-runtime-answer",
        include_family="memory",
        source_tier="synthetic_fixture",
        private_class="reportable_synthetic",
        canonicality="safe_fixture",
        retrieval_backend="metadata_only",
        title="Default-off runtime card",
        safe_summary="Runtime proof is metadata-only: disabled by default, identity-gated, and rollback-safe.",
    ),
)


@runtime_checkable
class SourceAdapter(Protocol):
    """Read-only adapter protocol for safe content fixtures or downstream bridges."""

    @property
    def adapter_name(self) -> str:
        """Report-safe adapter label."""
        ...

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        """Return report-safe context items; no raw/private fallback allowed."""
        ...

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        """Return report-safe recall items; no raw/private fallback allowed."""
        ...


@dataclass(frozen=True)
class SyntheticSafeContentAdapter:
    """Static dogfood adapter backed only by committed safe fixture strings."""

    adapter_name: str = "synthetic-safe-content"
    items: tuple[dict[str, Any], ...] = SAFE_DOGFOOD_ITEMS

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        requested = {name for name in include if name}
        if not requested:
            requested = {"project", "memory"}
        return [dict(item) for item in self.items if item.get("include_family") in requested]

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        allowed_scopes = {"wiki", "diary", "context"} if scope == "all" else {scope}
        candidates = []
        for item in self.items:
            item_scope = str(item.get("scope") or "context")
            if item_scope not in allowed_scopes and scope != "all":
                continue
            candidates.append(dict(item))
        ranked = rank_synthetic_recall_items(candidates, query, n=n)
        return [
            {key: value for key, value in item.items() if not str(key).startswith("ranking_") and key != "source_order"}
            for item in ranked["items"]
        ]


@dataclass(frozen=True)
class SyntheticSourceCardAdapter:
    """Static source-card adapter backed only by sanitized metadata fixtures."""

    adapter_name: str = "synthetic-source-card"
    cards: tuple[SourceCard, ...] = SAFE_SOURCE_CARDS

    def source_cards(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        requested = {name for name in include if name}
        if not requested:
            requested = {"project", "memory"}
        return [card.to_safe_detail() for card in self.cards if card.include_family in requested]


@dataclass(frozen=True)
class AdapterMemorySeamProvider:
    """Memory Seam provider wrapper for a read-only SourceAdapter."""

    adapter: SourceAdapter
    source_card_adapter: SourceCardAdapter | None = None
    provider_name: str = "adapter-safe-content"

    def health(self) -> dict[str, Any]:
        return {
            "ok": True,
            "provider": self.provider_name,
            "adapter": self.adapter.adapter_name,
            "source_card_adapter": None if self.source_card_adapter is None else self.source_card_adapter.adapter_name,
            "contract_status": CONTRACT_STATUS,
            "dogfood_usefulness_status": DOGFOOD_USEFULNESS_STATUS,
            "source_card_adapter_status": SAFE_SOURCE_CARD_ADAPTER_STATUS,
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "raw_fallback_used": False,
            "write_custody_or_reindex": False,
        }

    def context(
        self,
        *,
        include: list[str],
        mode: str,
        agent: str | None,
        token_subject: str | None,
        allowed_scopes: Iterable[str] | None,
        acting_for: str | None,
        timeout_ms: int,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
        include_read_receipt: bool = False,
    ) -> dict[str, Any]:
        items = self.adapter.context_items(include=include, token_subject=token_subject)
        source_cards = self._source_cards(include=include, token_subject=token_subject)
        return self._envelope(
            endpoint="context",
            items=items,
            source_cards=source_cards,
            timeout_ms=timeout_ms,
            include_requested=list(include),
            include_effective=sorted({str(item.get("include_family")) for item in items}),
            mode=mode,
            agent=agent,
            token_subject=token_subject,
            allowed_scopes=allowed_scopes,
            acting_for=acting_for,
            read_receipt_requested=include_read_receipt,
        )

    def recall(
        self,
        query: str,
        *,
        scope: str,
        agent: str | None,
        token_subject: str | None,
        allowed_scopes: Iterable[str] | None,
        acting_for: str | None,
        n: int,
        timeout_ms: int,
        context_sources: Any = None,
        context_source_allowlist: Any = None,
        include_read_receipt: bool = False,
    ) -> dict[str, Any]:
        items = self.adapter.recall_items(query, scope=scope, token_subject=token_subject, n=n)
        return self._envelope(
            endpoint="recall",
            items=items,
            timeout_ms=timeout_ms,
            query=query,
            scope_requested=scope,
            scope_effective=sorted({str(item.get("scope")) for item in items}),
            agent=agent,
            token_subject=token_subject,
            allowed_scopes=allowed_scopes,
            acting_for=acting_for,
            read_receipt_requested=include_read_receipt,
            n=n,
        )

    def _envelope(self, *, endpoint: str, items: list[dict[str, Any]], timeout_ms: int, **extra: Any) -> dict[str, Any]:
        adapter_metadata = self._adapter_metadata()
        degraded_reasons = _envelope_degraded_reasons(items, adapter_metadata)
        read_backend_called = self.adapter.adapter_name in LOCAL_READ_ADAPTER_NAMES and bool(items)
        body = {
            "endpoint": endpoint,
            "provider": self.provider_name,
            "adapter": self.adapter.adapter_name,
            "source_card_adapter": None if self.source_card_adapter is None else self.source_card_adapter.adapter_name,
            "contract_status": CONTRACT_STATUS,
            "dogfood_usefulness_status": DOGFOOD_USEFULNESS_STATUS,
            "source_card_adapter_status": SAFE_SOURCE_CARD_ADAPTER_STATUS,
            "items": items,
            "partial": False,
            "degraded": bool(degraded_reasons),
            "degraded_reasons": degraded_reasons,
            "backend_latency_ms": 0,
            "timeout_ms": timeout_ms,
            "read_backend_called": read_backend_called,
            "live_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "raw_fallback_used": False,
            "write_custody_or_reindex": False,
            **adapter_metadata,
            **extra,
        }
        if endpoint == "recall":
            body["limits"] = dict(RECALL_LIMITS)
        if endpoint in {"context", "recall"} and not items:
            diagnostics = _zero_item_diagnostics(
                endpoint=endpoint,
                query=str(extra.get("query") or ""),
                adapter_name=self.adapter.adapter_name,
                adapter_metadata=adapter_metadata,
            )
            body["recall_diagnostics"] = diagnostics
            body.setdefault("reason", diagnostics["zero_reason"])
        return body

    def _adapter_metadata(self) -> dict[str, Any]:
        metadata: dict[str, Any] = {}
        protocol_version = getattr(self.adapter, "adapter_protocol_version", None)
        if protocol_version is not None:
            metadata["adapter_protocol_version"] = protocol_version

        scan_summary = getattr(self.adapter, "last_scan_summary", None)
        if callable(scan_summary):
            scan_summary = scan_summary()
        if isinstance(scan_summary, dict):
            metadata["adapter_scan_summary"] = dict(scan_summary)
            reason = scan_summary.get("reason")
            if isinstance(reason, str) and reason:
                metadata["reason"] = reason

        empty_reason = getattr(self.adapter, "last_empty_reason", None)
        if isinstance(empty_reason, str) and empty_reason:
            metadata["reason"] = empty_reason
        return metadata

    def _source_cards(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        if self.source_card_adapter is None:
            return []
        cards = self.source_card_adapter.source_cards(include=include, token_subject=token_subject)
        for card in cards:
            assert_source_card_is_report_safe(card)
        return cards


def synthetic_safe_content_provider() -> MemorySeamProvider:
    """Return a no-live provider useful enough to answer synthetic operator questions."""

    return AdapterMemorySeamProvider(SyntheticSafeContentAdapter(), SyntheticSourceCardAdapter())


def _envelope_degraded_reasons(items: list[dict[str, Any]], adapter_metadata: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    summary = adapter_metadata.get("adapter_scan_summary")
    if isinstance(summary, dict) and bool(summary.get("truncated")):
        reasons.append("scan_truncated")
    if isinstance(summary, dict) and int(summary.get("files_with_record_cap") or 0) > 0:
        reasons.append("scan_truncated")
    for item in items:
        item_reasons = item.get("degraded_reasons") or []
        if "utf8_replacement" in item_reasons:
            reasons.append("utf8_replacement")
        if item.get("truncated") or item.get("degraded_reason") in SCAN_TRUNCATED_ITEM_REASONS:
            reasons.append("scan_truncated")
    return _dedupe(reasons)


def _zero_item_diagnostics(
    *,
    endpoint: str,
    query: str,
    adapter_name: str,
    adapter_metadata: dict[str, Any],
) -> dict[str, Any]:
    summary = adapter_metadata.get("adapter_scan_summary")
    summary = summary if isinstance(summary, dict) else {}
    zero_reason = str(adapter_metadata.get("reason") or summary.get("reason") or "")
    if not zero_reason or zero_reason == "None":
        zero_reason = "zero_match" if endpoint == "recall" else "zero_context"
    files_scanned = _summary_int(summary, "files_scanned", fallback_key="rows_scanned")
    files_skipped = _summary_int(summary, "files_skipped")
    return {
        "zero_reason": zero_reason,
        "files_scanned": files_scanned,
        "files_skipped": files_skipped,
        "truncated": bool(summary.get("truncated")),
        "suggestion": _zero_item_suggestion(
            zero_reason=zero_reason,
            adapter_name=adapter_name,
            files_scanned=files_scanned,
            files_skipped=files_skipped,
            query=query,
        ),
    }


def _summary_int(summary: dict[str, Any], key: str, *, fallback_key: str | None = None) -> int:
    value = summary.get(key)
    if value is None and fallback_key is not None:
        value = summary.get(fallback_key)
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _zero_item_suggestion(
    *,
    zero_reason: str,
    adapter_name: str,
    files_scanned: int,
    files_skipped: int,
    query: str,
) -> str:
    if zero_reason == "zero_match":
        return f"zero-match: scanned {files_scanned} files, none matched {query!r}"
    if zero_reason == "empty_query":
        return "empty-query: provide at least one letter or number to recall"
    if zero_reason == "zero_markdown_files":
        if files_scanned == 0 and files_skipped:
            return "wrong adapter? try --adapter plaintext"
        return "add markdown files or try --adapter plaintext"
    if zero_reason == "zero_plaintext_files":
        return "try --adapter markdown, jsonl, or git-tree if this root is not plain text"
    if zero_reason == "zero_json_export_files":
        return "try --adapter markdown or plaintext for non-export folders"
    if zero_reason in {"zero_git_text_files", "not_a_git_repository"}:
        return "try --adapter plaintext or markdown for non-Git folders"
    if zero_reason in {"zero_rows", "missing_table", "missing_column"}:
        return "check the copied SQLite table and column mapping"
    if adapter_name == "local-sqlite-notes":
        return "check SQLite adapter configuration"
    return "check adapter selection, root, and query"


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


__all__ = [
    "ADAPTER_PROTOCOL_VERSION",
    "AdapterMemorySeamProvider",
    "DOGFOOD_USEFULNESS_STATUS",
    "FORBIDDEN_SOURCE_CARD_FRAGMENTS",
    "SAFE_DOGFOOD_ITEMS",
    "SAFE_SOURCE_CARD_ADAPTER_STATUS",
    "SAFE_SOURCE_CARDS",
    "RECALL_LIMITS",
    "SYNTHETIC_RECALL_RANKING_FIXTURE_VERSION",
    "SYNTHETIC_USEFULNESS_RUBRIC_VERSION",
    "SourceAdapter",
    "SourceCard",
    "SourceCardAdapter",
    "SyntheticSafeContentAdapter",
    "SyntheticSourceCardAdapter",
    "assert_source_card_is_report_safe",
    "rank_synthetic_recall_items",
    "score_synthetic_usefulness",
    "synthetic_safe_content_provider",
]
