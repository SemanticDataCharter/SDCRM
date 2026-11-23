"""Fixtures for the composition-model test suite.

The `model` fixture runs the REAL generator into a temp file and loads it, so the
suite tests the generator (the thing we change), not a stale committed artifact.
"""
import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATOR = os.path.join(ROOT, "generate_composition.py")
COMMITTED_JSON = os.path.join(ROOT, "composition-model.json")


@pytest.fixture(scope="session")
def model(tmp_path_factory):
    """Freshly generated composition-model.json, as a dict."""
    out = tmp_path_factory.mktemp("composition") / "composition-model.json"
    subprocess.run([sys.executable, GENERATOR, "--out", str(out)],
                   check=True, cwd=ROOT)
    with open(out, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="session")
def committed():
    """The committed composition-model.json, as a dict."""
    with open(COMMITTED_JSON, encoding="utf-8") as fh:
        return json.load(fh)
