from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_roles
from app.db.database import get_db
from app.models.resume_history import ResumeHistory
from app.models.user import Role, User

router = APIRouter(prefix="/users", tags=["Users"])

class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)

@router.get("/me/profile")
def profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"id": user.id, "full_name": user.full_name, "email": user.email, "role": user.role.value, "joined_date": user.created_at, "last_login": user.last_login, "uploaded_resume_count": db.query(ResumeHistory).filter_by(user_id=user.id).count()}

@router.patch("/me")
def update_profile(data: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.full_name = data.full_name.strip(); db.commit(); db.refresh(user)
    return {"id": user.id, "full_name": user.full_name}

@router.get("/")
def list_users(_: User = Depends(require_roles(Role.ADMIN)), db: Session = Depends(get_db)):
    return [{"id": u.id, "full_name": u.full_name, "email": u.email, "role": u.role.value, "is_active": u.is_active, "created_at": u.created_at} for u in db.query(User).order_by(User.created_at.desc()).all()]

@router.post("/{user_id}/deactivate")
def deactivate(user_id: int, admin: User = Depends(require_roles(Role.ADMIN)), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    if user.id == admin.id: raise HTTPException(400, "Administrators cannot deactivate themselves")
    user.is_active = False; db.commit()
    return {"status": "deactivated"}
