import logging
from typing import Any, Callable, Coroutine

from fastapi import WebSocketDisconnect
from pydantic import ValidationError

from app.coder.enums import CoderEventType
from app.coder.schemas import WebSocketMessage
from app.coder.services import CoderService
from app.commons.websockets import WebSocketConnectionManager
from app.core.templating import templates

logger = logging.getLogger(__name__)

Handler = Callable[[Any], Coroutine[Any, Any, None]]


class WebSocketOrchestrator:
    def __init__(
        self,
        coder_service: CoderService,
        ws_manager: WebSocketConnectionManager,
    ):
        self.coder_service = coder_service
        self.ws_manager = ws_manager
        self.event_handlers: dict[CoderEventType, Handler] = {
            CoderEventType.USER_MESSAGE: self._render_user_message,
            CoderEventType.AI_MESSAGE_CHUNK: self._render_ai_message_chunk,
            CoderEventType.SYSTEM_LOG_APPENDED: self._render_system_log,
            CoderEventType.USAGE_METRICS_UPDATED: self._render_usage_metrics,
            CoderEventType.ERROR: self._render_error,
        }

    async def _process_chunk(self, chunk: dict):
        event_type = chunk["type"]
        event_data = chunk["data"]
        handler = self.event_handlers.get(event_type)
        if not handler:
            logger.warning(f"No handler for event type: {event_type}")
            return
        await handler(event_data)

    async def handle_connection(self):
        logger.info("WebSocket connection established.")
        try:
            while True:
                data = await self.ws_manager.receive_json()
                logger.info("Received JSON data from client.")

                try:
                    message = WebSocketMessage(**data)
                except ValidationError as e:
                    logger.error(f"WebSocket validation error: {e}", exc_info=True)
                    await self._render_error(f"Invalid message format: {e}")
                    continue

                stream = self.coder_service.stream_workflow_response(user_message=message.message)

                async for chunk in stream:
                    await self._process_chunk(chunk)

        except WebSocketDisconnect:
            logger.info("Client disconnected. Connection handled gracefully.")
        except Exception as e:
            logger.error(f"An error occurred in WebSocket: {e}", exc_info=True)
            await self._render_error(str(e))

    async def _render_user_message(self, data: dict):
        template = templates.get_template("chat/partials/user_message.html").render(data)
        await self.ws_manager.send_html(template)

    async def _render_ai_message_chunk(self, data: dict):
        template = templates.get_template("chat/partials/ai_message.html").render(data)
        await self.ws_manager.send_html(template)

    async def _render_system_log(self, data: dict):
        template = templates.get_template("logs/partials/log_item.html").render(data)
        await self.ws_manager.send_html(template)

    async def _render_usage_metrics(self, data: dict):
        template = templates.get_template("usage/partials/session_metrics.html").render(data)
        await self.ws_manager.send_html(template)

    async def _render_error(self, error_message: str):
        template = templates.get_template("chat/partials/error_message.html").render({"message": error_message})
        await self.ws_manager.send_html(template)