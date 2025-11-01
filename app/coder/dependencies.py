from fastapi import Depends

from app.chat.dependencies import get_chat_service
from app.chat.services import ChatService
from app.coder.services import CoderService
from app.usage.dependencies import get_usage_service
from app.usage.services import UsageService


def get_coder_service(
    chat_service: ChatService = Depends(get_chat_service),
    usage_service: UsageService = Depends(get_usage_service),
) -> CoderService:
    return CoderService(
        chat_service=chat_service,
        usage_service=usage_service,
    )