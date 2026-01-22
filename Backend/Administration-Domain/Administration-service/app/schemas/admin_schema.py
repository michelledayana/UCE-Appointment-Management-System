from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime

class AuditEvent(BaseModel):
    event: str
    source: str
    timestamp: datetime
    payload: Dict[str, Any]
