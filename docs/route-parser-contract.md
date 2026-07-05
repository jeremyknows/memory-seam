# Route parser contract

Memory Seam's portable router is a no-live in-process helper, not a service listener. It accepts synthetic/local calls for `GET /health`, `GET /context`, and `GET /recall` only. Write-like routes remain unavailable and must be denied before any read handler is called.

## Query parsing rules

- Repeated query parameters use the first value returned by `urllib.parse.parse_qs`.
- Blank or missing `include` values become an empty include list.
- `include` is comma-separated and trims whitespace around non-empty entries.
- Blank or missing `mode` defaults to `startup` for `/context`.
- Blank or missing `scope` defaults to `wiki` for `/recall`.
- Blank or missing `query` defaults to an empty string for `/recall`.
- Blank or missing integer parameters use their endpoint defaults.
- `timeout_ms` is clamped to the committed `MIN_TIMEOUT_MS`/`MAX_TIMEOUT_MS` contract bounds.
- Invalid integer parameters return `400 bad_request` rather than falling through to a handler.

## Method and path rules

- Unknown paths return `404 route_not_found` before handlers run.
- Known read paths with non-`GET` methods return `405 method_not_allowed` before handlers run.
- Explicit write-like route/method pairs from `WRITE_LIKE_ROUTES` return `405 write_like_route_unavailable` before handlers run.
- Successful read routes return JSON envelopes with status code `200` and `content-type: application/json`.

These rules are covered by `tests/test_route_parser_edge_cases.py` so downstream bridge adapters can depend on deterministic no-live behavior without probing live sources, starting services, or adding write custody paths.
