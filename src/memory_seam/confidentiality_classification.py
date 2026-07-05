"""Portable fail-closed confidentiality classification primitives.

This module is source-agnostic portable core. It does not know deployment-specific
confidential lines, read files, inspect credentials, or grant activation. Adapters pass a
positive clean signal only after their custody-specific checks have completed;
without that signal the portable default is withheld/uncertain.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

CLASSIFICATION_ALLOWED = "allow"
CLASSIFICATION_WITHHELD = "withhold"
CONFIDENTIALITY_CLASSIFICATION_ALLOWED = CLASSIFICATION_ALLOWED
CONFIDENTIALITY_CLASSIFICATION_WITHHELD = CLASSIFICATION_WITHHELD

RAW_SESSION_MARKERS = (
    re.compile(r"\braw[-_ ]?session\b", re.IGNORECASE),
    re.compile(r"\barchivist_raw_session\b", re.IGNORECASE),
    re.compile(
        r"^\s*(?:private_class|operation_class)\s*:\s*['\"]?archivist_raw_session['\"]?\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
)
CONFIDENTIALITY_RAW_SESSION_MARKERS = RAW_SESSION_MARKERS


@dataclass(frozen=True)
class ConfidentialityClassificationVerdict:
    decision: str
    reason_code: str
    private_class: str
    deny_before_sink: bool
    public_reportable_allowed: bool
    body_promotion_allowed: bool
    matched_markers: tuple[str, ...] = ()


def classify_confidentiality(*, text: str, positive_clean_signal: bool = False) -> ConfidentialityClassificationVerdict:
    """Classify content with fail-closed terminal semantics.

    ``positive_clean_signal`` is the only path to ``allow``. The absence of known
    bad markers is not evidence of cleanliness; empty, unknown-origin, token-like,
    or partner-sensitive content all stay withheld until an adapter supplies a
    positive clean signal from its own custody review.
    """

    markers = tuple(rx.pattern for rx in RAW_SESSION_MARKERS if rx.search(text or ""))
    if markers:
        return ConfidentialityClassificationVerdict(
            decision=CLASSIFICATION_WITHHELD,
            reason_code="raw_session_in_indexed_root",
            private_class="archivist_raw_session",
            deny_before_sink=True,
            public_reportable_allowed=False,
            body_promotion_allowed=False,
            matched_markers=markers,
        )
    if not positive_clean_signal:
        return ConfidentialityClassificationVerdict(
            decision=CLASSIFICATION_WITHHELD,
            reason_code="classification_uncertain",
            private_class="classification_uncertain",
            deny_before_sink=True,
            public_reportable_allowed=False,
            body_promotion_allowed=False,
            matched_markers=(),
        )
    return ConfidentialityClassificationVerdict(
        decision=CLASSIFICATION_ALLOWED,
        reason_code="classification_passed",
        private_class="wiki_safe_summary",
        deny_before_sink=False,
        public_reportable_allowed=True,
        body_promotion_allowed=True,
        matched_markers=(),
    )
