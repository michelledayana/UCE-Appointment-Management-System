from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import UserProfile
from app.schemas.user import UserProfileUpdate, UserProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("", response_model=list[UserProfileResponse])
def get_all_profiles(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@router.get("/{email}", response_model=UserProfileResponse)
def get_user_profile(email: str, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(
        UserProfile.email == email
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/{email}")
def update_profile(
    email: str,
    data: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(
        UserProfile.email == email
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return {"message": "Profile updated successfully"}

