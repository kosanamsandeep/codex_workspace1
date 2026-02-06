from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable

from src.domain import (
    Course,
    CourseId,
    DurationMinutes,
    SessionId,
    StudySession,
    Topic,
    TopicId,
    new_course_id,
    new_session_id,
    new_topic_id,
)

from .errors import ApplicationValidationError, NotFoundError
from .ports import CourseRepository, SessionRepository, TopicRepository, WeeklyReport


@dataclass(frozen=True)
class CreateCourseRequest:
    name: str


@dataclass(frozen=True)
class AddTopicRequest:
    course_id: CourseId
    name: str


@dataclass(frozen=True)
class PlanSessionRequest:
    topic_id: TopicId
    scheduled_date: date
    duration_minutes: int


@dataclass(frozen=True)
class CompleteSessionRequest:
    session_id: SessionId
    completed_at: datetime | None = None


@dataclass(frozen=True)
class WeeklyReportRequest:
    week_start: date


def create_course(
    request: CreateCourseRequest, course_repo: CourseRepository
) -> Course:
    name = request.name.strip()
    if not name:
        raise ApplicationValidationError("course name cannot be empty")
    course = Course(course_id=new_course_id(), name=name)
    course_repo.add(course)
    return course


def list_courses(course_repo: CourseRepository) -> Iterable[Course]:
    return course_repo.list_all()


def delete_course(course_id: CourseId, course_repo: CourseRepository) -> None:
    if course_repo.get(course_id) is None:
        raise NotFoundError("course not found")
    course_repo.remove(course_id)


def add_topic(
    request: AddTopicRequest,
    course_repo: CourseRepository,
    topic_repo: TopicRepository,
) -> Topic:
    if course_repo.get(request.course_id) is None:
        raise NotFoundError("course not found")
    name = request.name.strip()
    if not name:
        raise ApplicationValidationError("topic name cannot be empty")
    topic = Topic(topic_id=new_topic_id(), course_id=request.course_id, name=name)
    topic_repo.add(topic)
    return topic


def list_topics(
    course_id: CourseId, topic_repo: TopicRepository
) -> Iterable[Topic]:
    return topic_repo.list_by_course(course_id)


def remove_topic(topic_id: TopicId, topic_repo: TopicRepository) -> None:
    if topic_repo.get(topic_id) is None:
        raise NotFoundError("topic not found")
    topic_repo.remove(topic_id)


def plan_session(
    request: PlanSessionRequest, topic_repo: TopicRepository, session_repo: SessionRepository
) -> StudySession:
    if topic_repo.get(request.topic_id) is None:
        raise NotFoundError("topic not found")
    duration = DurationMinutes(request.duration_minutes)
    session = StudySession(
        session_id=new_session_id(),
        topic_id=request.topic_id,
        scheduled_date=request.scheduled_date,
        duration=duration,
    )
    session_repo.add(session)
    return session


def list_sessions(session_repo: SessionRepository) -> Iterable[StudySession]:
    return session_repo.list_all()


def complete_session(
    request: CompleteSessionRequest, session_repo: SessionRepository
) -> StudySession:
    session = session_repo.get(request.session_id)
    if session is None:
        raise NotFoundError("session not found")
    completed = session.complete(completed_at=request.completed_at)
    session_repo.update(completed)
    return completed


def generate_weekly_report(
    request: WeeklyReportRequest,
    course_repo: CourseRepository,
    topic_repo: TopicRepository,
    session_repo: SessionRepository,
) -> WeeklyReport:
    week_start = request.week_start
    if week_start.weekday() != 0:
        raise ApplicationValidationError("week_start must be a Monday")
    week_end = week_start + timedelta(days=7)

    minutes_by_course: dict[CourseId, int] = {}
    minutes_by_topic: dict[TopicId, int] = {}
    total_minutes = 0

    sessions = session_repo.list_all()
    for session in sessions:
        if not (week_start <= session.scheduled_date < week_end):
            continue
        total_minutes += session.duration.value
        minutes_by_topic[session.topic_id] = (
            minutes_by_topic.get(session.topic_id, 0) + session.duration.value
        )

    # Map topic totals to course totals
    for course in course_repo.list_all():
        course_total = 0
        for topic in topic_repo.list_by_course(course.course_id):
            course_total += minutes_by_topic.get(topic.topic_id, 0)
        if course_total:
            minutes_by_course[course.course_id] = course_total

    return WeeklyReport(
        week_start=week_start,
        total_minutes=total_minutes,
        minutes_by_course=minutes_by_course,
        minutes_by_topic=minutes_by_topic,
    )

