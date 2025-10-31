class ProjectException(Exception):
    """Base exception for projects application."""


class ProjectNotFoundException(ProjectException):
    """Raised when a project is not found."""


class MultipleActiveProjectsException(ProjectException):
    """Raised when more than one active project is found."""
