from sqlalchemy.orm import Session

from app.settings.enums import CodingMode, ContextStrategy, OperationalMode
from app.settings.repositories import LLMSettingsRepository, SettingsRepository
from app.settings.schemas import LLMSettingsCreate, SettingsCreate


def initialize_application_settings(db: Session) -> None:
    """
    Creates the default application settings if they don't exist.
    This function should be called on application startup.
    """
    settings_repo = SettingsRepository(db)
    existing_settings = settings_repo.get(pk=1)

    if not existing_settings:
        llm_settings_repo = LLMSettingsRepository(db)
        default_llm = llm_settings_repo.get_by_model_and_temp(model_name="GPT-4", temperature=0.7)
        if not default_llm:
            default_llm = llm_settings_repo.create(
                LLMSettingsCreate(model_name="GPT-4", temperature=0.7, context_window=200000)
            )

        settings_repo.create(
            SettingsCreate(
                operational_mode=OperationalMode.CODE,
                coding_mode=CodingMode.AGENT,
                context_strategy=ContextStrategy.MANUAL,
                max_history_length=50,
                ast_token_limit=10000,
                coding_llm_settings_id=default_llm.id,
            )
        )
        db.commit()