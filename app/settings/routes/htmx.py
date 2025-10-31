from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi_htmx import htmx

from app.core.templating import templates
from app.settings.dependencies import get_settings_service
from app.settings.schemas import SettingsUpdate
from app.settings.services import SettingsService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_settings_modal(
    request: Request,
    service: SettingsService = Depends(get_settings_service),
):
    page_data = service.get_settings_page_data()
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
    service.update_settings(settings_in=settings_in)
    return {"settings": service.get_settings(), "success": "Settings saved successfully"}