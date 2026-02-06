from __future__ import annotations

from src.adapters import InMemorySessionRepository, InMemoryTopicRepository
from src.domain import CourseId, TopicId


def test_list_by_course_empty() -> None:
    topics = InMemoryTopicRepository()
    assert list(topics.list_by_course(CourseId("missing-course"))) == []


def test_list_by_topic_empty() -> None:
    sessions = InMemorySessionRepository()
    assert list(sessions.list_by_topic(TopicId("missing-topic"))) == []


def test_remove_missing_topic_is_noop() -> None:
    topics = InMemoryTopicRepository()
    topics.remove(TopicId("missing-topic"))
