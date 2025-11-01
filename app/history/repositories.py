from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.commons.repositories import BaseRepository
from app.history.models import ChatSession


class ChatSessionRepository(BaseRepository[ChatSession]):
    model = ChatSession

    def __init__(self, db: Session):
        super().__init__(db)

    def list_by_project(self, project_id: int) -> list[ChatSession]:
        return list(
            self.db.execute(
                select(self.model)
                .where(self.model.project_id == project_id)
                .options(joinedload(self.model.messages))
                .order_by(self.model.created_at.desc())
            )
            .scalars()
            .all()
        )