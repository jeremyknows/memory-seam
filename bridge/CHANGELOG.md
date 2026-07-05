# Changelog

## [Unreleased]

- Initial Memory Seam MCP stdio bridge package.
- Consolidated bridge packaging under `memory-seam/bridge` for install via
  `git+https://github.com/jeremyknows/memory-seam.git#subdirectory=bridge`.
- Added bridge/core compatibility metadata and startup version-skew checks.
- Changed bridge/core compatibility checks to fail closed for any installed core
  version outside the declared range unless
  `MEMORY_SEAM_MCP_ALLOW_INCOMPATIBLE=1` is explicitly set.
- Added MCP recall input bounds for query type, query length, term count, and
  `n` validation/clamping before local file scans run.
