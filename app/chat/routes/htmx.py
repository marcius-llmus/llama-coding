from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.core.templating import templates

router = APIRouter()


@router.post("/", response_class=HTMLResponse)
async def handle_message(
    request: Request,
    message: Annotated[str, Form()],
):
    # This is a placeholder. Later, this will invoke the ChatService
    # and stream back the user message, then the AI response.
    return templates.TemplateResponse(
        "chat/partials/user_message.html", {"request": request, "message": message}
    )


@router.post("/clear", response_class=HTMLResponse)
async def clear_chat(request: Request):
    # This will later clear the session history and return the initial state
    return templates.TemplateResponse(
        "chat/partials/message_list.html", {"request": request}
    )
