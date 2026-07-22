from app.db.database import Base, engine

# Import all models
from app.models.company import Company
from app.models.job import Job
from app.models.resume_history import ResumeHistory
from app.models.user import User
from app.models.auth import PasswordResetToken, RefreshToken

Base.metadata.create_all(bind=engine)

print("All tables created successfully.")
