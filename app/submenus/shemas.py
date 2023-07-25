from typing import Optional

from pydantic import BaseModel


class SSubmenuAddIn(BaseModel):
    title: str
    description: str


class SSubmenuAddOut(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int


class SSubmenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
