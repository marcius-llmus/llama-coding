from sqlalchemy.orm import Session
from app.core.db import engine


def get_db():
    """
    FastAPI dependency that provides a transactional database session.
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
