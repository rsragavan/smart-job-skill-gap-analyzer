from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ResumeHistory(Base):
    __tablename__ = "resume_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Store skills as a comma-separated string or JSON string
    extracted_skills: Mapped[str] = mapped_column(
        String(2000),
        nullable=False
    )

    # Number of recommended jobs
    recommended_jobs: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<ResumeHistory("
            f"id={self.id}, "
            f"filename='{self.filename}', "
            f"recommended_jobs={self.recommended_jobs})>"
        )
