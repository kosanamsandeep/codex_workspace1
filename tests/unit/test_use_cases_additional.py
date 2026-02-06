from __future__ import annotations

from datetime import date, timedelta

import pytest

from src.adapters import (
    InMemoryCourseRepository,
    InMemorySessionRepository,
    InMemoryTopicRepository,
)
from src.application import (
    AddTopicRequest,
    CreateCourseRequest,
    NotFoundError,
    PlanSessionRequest,
    WeeklyReportRequest,
    add_topic,
    create_course,
    delete_course,
    generate_weekly_report,
    plan_session,
    remove_topic,
)


def test_delete_course_and_remove_topic() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()

    course = create_course(CreateCourseRequest(name="Databases"), courses)
    topic = add_topic(AddTopicRequest(course_id=course.course_id, name="Indexes"), courses, topics)

    remove_topic(topic.topic_id, topics)
    assert list(topics.list_by_course(course.course_id)) == []

    delete_course(course.course_id, courses)
    assert list(courses.list_all()) == []

    with pytest.raises(NotFoundError):
        delete_course(course.course_id, courses)


def test_weekly_report_totals() -> None:
    courses = InMemoryCourseRepository()
    topics = InMemoryTopicRepository()
    sessions = InMemorySessionRepository()

    course = create_course(CreateCourseRequest(name="Systems"), courses)
    topic = add_topic(AddTopicRequest(course_id=course.course_id, name="CPU"), courses, topics)

    monday = date(2026, 2, 2)
    plan_session(
        PlanSessionRequest(topic_id=topic.topic_id, scheduled_date=monday, duration_minutes=30),
        topics,
        sessions,
    )
    plan_session(
        PlanSessionRequest(
            topic_id=topic.topic_id,
            scheduled_date=monday + timedelta(days=2),
            duration_minutes=45,
        ),
        topics,
        sessions,
    )
    plan_session(
        PlanSessionRequest(
            topic_id=topic.topic_id,
            scheduled_date=monday + timedelta(days=10),
            duration_minutes=60,
        ),
        topics,
        sessions,
    )

    report = generate_weekly_report(
        WeeklyReportRequest(week_start=monday),
        courses,
        topics,
        sessions,
    )
    assert report.total_minutes == 75
    assert report.minutes_by_course[course.course_id] == 75
    assert report.minutes_by_topic[topic.topic_id] == 75
