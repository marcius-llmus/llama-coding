from fastapi import APIRouter, Depends, WebSocket, Request
from fastapi.responses import HTMLResponse

from app.coder.dependencies import get_coder_page_service, get_coder_service
from app.coder.presentation import WebSocketOrchestrator
from app.coder.services import CoderService, CoderPageService
from app.commons.websockets import WebSocketConnectionManager
from app.core.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    page_service: CoderPageService = Depends(get_coder_page_service),
):
    page_data = page_service.get_main_page_data()
    return templates.TemplateResponse(
        "chat/pages/main.html", {"request": request, **page_data}
    )


@router.websocket("/ws")
async def conversation_websocket(
    websocket: WebSocket,
    coder_service: CoderService = Depends(get_coder_service),
):
    ws_manager = WebSocketConnectionManager(websocket)
    await ws_manager.connect()
    orchestrator = WebSocketOrchestrator(coder_service=coder_service, ws_manager=ws_manager)
    await orchestrator.handle_connection()
