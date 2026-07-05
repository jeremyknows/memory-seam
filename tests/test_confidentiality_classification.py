"""Portable fail-closed confidentiality classification tests."""

from __future__ import annotations

import memory_seam
from memory_seam.confidentiality_classification import (
    CLASSIFICATION_ALLOWED,
    CLASSIFICATION_WITHHELD,
    classify_confidentiality,
)


def test_classifier_withholds_empty_unknown_and_secret_like_text_by_default() -> None:
    synthetic_token = "sk-" + "test_12345678901234567890"
    for text in ("", "VF pricing partner packet", "op://Shared/secret/token", synthetic_token):
        verdict = classify_confidentiality(text=text, positive_clean_signal=False)
        assert verdict.decision == CLASSIFICATION_WITHHELD
        assert verdict.reason_code == "classification_uncertain"
        assert verdict.public_reportable_allowed is False
        assert verdict.body_promotion_allowed is False


def test_classifier_denies_raw_session_markers() -> None:
    verdict = classify_confidentiality(text="raw session transcript body", positive_clean_signal=True)
    assert verdict.decision == CLASSIFICATION_WITHHELD
    assert verdict.reason_code == "raw_session_in_indexed_root"
    assert verdict.private_class == "archivist_raw_session"


def test_classifier_requires_positive_clean_signal_to_allow() -> None:
    verdict = classify_confidentiality(
        text="sanitized sourced summary with no private body",
        positive_clean_signal=True,
    )
    assert verdict.decision == CLASSIFICATION_ALLOWED
    assert verdict.reason_code == "classification_passed"
    assert verdict.private_class == "wiki_safe_summary"
    assert verdict.public_reportable_allowed is True
    assert verdict.body_promotion_allowed is True


def test_classifier_is_exported_from_package() -> None:
    assert memory_seam.classify_confidentiality(text="", positive_clean_signal=False).decision == CLASSIFICATION_WITHHELD
