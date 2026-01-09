from pydantic import BaseModel

class ServiceCreate(BaseModel):
    name: str
    description: str
    student_price: float
    general_price: float


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    student_price: float | None = None
    general_price: float | None = None
    is_active: bool | None = None
