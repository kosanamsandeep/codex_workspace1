from __future__ import annotations

from pathlib import Path

from src.cli.app import run


def test_cli_flow(tmp_path: Path) -> None:
    store = tmp_path / "store.json"

    exit_code = run(["--store", str(store), "add-course", "Algorithms"])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "list-courses"])
    assert exit_code == 0
