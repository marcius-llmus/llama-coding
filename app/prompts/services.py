from app.projects.models import Project
from app.projects.exceptions import ActiveProjectRequiredException
from app.projects.services import ProjectService
from app.prompts.exceptions import PromptNotFoundException, UnsupportedPromptTypeException
from app.prompts.models import Prompt
from app.prompts.repositories import PromptRepository
from app.prompts.schemas import NewPromptFormContext, PromptCreate, PromptsPageData, PromptUpdate
from app.prompts.enums import PromptType, PromptTargetSelector


class PromptService:
    def __init__(self, prompt_repo: PromptRepository):
        self.prompt_repo = prompt_repo

    def get_prompt(self, prompt_id: int) -> Prompt:
        prompt = self.prompt_repo.get(pk=prompt_id)
        if not prompt:
            raise PromptNotFoundException(f"Prompt with id {prompt_id} not found.")
        return prompt

    def create_prompt(self, prompt_in: PromptCreate) -> Prompt:
        return self.prompt_repo.create(obj_in=prompt_in)

    def update_prompt(self, prompt_id: int, prompt_in: PromptUpdate) -> Prompt:
        db_obj = self.get_prompt(prompt_id)
        return self.prompt_repo.update(db_obj=db_obj, obj_in=prompt_in)

    def delete_prompt(self, prompt_id: int) -> None:
        self.get_prompt(prompt_id)  # Ensures the prompt exists before attempting deletion
        self.prompt_repo.delete(pk=prompt_id)

    def get_global_prompts(self) -> list[Prompt]:
        return self.prompt_repo.list_global()

    def get_project_prompts(self, project: Project | None) -> list[Prompt]:
        if not project:
            return []
        return self.prompt_repo.list_by_project(project_id=project.id)

    def get_template_app_prompts(self) -> list[Prompt]:
        return self.prompt_repo.list_template_apps()


class PromptPageService:
    def __init__(self, prompt_service: PromptService, project_service: ProjectService):
        self.prompt_service = prompt_service
        self.project_service = project_service

    def get_prompts_page_data(self) -> PromptsPageData:
        active_project = self.project_service.project_repo.get_active()
        global_prompts = self.prompt_service.get_global_prompts()
        project_prompts = self.prompt_service.get_project_prompts(project=active_project)
        template_app_prompts = self.prompt_service.get_template_app_prompts()
        return {
            "global_prompts": global_prompts,
            "project_prompts": project_prompts,
            "template_app_prompts": template_app_prompts,
            "active_project": active_project,
        }

    def get_new_prompt_form_context(self, prompt_type: PromptType) -> NewPromptFormContext:
        if prompt_type == PromptType.GLOBAL:
            return {"prompt_type": prompt_type, "target_selector": PromptTargetSelector.GLOBAL}

        if prompt_type == PromptType.PROJECT:
            active_project = self.project_service.project_repo.get_active()
            if not active_project:
                raise ActiveProjectRequiredException("An active project is required to create a project prompt.")
            return {
                "prompt_type": prompt_type,
                "target_selector": PromptTargetSelector.PROJECT,
                "project_id": str(active_project.id),
            }

        raise UnsupportedPromptTypeException(f"Prompt type '{prompt_type}' is not supported for form creation.")
