from app.settings.models import LLMSettings, Settings
from app.settings.repositories import LLMSettingsRepository, SettingsRepository
from app.settings.exceptions import LLMSettingsNotFoundException, SettingsNotFoundException
from app.settings.schemas import LLMSettingsUpdate, SettingsUpdate


class LLMSettingsService:
    def __init__(self, llm_settings_repo: LLMSettingsRepository):
        self.llm_settings_repo = llm_settings_repo

    def update_llm_settings(self, *, llm_settings_id: int, settings_in: LLMSettingsUpdate) -> LLMSettings:
        db_obj = self.llm_settings_repo.get(pk=llm_settings_id)
        if not db_obj:
            raise LLMSettingsNotFoundException(f"LLMSettings with id {llm_settings_id} not found.")
        return self.llm_settings_repo.update(db_obj=db_obj, obj_in=settings_in)


class SettingsService:
    def __init__(
        self,
        settings_repo: SettingsRepository,
        llm_settings_service: LLMSettingsService,
    ):
        self.settings_repo = settings_repo
        self.llm_settings_service = llm_settings_service

    def get_settings(self) -> Settings:
        settings = self.settings_repo.get(pk=1)
        if not settings:
            # This should not happen if the startup hook is successful
            raise SettingsNotFoundException("Application settings have not been initialized.")
        return settings

    def update_settings(self, *, settings_in: SettingsUpdate) -> Settings:
        settings = self.get_settings()

        if settings_in.coding_llm_settings:
            self.llm_settings_service.update_llm_settings(
                llm_settings_id=settings.coding_llm_settings_id,
                settings_in=settings_in.coding_llm_settings,
            )

        return self.settings_repo.update(db_obj=settings, obj_in=settings_in)


class SettingsPageService:
    def __init__(self, settings_service: SettingsService):
        self.settings_service = settings_service

    def get_settings_page_data(self) -> dict:
        settings = self.settings_service.get_settings()
        return {"settings": settings}
