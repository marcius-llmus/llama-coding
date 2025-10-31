from fastapi import Depends
from sqlalchemy.orm import Session

from app.commons.dependencies import get_db
from app.settings.repositories import LLMSettingsRepository, SettingsRepository
from app.settings.services import (
    LLMSettingsService,
    SettingsPageService,
    SettingsService,
)


def get_llm_settings_repository(db: Session = Depends(get_db)) -> LLMSettingsRepository:
    return LLMSettingsRepository(db=db)


def get_settings_repository(db: Session = Depends(get_db)) -> SettingsRepository:
    return SettingsRepository(db=db)


def get_llm_settings_service(
    llm_settings_repo: LLMSettingsRepository = Depends(get_llm_settings_repository),
) -> LLMSettingsService:
    return LLMSettingsService(llm_settings_repo=llm_settings_repo)


def get_settings_service(
    settings_repo: SettingsRepository = Depends(get_settings_repository),
    llm_settings_service: LLMSettingsService = Depends(get_llm_settings_service),
) -> SettingsService:
    return SettingsService(settings_repo=settings_repo, llm_settings_service=llm_settings_service)


def get_settings_page_service(
    settings_service: SettingsService = Depends(get_settings_service),
) -> SettingsPageService:
    return SettingsPageService(settings_service=settings_service)