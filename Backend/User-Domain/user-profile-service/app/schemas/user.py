from pydantic import BaseModel
from datetime import datetime

class UserProfileResponse(BaseModel):
    id: int
    full_name: str
    email: str
    user_type: str
    created_at: datetime

    class Config:
        from_attributes = True
