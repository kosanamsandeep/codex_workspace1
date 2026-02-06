class ApplicationError(Exception):
    """Base error for application-level issues."""


class NotFoundError(ApplicationError):
    """Raised when a required entity is missing."""


class ApplicationValidationError(ApplicationError):
    """Raised for invalid use case input."""

