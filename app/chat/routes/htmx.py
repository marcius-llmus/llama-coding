from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.chat.dependencies import get_chat_service
from app.chat.schemas import MessageForm
from app.chat.services import ChatService
from app.core.templating import templates

router = APIRouter()


@router.post("/", response_class=HTMLResponse)
async def handle_message(
    request: Request,
    form_data: MessageForm,
    service: ChatService = Depends(get_chat_service),
):
    # This is a placeholder. Later, this will invoke the ChatService
    # and stream back the user message, then the AI response.
    user_message = service.add_user_message(content=form_data.message)
    return templates.TemplateResponse(
        "chat/partials/user_message.html", {"request": request, "message": user_message.content}
    )


@router.post("/clear", response_class=HTMLResponse)
async def clear_chat(request: Request):
    # This will later clear the session history and return the initial state
    return templates.TemplateResponse(
        "chat/partials/message_list.html", {"request": request}
    )