from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from src.application import CourseRepository, SessionRepository, TopicRepository
from src.domain import (
    Course,
    CourseId,
    DurationMinutes,
    SessionId,
    StudySession,
    Topic,
    TopicId,
)


def _to_date(value: str) -> date:
    return date.fromisoformat(value)


def _to_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


class JsonFileStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write({"courses": [], "topics": [], "sessions": []})

    def _read(self) -> dict[str, list[dict]]:
        data = json.loads(self._path.read_text(encoding="utf-8"))
        if not {"courses", "topics", "sessions"} <= data.keys():
            raise ValueError("invalid store format")
        return data

    def _write(self, data: dict[str, list[dict]]) -> None:
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class JsonCourseRepository(CourseRepository):
    def __init__(self, store: JsonFileStore) -> None:
        self._store = store

    def add(self, course: Course) -> None:
        data = self._store._read()
        data["courses"].append({"course_id": course.course_id, "name": course.name})
        self._store._write(data)

    def get(self, course_id: CourseId) -> Course | None:
        data = self._store._read()
        for item in data["courses"]:
            if item["course_id"] == course_id:
                return Course(course_id=CourseId(item["course_id"]), name=item["name"])
        return None

    def list_all(self) -> Iterable[Course]:
        data = self._store._read()
        return [
            Course(course_id=CourseId(item["course_id"]), name=item["name"])
            for item in data["courses"]
        ]

    def remove(self, course_id: CourseId) -> None:
        data = self._store._read()
        data["courses"] = [
            item for item in data["courses"] if item["course_id"] != course_id
        ]
        self._store._write(data)


class JsonTopicRepository(TopicRepository):
    def __init__(self, store: JsonFileStore) -> None:
        self._store = store

    def add(self, topic: Topic) -> None:
        data = self._store._read()
        data["topics"].append(
            {
                "topic_id": topic.topic_id,
                "course_id": topic.course_id,
                "name": topic.name,
            }
        )
        self._store._write(data)

    def get(self, topic_id: TopicId) -> Topic | None:
        data = self._store._read()
        for item in data["topics"]:
            if item["topic_id"] == topic_id:
                return Topic(
                    topic_id=TopicId(item["topic_id"]),
                    course_id=CourseId(item["course_id"]),
                    name=item["name"],
                )
        return None

    def list_by_course(self, course_id: CourseId) -> Iterable[Topic]:
        data = self._store._read()
        return [
            Topic(
                topic_id=TopicId(item["topic_id"]),
                course_id=CourseId(item["course_id"]),
                name=item["name"],
            )
            for item in data["topics"]
            if item["course_id"] == course_id
        ]

    def remove(self, topic_id: TopicId) -> None:
        data = self._store._read()
        data["topics"] = [
            item for item in data["topics"] if item["topic_id"] != topic_id
        ]
        self._store._write(data)


class JsonSessionRepository(SessionRepository):
    def __init__(self, store: JsonFileStore) -> None:
        self._store = store

    def add(self, session: StudySession) -> None:
        data = self._store._read()
        data["sessions"].append(
            {
                "session_id": session.session_id,
                "topic_id": session.topic_id,
                "scheduled_date": session.scheduled_date.isoformat(),
                "duration_minutes": session.duration.value,
                "completed": session.completed,
                "completed_at": session.completed_at.isoformat()
                if session.completed_at
                else None,
            }
        )
        self._store._write(data)

    def get(self, session_id: SessionId) -> StudySession | None:
        data = self._store._read()
        for item in data["sessions"]:
            if item["session_id"] == session_id:
                return StudySession(
                    session_id=SessionId(item["session_id"]),
                    topic_id=TopicId(item["topic_id"]),
                    scheduled_date=_to_date(item["scheduled_date"]),
                    duration=DurationMinutes(item["duration_minutes"]),
                    completed=item["completed"],
                    completed_at=_to_datetime(item["completed_at"]),
                )
        return None

    def list_by_topic(self, topic_id: TopicId) -> Iterable[StudySession]:
        data = self._store._read()
        return [
            StudySession(
                session_id=SessionId(item["session_id"]),
                topic_id=TopicId(item["topic_id"]),
                scheduled_date=_to_date(item["scheduled_date"]),
                duration=DurationMinutes(item["duration_minutes"]),
                completed=item["completed"],
                completed_at=_to_datetime(item["completed_at"]),
            )
            for item in data["sessions"]
            if item["topic_id"] == topic_id
        ]

    def list_all(self) -> Iterable[StudySession]:
        data = self._store._read()
        return [
            StudySession(
                session_id=SessionId(item["session_id"]),
                topic_id=TopicId(item["topic_id"]),
                scheduled_date=_to_date(item["scheduled_date"]),
                duration=DurationMinutes(item["duration_minutes"]),
                completed=item["completed"],
                completed_at=_to_datetime(item["completed_at"]),
            )
            for item in data["sessions"]
        ]

    def update(self, session: StudySession) -> None:
        data = self._store._read()
        updated = []
        for item in data["sessions"]:
            if item["session_id"] == session.session_id:
                updated.append(
                    {
                        "session_id": session.session_id,
                        "topic_id": session.topic_id,
                        "scheduled_date": session.scheduled_date.isoformat(),
                        "duration_minutes": session.duration.value,
                        "completed": session.completed,
                        "completed_at": session.completed_at.isoformat()
                        if session.completed_at
                        else None,
                    }
                )
            else:
                updated.append(item)
        data["sessions"] = updated
        self._store._write(data)
