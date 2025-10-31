from typing import NotRequired, TypedDict

from pydantic import BaseModel, ConfigDict

from app.projects.models import Project
from app.prompts.enums import PromptType
from app.prompts.models import Prompt


class PromptBase(BaseModel):
    name: str
    content: str
    type: PromptType


class PromptCreate(PromptBase):
    project_id: int | None = None


class PromptUpdate(BaseModel):
    name: str | None = None
    content: str | None = None


class PromptRead(PromptBase):
    id: int
    project_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class PromptsPageData(TypedDict):
    global_prompts: list[Prompt]
    project_prompts: list[Prompt]
    template_app_prompts: list[Prompt]
    active_project: Project | None


class NewPromptFormContext(TypedDict):
    prompt_type: str
    target_selector: str
    project_id: NotRequired[str]
