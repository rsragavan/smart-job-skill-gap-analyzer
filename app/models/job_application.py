from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="Applied",
        index=True,
    )
    source_type = Column(String(20), nullable=False, default="scraped")
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    company_role_id = Column(Integer, ForeignKey("company_roles.id", ondelete="SET NULL"), nullable=True, index=True)
    current_selection_round = Column(String(150), nullable=True)
    current_round_number = Column(Integer, nullable=True)
    interview_date = Column(DateTime(timezone=True), nullable=True)
    custom_company_name = Column(String(255), nullable=True)
    custom_job_title = Column(String(255), nullable=True)
    custom_location = Column(String(255), nullable=True)
    custom_job_url = Column(String(500), nullable=True)

    notes = Column(
        Text,
        nullable=True,
    )

    applied_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    user = relationship("User", back_populates="applications")

    job = relationship("Job", back_populates="applications")


class ApplicationTimeline(Base):
    __tablename__ = "application_timeline"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), nullable=False)
    notes = Column(Text, nullable=True)
    progress_percentage = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)


class ApplicationStageHistory(Base):
    __tablename__ = "application_stage_history"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    previous_stage = Column(String(30), nullable=True)
    new_stage = Column(String(30), nullable=False)
    changed_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
