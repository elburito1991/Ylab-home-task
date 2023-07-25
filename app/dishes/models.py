import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.submenus.models import Submenus


class Dishes(Base):
    __tablename__ = "dishes"

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    submenu_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("submenus.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    submenus: Mapped["Submenus"] = relationship(back_populates="dishes")

