from enum import StrEnum


class PromptType(StrEnum):
    SYSTEM = "system"
    GLOBAL = "global"
    PROJECT = "project"
    TEMPLATE_APP = "template_app"


class PromptTargetSelector(StrEnum):
    GLOBAL = "#global-prompt-list-container"
    PROJECT = "#project-prompt-list-container"
