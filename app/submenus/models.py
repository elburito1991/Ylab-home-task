import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.dishes.models import Dishes
    from app.menus.models import Menus


class Submenus(Base):
    __tablename__ = "submenus"

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    dishes_count: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    menu_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("menus.id", ondelete="CASCADE", onupdate="CASCADE"),

    )
    menu: Mapped["Menus"] = relationship(back_populates="submenus")
    dishes: Mapped[list["Dishes"]] = relationship(
        back_populates="submenus"
    )
