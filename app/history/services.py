from app.projects.exceptions import ActiveProjectRequiredException
from app.projects.services import ProjectService
from app.history.exceptions import ChatSessionNotFoundException
from app.history.models import ChatSession
from app.history.repositories import ChatSessionRepository
from app.history.schemas import ChatSessionCreate


class HistoryService:
    def __init__(self, session_repo: ChatSessionRepository):
        self.session_repo = session_repo

    def get_sessions_by_project(self, project_id: int) -> list[ChatSession]:
        return self.session_repo.list_by_project(project_id=project_id)

    def create_session(self, session_in: ChatSessionCreate) -> ChatSession:
        return self.session_repo.create(obj_in=session_in)

    def delete_session(self, session_id: int) -> None:
        session = self.session_repo.get(pk=session_id)
        if not session:
            raise ChatSessionNotFoundException(f"Session with id {session_id} not found.")
        self.session_repo.delete(pk=session_id)


class HistoryPageService:
    def __init__(self, history_service: HistoryService, project_service: ProjectService):
        self.history_service = history_service
        self.project_service = project_service

    def get_history_page_data(self) -> dict:
        active_project = self.project_service.project_repo.get_active()
        sessions = self.history_service.get_sessions_by_project(project_id=active_project.id) if active_project else []
        return {"sessions": sessions}