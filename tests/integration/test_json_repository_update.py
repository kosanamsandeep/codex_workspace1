from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from src.adapters import JsonCourseRepository, JsonFileStore, JsonSessionRepository, JsonTopicRepository
from src.domain import DurationMinutes, StudySession, new_course_id, new_session_id, new_topic_id
from src.domain.models import Course, Topic


def test_json_update_and_list(tmp_path: Path) -> None:
    store = JsonFileStore(tmp_path / "store.json")
    courses = JsonCourseRepository(store)
    topics = JsonTopicRepository(store)
    sessions = JsonSessionRepository(store)

    course = Course(course_id=new_course_id(), name="AI")
    courses.add(course)

    topic = Topic(topic_id=new_topic_id(), course_id=course.course_id, name="Planning")
    topics.add(topic)

    session = StudySession(
        session_id=new_session_id(),
        topic_id=topic.topic_id,
        scheduled_date=date(2026, 2, 2),
        duration=DurationMinutes(30),
    )
    sessions.add(session)

    other = StudySession(
        session_id=new_session_id(),
        topic_id=topic.topic_id,
        scheduled_date=date(2026, 2, 3),
        duration=DurationMinutes(15),
    )
    sessions.add(other)

    updated = session.complete(completed_at=datetime(2026, 2, 2, 12, 0, 0))
    sessions.update(updated)

    reloaded = sessions.get(session.session_id)
    assert reloaded is not None
    assert reloaded.completed is True

    by_topic = list(sessions.list_by_topic(topic.topic_id))
    assert len(by_topic) == 2

    all_sessions = list(sessions.list_all())
    assert len(all_sessions) == 2
