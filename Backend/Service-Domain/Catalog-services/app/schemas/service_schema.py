from pydantic import BaseModel
from typing import Optional

class ServiceCreate(BaseModel):
    name: str
    category: str
    description: str
    student_price: float
    general_price: float

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    student_price: Optional[float] = None
    general_price: Optional[float] = None
    is_active: Optional[bool] = None
