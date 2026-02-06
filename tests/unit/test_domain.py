from __future__ import annotations

from datetime import date

import pytest

from src.domain import Course, DurationMinutes, StudySession, Topic, new_course_id, new_session_id, new_topic_id
from src.domain.errors import DomainValidationError


def test_duration_must_be_positive() -> None:
    with pytest.raises(DomainValidationError):
        DurationMinutes(0)


def test_course_requires_name() -> None:
    with pytest.raises(DomainValidationError):
        Course(course_id=new_course_id(), name=" ")


def test_topic_requires_name() -> None:
    with pytest.raises(DomainValidationError):
        Topic(topic_id=new_topic_id(), course_id=new_course_id(), name="")


def test_complete_session_sets_completed() -> None:
    session = StudySession(
        session_id=new_session_id(),
        topic_id=new_topic_id(),
        scheduled_date=date(2026, 2, 1),
        duration=DurationMinutes(30),
    )
    completed = session.complete()
    assert completed.completed is True
    assert completed.completed_at is not None
