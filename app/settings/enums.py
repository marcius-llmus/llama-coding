from enum import StrEnum


class OperationalMode(StrEnum):
    CODE = "code"
    PLAN = "plan"
    READ_ONLY = "read_only"


class CodingMode(StrEnum):
    AGENT = "agent"
    SINGLE_SHOT = "single_shot"


class ContextStrategy(StrEnum):
    MANUAL = "manual"
    AUTO_GATHER = "auto_gather"
    RAG = "rag"