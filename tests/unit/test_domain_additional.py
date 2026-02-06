from __future__ import annotations

from datetime import date, datetime

import pytest

from src.domain import DurationMinutes, StudySession, new_session_id, new_topic_id
from src.domain.errors import DomainValidationError


def test_completed_session_requires_completed_at() -> None:
    with pytest.raises(DomainValidationError):
        StudySession(
            session_id=new_session_id(),
            topic_id=new_topic_id(),
            scheduled_date=date(2026, 2, 1),
            duration=DurationMinutes(30),
            completed=True,
            completed_at=None,
        )


def test_completed_at_requires_completed_flag() -> None:
    with pytest.raises(DomainValidationError):
        StudySession(
            session_id=new_session_id(),
            topic_id=new_topic_id(),
            scheduled_date=date(2026, 2, 1),
            duration=DurationMinutes(30),
            completed=False,
            completed_at=datetime(2026, 2, 1, 10, 0, 0),
        )
