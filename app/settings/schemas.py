from pydantic import BaseModel, ConfigDict, Field

from app.settings.enums import CodingMode, ContextStrategy, OperationalMode


class LLMSettingsBase(BaseModel):
    model_name: str
    temperature: float
    context_window: int


class LLMSettingsCreate(LLMSettingsBase):
    pass


class LLMSettingsRead(LLMSettingsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LLMSettingsUpdate(BaseModel):
    model_name: str
    temperature: float
    context_window: int


class SettingsBase(BaseModel):
    operational_mode: OperationalMode
    coding_mode: CodingMode
    context_strategy: ContextStrategy
    max_history_length: int
    ast_token_limit: int


class SettingsCreate(SettingsBase):
    coding_llm_settings_id: int


class SettingsUpdate(BaseModel):
    max_history_length: int | None = None
    ast_token_limit: int | None = None
    coding_llm_settings: LLMSettingsUpdate | None = Field(default=None, exclude=True)


class SettingsRead(SettingsBase):
    id: int
    coding_llm_settings: LLMSettingsRead
    model_config = ConfigDict(from_attributes=True)