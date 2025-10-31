from sqlalchemy import select
from sqlalchemy.orm import Session

from app.commons.repositories import BaseRepository
from app.prompts.models import Prompt
from app.prompts.enums import PromptType


class PromptRepository(BaseRepository[Prompt]):
    model = Prompt

    def __init__(self, db: Session):
        super().__init__(db)

    def list_global(self) -> list[Prompt]:
        return list(
            self.db.execute(
                select(self.model).where(self.model.project_id.is_(None), self.model.type == PromptType.GLOBAL).order_by(self.model.name)
            )
            .scalars()
            .all()
        )

    def list_by_project(self, project_id: int) -> list[Prompt]:
        return list(
            self.db.execute(
                select(self.model).where(self.model.project_id == project_id, self.model.type == PromptType.PROJECT).order_by(self.model.name)
            )
            .scalars()
            .all()
        )

    def list_template_apps(self) -> list[Prompt]:
        return list(
            self.db.execute(select(self.model).where(self.model.type == PromptType.TEMPLATE_APP).order_by(self.model.name))
            .scalars()
            .all()
        )
