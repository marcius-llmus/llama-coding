from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi_htmx import htmx_init

from app.coder.routes.htmx import router as coder_htmx_router
from app.chat.routes.htmx import router as chat_htmx_router
from app.core.db import engine
from app.core.templating import templates
from app.projects.routes.htmx import router as projects_htmx_router
from app.context.routes.htmx import router as context_htmx_router
from app.history.routes.htmx import router as history_htmx_router
from app.prompts.routes.htmx import router as prompts_htmx_router
from app.settings.routes.htmx import router as settings_htmx_router
from app.settings.utils import initialize_application_settings
from app.usage.dependencies import get_usage_page_service
from app.usage.services import UsagePageService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ensures that the default application settings are created on startup.
    """
    with Session(engine) as session:
        initialize_application_settings(session)
    yield

app = FastAPI(lifespan=lifespan)

htmx_init(templates=templates, file_extension="html")

app.include_router(coder_htmx_router, prefix="/coder", tags=["coder"])
app.include_router(settings_htmx_router, prefix="/settings", tags=["settings"])
app.include_router(projects_htmx_router, prefix="/projects", tags=["projects"])
app.include_router(prompts_htmx_router, prefix="/prompts", tags=["prompts"])
app.include_router(context_htmx_router, prefix="/context", tags=["context"])
app.include_router(history_htmx_router, prefix="/history", tags=["history"])
app.include_router(chat_htmx_router, prefix="/chat", tags=["chat"])


@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    usage_page_service: UsagePageService = Depends(get_usage_page_service),
):
    # This should eventually fetch initial data from an orchestrator service
    # For now, it just renders the main page shell.
    usage_data = usage_page_service.get_session_metrics_page_data()
    return templates.TemplateResponse("chat/pages/main.html", {"request": request, **usage_data})