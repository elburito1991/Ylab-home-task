from pydantic import BaseModel


class SMenuAddIn(BaseModel):
    title: str
    description: str


class SMenuAddOut(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class SMenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
