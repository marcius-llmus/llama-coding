from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    name: str
    path: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    path: str | None = None


class ProjectRead(ProjectBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
