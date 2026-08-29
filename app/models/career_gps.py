from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CareerProgress(Base):
    __tablename__ = "career_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    career_path: Mapped[str] = mapped_column(String(80), default="Full Stack")
    goal_role: Mapped[str | None] = mapped_column(String(160), nullable=True)
    target_company: Mapped[str | None] = mapped_column(String(160), nullable=True)
    readiness_score: Mapped[int] = mapped_column(Integer, default=0)
    company_readiness: Mapped[int] = mapped_column(Integer, default=0)
    role_readiness: Mapped[int] = mapped_column(Integer, default=0)
    estimated_learning_days: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class CareerGoal(Base):
    __tablename__ = "career_goals"
    __table_args__ = (UniqueConstraint("user_id", "goal_key", name="uq_career_goal"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    goal_key: Mapped[str] = mapped_column(String(80))
    goal_value: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
