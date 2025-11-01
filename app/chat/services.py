from app.chat.enums import MessageRole
from app.chat.repositories import MessageRepository
from app.chat.schemas import MessageCreate
from app.history.models import ChatSession, Message
from app.history.schemas import ChatSessionCreate
from app.history.services import HistoryService
from app.projects.exceptions import ActiveProjectRequiredException
from app.projects.services import ProjectService


class ChatService:
    def __init__(
        self,
        message_repo: MessageRepository,
        history_service: HistoryService,
        project_service: ProjectService,
    ):
        self.message_repo = message_repo
        self.history_service = history_service
        self.project_service = project_service

    def get_or_create_active_session(self) -> ChatSession:
        active_project = self.project_service.project_repo.get_active()
        if not active_project:
            raise ActiveProjectRequiredException("Cannot start a chat without an active project.")

        sessions = self.history_service.get_sessions_by_project(project_id=active_project.id)
        if sessions:
            return sessions[0]  # Return the most recent session

        session_in = ChatSessionCreate(name="New Session", project_id=active_project.id)
        return self.history_service.create_session(session_in=session_in)

    def add_user_message(self, content: str) -> Message:
        session = self.get_or_create_active_session()
        message_in = MessageCreate(
            session_id=session.id,
            role=MessageRole.USER,
            content=content,
        )
        return self.message_repo.create(obj_in=message_in)