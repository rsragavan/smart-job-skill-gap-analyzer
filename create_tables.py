from app.db.database import Base, engine

# Import all models
from app.models.auth import PasswordResetToken, RefreshToken
from app.models.company import Company
from app.models.company_intelligence import CompanyInsight, CompanyInterviewQuestion, CompanyLocation, CompanyPreparation, CompanyResource, CompanyRole, CompanySelectionProcess, CompanySkill, StartupFunding, StartupInformation, StartupRole
from app.models.mock_interview import AssessmentAttempt, CodingAssessment, MockInterview, MockInterviewQuestion
from app.models.job import Job
from app.models.job_application import ApplicationStageHistory, ApplicationTimeline, JobApplication
from app.models.learning_progress import LearningProgress
from app.models.gamification import Achievement, GamificationEvent, UserBadge, UserGamification
from app.models.career_gps import CareerGoal, CareerProgress
from app.models.resume_history import ResumeHistory
from app.models.unknown_skill import UnknownSkill
from app.models.user import User
from app.models.user_target import UserTarget
from app.models.content import CodingQuestion, InterviewQuestion, LearningResource

_ = (
    PasswordResetToken,
    RefreshToken,
    Company,
    CompanyLocation,
    CompanyRole,
    CompanySelectionProcess,
    CompanyPreparation,
    CompanySkill,
    CompanyInterviewQuestion,
    CompanyResource,
    CompanyInsight,
    StartupInformation,
    StartupFunding,
    StartupRole,
    MockInterview,
    MockInterviewQuestion,
    CodingAssessment,
    AssessmentAttempt,
    Job,
    JobApplication,
    ApplicationTimeline,
    ApplicationStageHistory,
    LearningProgress,
    Achievement,
    GamificationEvent,
    UserBadge,
    UserGamification,
    CareerGoal,
    CareerProgress,
    ResumeHistory,
    UnknownSkill,
    User,
    UserTarget,
    CodingQuestion,
    InterviewQuestion,
    LearningResource,
)

from app.db.init_db import create_schema
create_schema()

print("All tables created successfully.")
