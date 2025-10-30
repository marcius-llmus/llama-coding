from sqlalchemy import (
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.settings.enums import CodingMode, ContextStrategy, OperationalMode


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, default=1)
    operational_mode = Column(Enum(OperationalMode), nullable=False)
    coding_mode = Column(Enum(CodingMode), nullable=False)
    context_strategy = Column(Enum(ContextStrategy), nullable=False)
    max_history_length = Column(Integer, nullable=False)
    ast_token_limit = Column(Integer, nullable=False)
    coding_llm_settings_id = Column(Integer, ForeignKey("llm_settings.id"), nullable=False)

    coding_llm_settings = relationship("LLMSettings", foreign_keys=[coding_llm_settings_id])


class LLMSettings(Base):
    __tablename__ = "llm_settings"

    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    context_window = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("model_name", "temperature", name="_model_temperature_uc"),)