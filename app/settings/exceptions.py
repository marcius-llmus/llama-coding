class SettingsException(Exception):
    """Base exception for settings application."""


class SettingsNotFoundException(SettingsException):
    """Raised when application settings are not found."""


class LLMSettingsNotFoundException(SettingsException):
    """Raised when LLM settings are not found."""