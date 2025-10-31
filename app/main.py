from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi_htmx import htmx_init

from app.chat.routes.htmx import router as chat_htmx_router
from app.core.db import engine
from app.core.templating import templates
from app.settings.routes.htmx import router as settings_htmx_router
from app.settings.utils import initialize_application_settings

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

app.include_router(settings_htmx_router, prefix="/settings", tags=["settings"])
app.include_router(chat_htmx_router, prefix="/chat", tags=["chat"])


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # This should eventually fetch initial data from an orchestrator service
    # For now, it just renders the main page shell.
    return templates.TemplateResponse("chat/pages/main.html", {"request": request})