from pydantic import BaseModel


class ChatSessionCreate(BaseModel):
    name: str
    project_id: int