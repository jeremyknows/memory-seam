#!/usr/bin/env python3
"""Smoke-test an installed Memory Seam package without live/private sources."""

from __future__ import annotations

from importlib import metadata

from memory_seam import NullMemorySeamProvider, provider_handlers, read_receipt_enabled, route_request


def main() -> int:
    package_version = metadata.version("memory-seam")
    provider = NullMemorySeamProvider()
    response = route_request(
        "GET",
        "/context?include=project&agent=sax&read_receipt=metadata_only",
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context"],
    )

    if package_version != "0.1.0":
        raise SystemExit(f"unexpected package version: {package_version}")
    if response["status_code"] != 200:
        raise SystemExit(f"unexpected status code: {response['status_code']}")

    body = response["body"]
    if body["items"]:
        raise SystemExit("null provider returned items during no-live package smoke")
    if body["read_backend_called"] is not False:
        raise SystemExit("package smoke attempted a read backend call")
    if body["service_started"] is not False:
        raise SystemExit("package smoke started a service")
    if body["runtime_registry_consumed"] is not False:
        raise SystemExit("package smoke consumed Runtime Registry state")
    if body["write_custody_or_reindex"] is not False:
        raise SystemExit("package smoke performed write/custody/reindex behavior")

    print("package import smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
