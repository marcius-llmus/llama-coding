from pydantic import BaseModel


class SessionMetrics(BaseModel):
    session_cost: float = 0.0
    monthly_cost: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    message_count: int = 0
    files_count: int = 0