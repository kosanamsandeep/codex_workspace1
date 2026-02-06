from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from src.cli.app import run


def test_cli_flow(tmp_path: Path) -> None:
    store = tmp_path / "store.json"

    exit_code = run(["--store", str(store), "add-course", "Algorithms"])
    assert exit_code == 0

    data = json.loads(store.read_text(encoding="utf-8"))
    course_id = data["courses"][0]["course_id"]

    exit_code = run(["--store", str(store), "add-topic", course_id, "Graphs"])
    assert exit_code == 0

    data = json.loads(store.read_text(encoding="utf-8"))
    topic_id = data["topics"][0]["topic_id"]

    monday = date(2026, 2, 3)
    monday = monday - timedelta(days=monday.weekday())
    exit_code = run(
        [
            "--store",
            str(store),
            "plan-session",
            topic_id,
            monday.isoformat(),
            "30",
        ]
    )
    assert exit_code == 0

    data = json.loads(store.read_text(encoding="utf-8"))
    session_id = data["sessions"][0]["session_id"]

    exit_code = run(
        [
            "--store",
            str(store),
            "complete-session",
            session_id,
            "--completed-at",
            "2026-02-03T10:00:00",
        ]
    )
    assert exit_code == 0

    exit_code = run(["--store", str(store), "list-courses"])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "list-topics", course_id])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "remove-topic", topic_id])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "delete-course", course_id])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "delete-course", course_id])
    assert exit_code == 1

    exit_code = run(["--store", str(store), "list-sessions"])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "weekly-report", monday.isoformat()])
    assert exit_code == 0

    exit_code = run(["--store", str(store), "delete-course", "missing"])
    assert exit_code == 1
