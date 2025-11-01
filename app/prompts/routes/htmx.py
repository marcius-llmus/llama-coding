from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from fastapi_htmx import htmx

from app.core.templating import templates
from app.projects.exceptions import ActiveProjectRequiredException
from app.projects.dependencies import get_project_service
from app.projects.services import ProjectService
from app.prompts.dependencies import get_prompt_page_service, get_prompt_service
from app.prompts.enums import PromptType
from app.prompts.exceptions import PromptNotFoundException, UnsupportedPromptTypeException
from app.prompts.schemas import PromptCreate, PromptUpdate
from app.prompts.services import PromptPageService, PromptService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_prompts_modal(
    request: Request,
    service: PromptPageService = Depends(get_prompt_page_service),
):
    page_data = service.get_prompts_page_data()
    return templates.TemplateResponse(
        "prompts/partials/modal_content.html", {"request": request, **page_data}
    )


@router.get("/new", response_class=HTMLResponse)
async def get_new_prompt_form(
    request: Request,
    prompt_type: PromptType = Query(...),
    service: PromptPageService = Depends(get_prompt_page_service),
):
    try:
        context = service.get_new_prompt_form_context(prompt_type=prompt_type)
        return templates.TemplateResponse(
            "prompts/partials/prompt_form.html", {"request": request, **context}
        )
    except ActiveProjectRequiredException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UnsupportedPromptTypeException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_class=HTMLResponse)
@htmx("prompts/partials/prompt_item")
async def create_prompt(
    request: Request,
    prompt_in: PromptCreate,
    service: PromptService = Depends(get_prompt_service),
):
    prompt = service.create_prompt(prompt_in=prompt_in)
    return {"prompt": prompt}


@router.get("/{prompt_id}/edit", response_class=HTMLResponse)
async def get_edit_prompt_form(
    request: Request,
    prompt_id: int,
    service: PromptService = Depends(get_prompt_service),
):
    try:
        prompt = service.get_prompt(prompt_id=prompt_id)
        return templates.TemplateResponse("prompts/partials/prompt_form.html", {"request": request, "prompt": prompt})
    except PromptNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{prompt_id}", response_class=HTMLResponse)
@htmx("prompts/partials/prompt_item")
async def update_prompt(
    request: Request,
    prompt_id: int,
    prompt_in: PromptUpdate,
    service: PromptService = Depends(get_prompt_service),
):
    try:
        prompt = service.update_prompt(prompt_id=prompt_id, prompt_in=prompt_in)
        return {"prompt": prompt}
    except PromptNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{prompt_id}", status_code=status.HTTP_200_OK)
async def delete_prompt(
    request: Request,
    prompt_id: int,
    service: PromptService = Depends(get_prompt_service),
):
    try:
        service.delete_prompt(prompt_id=prompt_id)
        return ""
    except PromptNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
