from __future__ import annotations

from memory_seam.custody_receipts import (
    L6_CUSTODY_RECEIPT_ALLOWED_SHAPES,
    L6_CUSTODY_RECEIPT_HELD_SURFACES,
    L6_CUSTODY_RECEIPT_NOOP_FIXTURES,
    L6_CUSTODY_RECEIPT_REQUIRED_FIELDS,
    L6_CUSTODY_RECEIPT_STATUS,
    build_l6_custody_receipt_noop_fixtures,
    validate_l6_custody_receipt_noop_fixture,
)


PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "private-correlation-ref",
)


class SideEffectSpies:
    def __init__(self) -> None:
        self.write_callbacks = 0
        self.custody_callbacks = 0
        self.reindex_callbacks = 0
        self.rollback_callbacks = 0
        self.provider_calls = 0
        self.backend_calls = 0
        self.source_stat_calls = 0
        self.source_read_calls = 0

    def counters(self) -> dict[str, int | bool]:
        return {
            "write_custody_or_reindex": False,
            "write_callbacks": self.write_callbacks,
            "custody_callbacks": self.custody_callbacks,
            "reindex_callbacks": self.reindex_callbacks,
            "rollback_callbacks": self.rollback_callbacks,
            "provider_calls": self.provider_calls,
            "backend_calls": self.backend_calls,
            "source_stat_calls": self.source_stat_calls,
            "source_read_calls": self.source_read_calls,
        }


def test_custody_receipt_schema_is_noop_and_implementation_held():
    fixtures = build_l6_custody_receipt_noop_fixtures()

    assert L6_CUSTODY_RECEIPT_STATUS == "noop_fixture_implementation_held"
    assert {receipt["shape"] for receipt in fixtures} == set(L6_CUSTODY_RECEIPT_ALLOWED_SHAPES)
    for receipt in fixtures:
        assert set(L6_CUSTODY_RECEIPT_REQUIRED_FIELDS).issubset(receipt)
        assert receipt["status"] == "noop_fixture_implementation_held"
        assert tuple(receipt["held_surfaces"]) == L6_CUSTODY_RECEIPT_HELD_SURFACES
        assert "write_execution" in receipt["held_surfaces"]
        assert "custody_transfer" in receipt["held_surfaces"]
        assert "reindex_execution" in receipt["held_surfaces"]
        assert validate_l6_custody_receipt_noop_fixture(receipt) == []


def test_fixtures_cover_required_decision_shapes_without_performing_writes():
    spies = SideEffectSpies()
    receipts = build_l6_custody_receipt_noop_fixtures()

    assert [receipt["shape"] for receipt in receipts] == [
        "requested",
        "denied_before_write",
        "held_for_approval",
        "rollback_required",
    ]
    assert {receipt["approval_state"] for receipt in receipts} == {
        "not_approved",
        "denied",
        "held_for_jeremy_approval",
        "implementation_held",
    }
    assert any(receipt["rollback_state"] == "rollback_required_but_not_executed" for receipt in receipts)
    for receipt in receipts:
        assert receipt["side_effects"] == spies.counters()
    assert spies.counters() == {
        "write_custody_or_reindex": False,
        "write_callbacks": 0,
        "custody_callbacks": 0,
        "reindex_callbacks": 0,
        "rollback_callbacks": 0,
        "provider_calls": 0,
        "backend_calls": 0,
        "source_stat_calls": 0,
        "source_read_calls": 0,
    }


def test_receipts_are_report_safe_and_do_not_echo_private_payload_material():
    receipts = build_l6_custody_receipt_noop_fixtures()
    rendered = repr(receipts)

    for marker in PRIVATE_MARKERS:
        assert marker not in rendered
    for receipt in receipts:
        assert receipt["report_safety"] == {
            "raw_private_text": False,
            "credentials_or_auth_material": False,
            "private_paths": False,
            "platform_ids": False,
            "raw_query_or_payload": False,
            "private_correlation_refs": False,
        }
        assert "raw" not in receipt["safe_payload_class"]
        assert "path" not in receipt["safe_payload_class"]


def test_builder_returns_copies_so_fixture_contract_stays_stable():
    receipts = build_l6_custody_receipt_noop_fixtures()
    receipts[0]["side_effects"]["write_callbacks"] = 1
    receipts[0]["report_safety"]["credentials_or_auth_material"] = True

    fresh_receipts = build_l6_custody_receipt_noop_fixtures()

    assert fresh_receipts[0]["side_effects"]["write_callbacks"] == 0
    assert fresh_receipts[0]["report_safety"]["credentials_or_auth_material"] is False
    assert L6_CUSTODY_RECEIPT_NOOP_FIXTURES[0]["side_effects"]["write_callbacks"] == 0


def test_validator_rejects_side_effect_or_report_safety_regression_safely():
    receipt = build_l6_custody_receipt_noop_fixtures()[0]
    receipt["side_effects"]["provider_calls"] = 1
    receipt["report_safety"]["raw_query_or_payload"] = True
    receipt["held_surfaces"] = tuple(surface for surface in receipt["held_surfaces"] if surface != "write_execution")

    errors = validate_l6_custody_receipt_noop_fixture(receipt)

    assert "nonzero_side_effect_counter" in errors
    assert "unsafe_report_safety_flag" in errors
    assert "missing_held_surface_write_execution" in errors
    assert repr(errors) == "['nonzero_side_effect_counter', 'unsafe_report_safety_flag', 'missing_held_surface_write_execution']"
