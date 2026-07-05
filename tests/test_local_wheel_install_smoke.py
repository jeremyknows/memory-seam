import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_local_wheel_install_smoke_script_passes_from_checkout():
    subprocess.run([sys.executable, "scripts/local_wheel_install_smoke.py"], cwd=REPO_ROOT, check=True)


def test_local_wheel_install_smoke_is_documented():
    script = REPO_ROOT / "scripts" / "local_wheel_install_smoke.py"
    docs = (REPO_ROOT / "docs" / "packaging.md").read_text()

    assert script.exists()
    assert "python scripts/local_wheel_install_smoke.py" in docs


def test_local_wheel_install_smoke_keeps_no_live_boundary():
    text = (REPO_ROOT / "scripts" / "local_wheel_install_smoke.py").read_text()

    assert "--no-index" in text
    assert "package_import_smoke.py" in text
    assert "Runtime Registry" in text
    assert "twine" not in text
    assert "upload" not in text.lower()
