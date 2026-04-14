import uuid
from datetime import date, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.engine import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(200))
    dob: Mapped[date]
    gender: Mapped[str] = mapped_column(String(10))
    email: Mapped[str | None] = mapped_column(String(200), nullable=True, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
