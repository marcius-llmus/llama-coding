from fastapi import Depends
from sqlalchemy.orm import Session

from app.commons.dependencies import get_db
from app.projects.dependencies import get_project_service
from app.projects.services import ProjectService
from app.prompts.repositories import PromptRepository
from app.prompts.services import PromptPageService, PromptService


def get_prompt_repository(db: Session = Depends(get_db)) -> PromptRepository:
    return PromptRepository(db=db)


def get_prompt_service(
    repo: PromptRepository = Depends(get_prompt_repository),
) -> PromptService:
    return PromptService(prompt_repo=repo)


def get_prompt_page_service(
    prompt_service: PromptService = Depends(get_prompt_service),
    project_service: ProjectService = Depends(get_project_service),
) -> PromptPageService:
    return PromptPageService(prompt_service=prompt_service, project_service=project_service)
