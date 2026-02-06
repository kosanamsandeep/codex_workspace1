from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from src.application import CourseRepository, SessionRepository, TopicRepository
from src.domain import Course, CourseId, SessionId, StudySession, Topic, TopicId


class InMemoryCourseRepository(CourseRepository):
    def __init__(self) -> None:
        self._items: dict[CourseId, Course] = {}

    def add(self, course: Course) -> None:
        self._items[course.course_id] = course

    def get(self, course_id: CourseId) -> Course | None:
        return self._items.get(course_id)

    def list_all(self) -> Iterable[Course]:
        return list(self._items.values())

    def remove(self, course_id: CourseId) -> None:
        self._items.pop(course_id, None)


class InMemoryTopicRepository(TopicRepository):
    def __init__(self) -> None:
        self._items: dict[TopicId, Topic] = {}
        self._by_course: dict[CourseId, set[TopicId]] = defaultdict(set)

    def add(self, topic: Topic) -> None:
        self._items[topic.topic_id] = topic
        self._by_course[topic.course_id].add(topic.topic_id)

    def get(self, topic_id: TopicId) -> Topic | None:
        return self._items.get(topic_id)

    def list_by_course(self, course_id: CourseId) -> Iterable[Topic]:
        return [self._items[topic_id] for topic_id in self._by_course[course_id]]

    def remove(self, topic_id: TopicId) -> None:
        topic = self._items.pop(topic_id, None)
        if topic is None:
            return
        self._by_course[topic.course_id].discard(topic_id)


class InMemorySessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._items: dict[SessionId, StudySession] = {}
        self._by_topic: dict[TopicId, set[SessionId]] = defaultdict(set)

    def add(self, session: StudySession) -> None:
        self._items[session.session_id] = session
        self._by_topic[session.topic_id].add(session.session_id)

    def get(self, session_id: SessionId) -> StudySession | None:
        return self._items.get(session_id)

    def list_by_topic(self, topic_id: TopicId) -> Iterable[StudySession]:
        return [self._items[session_id] for session_id in self._by_topic[topic_id]]

    def list_all(self) -> Iterable[StudySession]:
        return list(self._items.values())

    def update(self, session: StudySession) -> None:
        self._items[session.session_id] = session

