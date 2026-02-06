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
    PlanSessionRequest,
    WeeklyReportRequest,
    add_topic,
    complete_session,
    create_course,
    generate_weekly_report,
    list_courses,
    list_sessions,
    list_topics,
    plan_session,
)


def test_create_and_list_course() -> None:
    courses = InMemoryCourseRepository()
    created = create_course(CreateCourseRequest(name="Algorithms"), courses)

    all_courses = list(list_courses(courses))
    assert len(all_courses) == 1
    assert all_courses[0].course_id == created.course_id


def test_add_topic_and_plan_session() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()
    sessions = InMemorySessionRepository()

    course = create_course(CreateCourseRequest(name="Math"), courses)
    topic = add_topic(AddTopicRequest(course_id=course.course_id, name="Algebra"), courses, topics)
    session = plan_session(
        PlanSessionRequest(
            topic_id=topic.topic_id,
            scheduled_date=date(2026, 2, 3),
            duration_minutes=45,
        ),
        topics,
        sessions,
    )

    assert session.topic_id == topic.topic_id
    assert len(list(list_topics(course.course_id, topics))) == 1
    assert len(list(list_sessions(sessions))) == 1


def test_complete_session() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()
    sessions = InMemorySessionRepository()

    course = create_course(CreateCourseRequest(name="CS"), courses)
    topic = add_topic(AddTopicRequest(course_id=course.course_id, name="Graphs"), courses, topics)
    session = plan_session(
        PlanSessionRequest(
            topic_id=topic.topic_id,
            scheduled_date=date(2026, 2, 3),
            duration_minutes=60,
        ),
        topics,
        sessions,
    )

    completed = complete_session(
        CompleteSessionRequest(session_id=session.session_id),
        sessions,
    )
    assert completed.completed is True


def test_weekly_report_requires_monday() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()
    sessions = InMemorySessionRepository()

    with pytest.raises(ApplicationValidationError):
        generate_weekly_report(
            WeeklyReportRequest(week_start=date(2026, 2, 4)),
            courses,
            topics,
            sessions,
        )
