from typing import Optional

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
    title: Optional[str] = None
    description: Optional[str] = None
