class PromptException(Exception):
    """Base exception for prompts application."""


class PromptNotFoundException(PromptException):
    """Raised when a prompt is not found."""


class UnsupportedPromptTypeException(PromptException):
    """Raised when an unsupported prompt type is used for an operation."""
