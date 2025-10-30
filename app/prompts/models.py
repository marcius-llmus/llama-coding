from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    project = relationship("Project", back_populates="prompts")
    project_attachments = relationship(
        "ProjectPromptAttachment", back_populates="prompt", cascade="all, delete-orphan"
    )
    session_attachments = relationship(
        "SessionPromptAttachment", back_populates="prompt", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("name", "project_id", name="_name_project_uc"),)


class ProjectPromptAttachment(Base):
    __tablename__ = "project_prompt_attachments"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), primary_key=True)

    project = relationship("Project", back_populates="prompt_attachments")
    prompt = relationship("Prompt", back_populates="project_attachments")


class SessionPromptAttachment(Base):
    __tablename__ = "session_prompt_attachments"

    session_id = Column(Integer, ForeignKey("chat_sessions.id"), primary_key=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), primary_key=True)

    session = relationship("ChatSession", back_populates="prompt_attachments")
    prompt = relationship("Prompt", back_populates="session_attachments")