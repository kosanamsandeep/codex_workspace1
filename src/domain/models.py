from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime

from .errors import DomainValidationError
from .value_objects import CourseId, DurationMinutes, SessionId, TopicId


@dataclass(frozen=True)
class Course:
    course_id: CourseId
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise DomainValidationError("course name cannot be empty")


@dataclass(frozen=True)
class Topic:
    topic_id: TopicId
    course_id: CourseId
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise DomainValidationError("topic name cannot be empty")


@dataclass(frozen=True)
class StudySession:
    session_id: SessionId
    topic_id: TopicId
    scheduled_date: date
    duration: DurationMinutes
    completed: bool = False
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.completed and self.completed_at is None:
            raise DomainValidationError("completed sessions must have completed_at")
        if not self.completed and self.completed_at is not None:
            raise DomainValidationError("completed_at requires completed=True")

    def complete(self, completed_at: datetime | None = None) -> "StudySession":
        if completed_at is None:
            completed_at = datetime.utcnow()
        return replace(self, completed=True, completed_at=completed_at)

