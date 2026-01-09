from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.appointment import UserProfile
from schemas.appointment import UserProfileUpdate, UserProfileResponse

router = APIRouter(prefix="/profile", tags=["Profiles"])

@router.get("/{email}", response_model=UserProfileResponse)
def get_profile(email: str, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.email == email).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/{email}", response_model=UserProfileResponse)
def update_profile(email: str, profile_data: UserProfileUpdate, db: Session = Depends(get_db)):
    profile_query = db.query(UserProfile).filter(UserProfile.email == email)
    profile = profile_query.first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields provided in the request
    update_dict = profile_data.dict(exclude_unset=True)
    profile_query.update(update_dict)
    db.commit()
    return profile_query.first()