from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_import_convertppt_is_lightweight() -> None:
    code = """
import json
import sys

import convertppt

print(json.dumps({
    "has_convert_file": hasattr(convertppt, "convert_file"),
    "loaded_modules": sorted(
        name for name in ("cv2", "paddle", "paddleocr", "pdf2image", "tkinter")
        if name in sys.modules
    ),
}))
"""
    result = run_python(code)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload["has_convert_file"] is True
    assert payload["loaded_modules"] == []


def test_build_output_path_matches_existing_suffix() -> None:
    code = """
from convertppt import build_output_path

print(build_output_path("deck.pptx"))
"""
    result = run_python(code)

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "deck_AI_REPAIRED.pptx"
