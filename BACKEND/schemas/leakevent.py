from pydantic import BaseModel
from datetime import datetime

class LeakEventCreate(BaseModel):
    title: str
    description: str
    severity: str  # can be validated later (Low, Medium, High)

class LeakEventResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    created_at: datetime

    class Config:
        orm_mode = True
