from __future__ import annotations

from datetime import date
from pathlib import Path

from src.adapters import JsonCourseRepository, JsonFileStore, JsonSessionRepository, JsonTopicRepository
from src.domain import DurationMinutes, StudySession, new_course_id, new_session_id, new_topic_id
from src.domain.models import Course, Topic


def test_json_repositories_round_trip(tmp_path: Path) -> None:
    store = JsonFileStore(tmp_path / "store.json")
    courses = JsonCourseRepository(store)
    topics = JsonTopicRepository(store)
    sessions = JsonSessionRepository(store)

    course = Course(course_id=new_course_id(), name="Physics")
    courses.add(course)
    assert courses.get(course.course_id) is not None

    topic = Topic(topic_id=new_topic_id(), course_id=course.course_id, name="Optics")
    topics.add(topic)
    assert topics.get(topic.topic_id) is not None

    session = StudySession(
        session_id=new_session_id(),
        topic_id=topic.topic_id,
        scheduled_date=date(2026, 2, 5),
        duration=DurationMinutes(30),
    )
    sessions.add(session)
    assert sessions.get(session.session_id) is not None
