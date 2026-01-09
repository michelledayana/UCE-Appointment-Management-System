from pydantic import BaseModel, root_validator
from typing import Optional


class UserProfileUpdate(BaseModel):
    phone: Optional[str] = None
    faculty: Optional[str] = None
    career: Optional[str] = None
    semester: Optional[int] = None


class UserProfileResponse(BaseModel):
    email: str
    full_name: str
    user_type: str

    phone: Optional[str] = None
    faculty: Optional[str] = None
    career: Optional[str] = None
    semester: Optional[int] = None

    class Config:
        from_attributes = True

    @root_validator
    def hide_student_fields(cls, values):
        if values.get("user_type") != "STUDENT":
            values["faculty"] = None
            values["career"] = None
            values["semester"] = None
        return values
