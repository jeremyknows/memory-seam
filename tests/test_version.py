from __future__ import annotations

import memory_seam


def test_package_exports_version():
    assert memory_seam.__version__ == "0.1.0"
    assert "__version__" in memory_seam.__all__
