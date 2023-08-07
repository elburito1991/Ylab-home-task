import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.submenus.models import Submenus


class Menus(Base):
    __tablename__ = 'menus'

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    submenus_count: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    dishes_count: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    submenus: Mapped[list['Submenus']] = relationship(back_populates='menu')
