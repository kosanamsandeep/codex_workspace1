from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from src.adapters import (
    JsonCourseRepository,
    JsonFileStore,
    JsonSessionRepository,
    JsonTopicRepository,
)
from src.application import (
    AddTopicRequest,
    ApplicationError,
    CompleteSessionRequest,
    CreateCourseRequest,
    PlanSessionRequest,
    WeeklyReportRequest,
    add_topic,
    complete_session,
    create_course,
    delete_course,
    generate_weekly_report,
    list_courses,
    list_sessions,
    list_topics,
    plan_session,
    remove_topic,
)
from src.domain import CourseId, SessionId, TopicId


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="study-planner", description="Study Planner CLI")
    parser.add_argument(
        "--store",
        type=Path,
        default=Path("data/store.json"),
        help="Path to JSON store file",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    add_course = sub.add_parser("add-course", help="Create a course")
    add_course.add_argument("name")

    sub.add_parser("list-courses", help="List courses")

    delete_course_parser = sub.add_parser("delete-course", help="Delete a course")
    delete_course_parser.add_argument("course_id")

    add_topic_parser = sub.add_parser("add-topic", help="Add a topic to a course")
    add_topic_parser.add_argument("course_id")
    add_topic_parser.add_argument("name")

    list_topics_parser = sub.add_parser("list-topics", help="List topics for course")
    list_topics_parser.add_argument("course_id")

    remove_topic_parser = sub.add_parser("remove-topic", help="Remove a topic")
    remove_topic_parser.add_argument("topic_id")

    plan_session_parser = sub.add_parser("plan-session", help="Plan a study session")
    plan_session_parser.add_argument("topic_id")
    plan_session_parser.add_argument("date")
    plan_session_parser.add_argument("duration_minutes", type=int)

    complete_session_parser = sub.add_parser(
        "complete-session", help="Mark session complete"
    )
    complete_session_parser.add_argument("session_id")
    complete_session_parser.add_argument("--completed-at")

    sub.add_parser("list-sessions", help="List sessions")

    report_parser = sub.add_parser("weekly-report", help="Generate weekly report")
    report_parser.add_argument("week_start")

    return parser


def run(args: list[str] | None = None) -> int:
    parser = build_parser()
    namespace = parser.parse_args(args=args)

    store = JsonFileStore(namespace.store)
    course_repo = JsonCourseRepository(store)
    topic_repo = JsonTopicRepository(store)
    session_repo = JsonSessionRepository(store)

    try:
        if namespace.command == "add-course":
            course = create_course(CreateCourseRequest(name=namespace.name), course_repo)
            print(f"{course.course_id} {course.name}")
        elif namespace.command == "list-courses":
            for course in list_courses(course_repo):
                print(f"{course.course_id} {course.name}")
        elif namespace.command == "delete-course":
            delete_course(CourseId(namespace.course_id), course_repo)
            print("deleted")
        elif namespace.command == "add-topic":
            topic = add_topic(
                AddTopicRequest(course_id=CourseId(namespace.course_id), name=namespace.name),
                course_repo,
                topic_repo,
            )
            print(f"{topic.topic_id} {topic.name}")
        elif namespace.command == "list-topics":
            for topic in list_topics(CourseId(namespace.course_id), topic_repo):
                print(f"{topic.topic_id} {topic.name}")
        elif namespace.command == "remove-topic":
            remove_topic(TopicId(namespace.topic_id), topic_repo)
            print("removed")
        elif namespace.command == "plan-session":
            session = plan_session(
                PlanSessionRequest(
                    topic_id=TopicId(namespace.topic_id),
                    scheduled_date=_parse_date(namespace.date),
                    duration_minutes=namespace.duration_minutes,
                ),
                topic_repo,
                session_repo,
            )
            print(f"{session.session_id} {session.scheduled_date} {session.duration.value}")
        elif namespace.command == "complete-session":
            session = complete_session(
                CompleteSessionRequest(
                    session_id=SessionId(namespace.session_id),
                    completed_at=_parse_datetime(namespace.completed_at),
                ),
                session_repo,
            )
            print(f"{session.session_id} completed={session.completed}")
        elif namespace.command == "list-sessions":
            for session in list_sessions(session_repo):
                print(
                    f"{session.session_id} {session.topic_id} "
                    f"{session.scheduled_date} {session.duration.value} "
                    f"completed={session.completed}"
                )
        elif namespace.command == "weekly-report":
            report = generate_weekly_report(
                WeeklyReportRequest(week_start=_parse_date(namespace.week_start)),
                course_repo,
                topic_repo,
                session_repo,
            )
            print(f"week_start={report.week_start}")
            print(f"total_minutes={report.total_minutes}")
            for course_id, minutes in report.minutes_by_course.items():
                print(f"course {course_id} {minutes}")
            for topic_id, minutes in report.minutes_by_topic.items():
                print(f"topic {topic_id} {minutes}")
        else:
            parser.error("unknown command")
    except ApplicationError as exc:
        print(f"error: {exc}")
        return 1

    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
