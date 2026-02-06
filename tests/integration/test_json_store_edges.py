from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.adapters.json_store import JsonFileStore, _to_datetime
from src.domain import CourseId, SessionId, TopicId


def test_to_datetime_none() -> None:
    assert _to_datetime(None) is None


def test_invalid_store_format_raises(tmp_path: Path) -> None:
    store_path = tmp_path / "store.json"
    store_path.write_text(json.dumps({"bad": []}), encoding="utf-8")
    store = JsonFileStore(store_path)
    with pytest.raises(ValueError):
        store._read()


def test_get_returns_none_when_missing(tmp_path: Path) -> None:
    store = JsonFileStore(tmp_path / "store.json")
    courses = store._read()["courses"]
    assert courses == []

    from src.adapters import JsonCourseRepository, JsonSessionRepository, JsonTopicRepository

    course_repo = JsonCourseRepository(store)
    topic_repo = JsonTopicRepository(store)
    session_repo = JsonSessionRepository(store)

    assert course_repo.get(CourseId("missing")) is None
    assert topic_repo.get(TopicId("missing")) is None
    assert session_repo.get(SessionId("missing")) is None
