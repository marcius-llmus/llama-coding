from fastapi import Depends

from app.chat.dependencies import get_chat_service
from app.chat.services import ChatService
from app.coder.services import CoderService, CoderPageService
from app.usage.dependencies import get_usage_service
from app.usage.dependencies import get_usage_page_service
from app.usage.services import UsageService
from app.usage.services import UsagePageService


def get_coder_service(
    chat_service: ChatService = Depends(get_chat_service),
    usage_service: UsageService = Depends(get_usage_service),
) -> CoderService:
    return CoderService(
        chat_service=chat_service,
        usage_service=usage_service,
    )


def get_coder_page_service(
    usage_page_service: UsagePageService = Depends(get_usage_page_service),
) -> CoderPageService:
    return CoderPageService(usage_page_service=usage_page_service)
