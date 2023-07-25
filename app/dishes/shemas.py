from typing import Optional

from pydantic import BaseModel, field_validator


class SDishAddIn(BaseModel):
    title: str
    description: str
    price: float


class SDishAddOut(BaseModel):
    id: str
    title: str
    description: str
    price: float

    @field_validator("price", mode="plain")
    def round_float(cls, v):
        return f"{v:.2f}"


class SDishUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
