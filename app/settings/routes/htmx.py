from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi_htmx import htmx

from app.core.templating import templates
from app.settings.dependencies import get_settings_page_service, get_settings_service
from app.settings.exceptions import LLMSettingsNotFoundException, SettingsNotFoundException
from app.settings.schemas import SettingsUpdate
from app.settings.services import SettingsPageService, SettingsService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_settings_modal(
    request: Request,
    service: SettingsPageService = Depends(get_settings_page_service),
):
    try:
        page_data = service.get_settings_page_data()
    except SettingsNotFoundException as e:
        # This is a server error, as settings should always be initialized
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return templates.TemplateResponse(
        "settings/partials/modal_content.html", {"request": request, **page_data}
    )


@router.post("/", response_class=HTMLResponse)
@htmx("settings/partials/modal_content", re_swap="innerHTML")
async def update_settings(
    request: Request,
    settings_in: SettingsUpdate,
    service: SettingsService = Depends(get_settings_service),
):
    try:
        service.update_settings(settings_in=settings_in)
        return {"settings": service.get_settings(), "success": "Settings saved successfully"}
    except (SettingsNotFoundException, LLMSettingsNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))