from __future__ import annotations

from dataclasses import dataclass
from typing import NewType
from uuid import uuid4

from .errors import DomainValidationError

CourseId = NewType("CourseId", str)
TopicId = NewType("TopicId", str)
SessionId = NewType("SessionId", str)


def new_course_id() -> CourseId:
    return CourseId(str(uuid4()))


def new_topic_id() -> TopicId:
    return TopicId(str(uuid4()))


def new_session_id() -> SessionId:
    return SessionId(str(uuid4()))


@dataclass(frozen=True)
class DurationMinutes:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise DomainValidationError("duration must be positive minutes")

