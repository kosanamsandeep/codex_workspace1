from __future__ import annotations

from datetime import date

import pytest

from src.adapters import (
    InMemoryCourseRepository,
    InMemorySessionRepository,
    InMemoryTopicRepository,
)
from src.application import (
    AddTopicRequest,
    ApplicationValidationError,
    CompleteSessionRequest,
    CreateCourseRequest,
    NotFoundError,
    PlanSessionRequest,
    add_topic,
    complete_session,
    create_course,
    plan_session,
    remove_topic,
)
from src.domain import CourseId, SessionId, TopicId


def test_create_course_rejects_empty_name() -> None:
    courses = InMemoryCourseRepository()
    with pytest.raises(ApplicationValidationError):
        create_course(CreateCourseRequest(name=" "), courses)


def test_add_topic_requires_existing_course() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()
    with pytest.raises(NotFoundError):
        add_topic(AddTopicRequest(course_id=CourseId("missing"), name="X"), courses, topics)


def test_add_topic_rejects_empty_name() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()
    course = create_course(CreateCourseRequest(name="Math"), courses)
    with pytest.raises(ApplicationValidationError):
        add_topic(AddTopicRequest(course_id=course.course_id, name=" "), courses, topics)


def test_plan_session_requires_existing_topic() -> None:
    topics = InMemoryTopicRepository()
    sessions = InMemorySessionRepository()
    with pytest.raises(NotFoundError):
        plan_session(
            PlanSessionRequest(
                topic_id=TopicId("missing"),
                scheduled_date=date(2026, 2, 1),
                duration_minutes=30,
            ),
            topics,
            sessions,
        )


def test_remove_topic_not_found() -> None:
    topics = InMemoryTopicRepository()
    with pytest.raises(NotFoundError):
        remove_topic(TopicId("missing"), topics)


def test_complete_session_not_found() -> None:
    sessions = InMemorySessionRepository()
    with pytest.raises(NotFoundError):
        complete_session(CompleteSessionRequest(session_id=SessionId("missing")), sessions)
