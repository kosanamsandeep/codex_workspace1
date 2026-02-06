from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Protocol

from src.domain import Course, CourseId, SessionId, StudySession, Topic, TopicId


@dataclass(frozen=True)
class WeeklyReport:
    week_start: date
    total_minutes: int
    minutes_by_course: dict[CourseId, int]
    minutes_by_topic: dict[TopicId, int]


class CourseRepository(Protocol):
    def add(self, course: Course) -> None: ...

    def get(self, course_id: CourseId) -> Course | None: ...

    def list_all(self) -> Iterable[Course]: ...

    def remove(self, course_id: CourseId) -> None: ...


class TopicRepository(Protocol):
    def add(self, topic: Topic) -> None: ...

    def get(self, topic_id: TopicId) -> Topic | None: ...

    def list_by_course(self, course_id: CourseId) -> Iterable[Topic]: ...

    def remove(self, topic_id: TopicId) -> None: ...


class SessionRepository(Protocol):
    def add(self, session: StudySession) -> None: ...

    def get(self, session_id: SessionId) -> StudySession | None: ...

    def list_by_topic(self, topic_id: TopicId) -> Iterable[StudySession]: ...

    def list_all(self) -> Iterable[StudySession]: ...

    def update(self, session: StudySession) -> None: ...
