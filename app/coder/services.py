from datetime import datetime
from typing import AsyncGenerator

from app.chat.services import ChatService
from app.coder.enums import CoderEventType
from app.usage.services import UsageService


class CoderService:
    def __init__(
        self,
        chat_service: ChatService,
        usage_service: UsageService,
    ):
        self.chat_service = chat_service
        self.usage_service = usage_service

    async def stream_workflow_response(self, user_message: str) -> AsyncGenerator[dict, None]:
        # 1. Persist user message and yield it back to the UI
        message_obj = self.chat_service.add_user_message(content=user_message)
        yield {"type": CoderEventType.USER_MESSAGE, "data": {"message": message_obj.content}}

        # 2. Simulate AI thinking and responding
        import asyncio

        await asyncio.sleep(0.5)
        yield {"type": CoderEventType.AI_MESSAGE_CHUNK, "data": {"message": "This is a streamed response from the Coder."}}
        await asyncio.sleep(0.5)
        yield {
            "type": CoderEventType.AI_MESSAGE_CHUNK,
            "data": {"message": " I will soon be able to generate code and manage context."},
        }

        # 3. Simulate a log event
        await asyncio.sleep(0.2)
        log_data = {"message": "AI workflow started.", "color": "blue", "timestamp": datetime.now().strftime("%H:%M:%S")}
        yield {"type": CoderEventType.SYSTEM_LOG_APPENDED, "data": log_data}

        # 4. Simulate a usage update
        await asyncio.sleep(0.2)
        metrics = self.usage_service.get_session_metrics()
        metrics.input_tokens = 50
        metrics.output_tokens = 150
        metrics.session_cost = 0.00012
        metrics.message_count = len(message_obj.session.messages)
        yield {"type": CoderEventType.USAGE_METRICS_UPDATED, "data": {"metrics": metrics}}