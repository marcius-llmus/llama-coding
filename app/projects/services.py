from app.projects.exceptions import ProjectNotFoundException
from app.projects.models import Project
from app.projects.repositories import ProjectRepository
from app.projects.schemas import ProjectCreate


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def get_projects(self) -> list[Project]:
        return self.project_repo.list()

    def get_project(self, project_id: int) -> Project:
        project = self.project_repo.get(pk=project_id)
        if not project:
            raise ProjectNotFoundException(f"Project with id {project_id} not found.")
        return project

    def create_project(self, project_in: ProjectCreate) -> Project:
        return self.project_repo.create(obj_in=project_in)

    def set_active_project(self, project_id: int) -> list[Project]:
        project_to_activate = self.get_project(project_id=project_id)
        current_active = self.project_repo.get_active()

        if current_active and current_active.id != project_to_activate.id:
            current_active.is_active = False
            self.project_repo.db.add(current_active)

        if not project_to_activate.is_active:
            project_to_activate.is_active = True
            self.project_repo.db.add(project_to_activate)

        return self.project_repo.list()


class ProjectPageService:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def get_projects_page_data(self) -> dict:
        projects = self.project_service.get_projects()
        return {"projects": projects}
