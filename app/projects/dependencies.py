from fastapi import Depends
from sqlalchemy.orm import Session

from app.commons.dependencies import get_db
from app.projects.repositories import ProjectRepository
from app.projects.services import ProjectPageService, ProjectService


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db=db)


def get_project_service(
    repo: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repo=repo)


def get_project_page_service(
    service: ProjectService = Depends(get_project_service),
) -> ProjectPageService:
    return ProjectPageService(project_service=service)
