from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

from app.settings.enums import CodingMode, ContextStrategy, OperationalMode


class LLMSettingsBase(BaseModel):
    model_name: str
    temperature: Decimal = Field(..., ge=0, le=1, max_digits=3, decimal_places=2)
    context_window: int


class LLMSettingsCreate(LLMSettingsBase):
    pass


class LLMSettingsRead(LLMSettingsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LLMSettingsUpdate(BaseModel):
    model_name: str | None = None
    temperature: Decimal | None = Field(default=None, ge=0, le=1, max_digits=3, decimal_places=2)
    context_window: int | None = None


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