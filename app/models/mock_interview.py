from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MockInterview(Base):
    __tablename__ = "mock_interviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    company_role_id: Mapped[int | None] = mapped_column(ForeignKey("company_roles.id", ondelete="SET NULL"), nullable=True, index=True)
    company_name: Mapped[str | None] = mapped_column(String(150))
    role_title: Mapped[str | None] = mapped_column(String(150))
    interview_type: Mapped[str] = mapped_column(String(40), index=True)
    experience_level: Mapped[str] = mapped_column(String(30), default="mid")
    status: Mapped[str] = mapped_column(String(20), default="in_progress", index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    overall_score: Mapped[int | None] = mapped_column(Integer)
    technical_score: Mapped[int | None] = mapped_column(Integer)
    communication_score: Mapped[int | None] = mapped_column(Integer)
    problem_solving_score: Mapped[int | None] = mapped_column(Integer)
    confidence_score: Mapped[int | None] = mapped_column(Integer)
    hr_score: Mapped[int | None] = mapped_column(Integer)
    strengths: Mapped[list | None] = mapped_column(JSON)
    weaknesses: Mapped[list | None] = mapped_column(JSON)
    recommended_skills: Mapped[list | None] = mapped_column(JSON)
    next_steps: Mapped[list | None] = mapped_column(JSON)
    feedback: Mapped[str | None] = mapped_column(Text)


class MockInterviewQuestion(Base):
    __tablename__ = "mock_interview_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    interview_id: Mapped[int] = mapped_column(ForeignKey("mock_interviews.id", ondelete="CASCADE"), index=True)
    source_question_id: Mapped[int | None] = mapped_column(ForeignKey("company_interview_questions.id", ondelete="SET NULL"), nullable=True)
    sequence: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(50))
    topic: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    difficulty: Mapped[str | None] = mapped_column(String(20), nullable=True)
    skill: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    question: Mapped[str] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(30), default="CURATED")
    recommendation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    answer: Mapped[str | None] = mapped_column(Text)
    score: Mapped[int | None] = mapped_column(Integer)
    feedback: Mapped[str | None] = mapped_column(Text)


class CodingAssessment(Base):
    __tablename__ = "coding_assessments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150))
    difficulty: Mapped[str] = mapped_column(String(20), index=True)
    time_limit_minutes: Mapped[int] = mapped_column(Integer)
    question_count: Mapped[int] = mapped_column(Integer)
    pass_percentage: Mapped[int] = mapped_column(Integer, default=60)
    topics: Mapped[list] = mapped_column(JSON, default=list)


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("coding_assessments.id", ondelete="CASCADE"), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    company_role_id: Mapped[int | None] = mapped_column(ForeignKey("company_roles.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="in_progress")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    answers: Mapped[dict | None] = mapped_column(JSON)
    score: Mapped[int | None] = mapped_column(Integer)
    passed: Mapped[bool | None] = mapped_column(Boolean)
    percentage: Mapped[int | None] = mapped_column(Integer)


class CodingAttempt(Base):
    """Immutable-ish audit record for IDE executions and submissions."""
    __tablename__ = "coding_attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("coding_questions.id", ondelete="CASCADE"), index=True)
    language: Mapped[str] = mapped_column(String(20))
    code: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), index=True)
    runtime_ms: Mapped[int | None] = mapped_column(Integer)
    passed_tests: Mapped[int] = mapped_column(Integer, default=0)
    failed_tests: Mapped[int] = mapped_column(Integer, default=0)
    total_tests: Mapped[int] = mapped_column(Integer, default=0)
    output: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)
    is_submission: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True)
