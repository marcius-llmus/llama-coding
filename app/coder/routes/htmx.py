from fastapi import APIRouter, Depends, WebSocket

from app.coder.dependencies import get_coder_service
from app.coder.presentation import WebSocketOrchestrator
from app.coder.services import CoderService
from app.commons.websockets import WebSocketConnectionManager

router = APIRouter()


@router.websocket("/ws")
async def conversation_websocket(
    websocket: WebSocket,
    coder_service: CoderService = Depends(get_coder_service),
):
    ws_manager = WebSocketConnectionManager(websocket)
    await ws_manager.connect()
    orchestrator = WebSocketOrchestrator(coder_service=coder_service, ws_manager=ws_manager)
    await orchestrator.handle_connection()