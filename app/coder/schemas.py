from pydantic import BaseModel


class WebSocketMessage(BaseModel):
    message: str