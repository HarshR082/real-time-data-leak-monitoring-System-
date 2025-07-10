# schemas/alert.py
from pydantic import BaseModel

class AlertResponse(BaseModel):
    id: int
    user_id: int
    keyword: str
    snippet: str
    link: str
    source: str

    class Config:
        from_attributes = True
