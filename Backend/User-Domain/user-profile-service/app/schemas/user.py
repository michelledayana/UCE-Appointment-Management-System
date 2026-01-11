from pydantic import BaseModel
from typing import Optional


class UserProfileResponse(BaseModel):
    email: str
    full_name: str
    user_type: str

    phone: Optional[str] = None
    faculty: Optional[str] = None
    career: Optional[str] = None
    semester: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class UserProfileUpdate(BaseModel):
    phone: Optional[str] = None
    faculty: Optional[str] = None
    career: Optional[str] = None
    semester: Optional[int] = None
