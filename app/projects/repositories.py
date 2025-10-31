from sqlalchemy import select
from sqlalchemy.orm import Session

from app.commons.repositories import BaseRepository
from app.projects.exceptions import MultipleActiveProjectsException
from app.projects.models import Project


class ProjectRepository(BaseRepository[Project]):
    model = Project

    def __init__(self, db: Session):
        super().__init__(db)

    def list(self) -> list[Project]:
        return list(self.db.execute(select(self.model).order_by(self.model.name)).scalars().all())

    def get_active(self) -> Project | None:
        active_projects = self.db.execute(select(self.model).where(self.model.is_active)).scalars().all()
        if len(active_projects) > 1:
            raise MultipleActiveProjectsException("Multiple active projects found.")
        return active_projects[0] if active_projects else None
