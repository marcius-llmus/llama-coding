from pydantic import BaseModel

from app.chat.enums import MessageRole


class MessageCreate(BaseModel):
    session_id: int
    role: MessageRole
    content: str


class MessageForm(BaseModel):
    message: str