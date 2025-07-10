from pydantic import BaseModel

class KeywordCreate(BaseModel):
    word: str

class KeywordResponse(BaseModel):
    id: int
    word: str

    class Config:
        from_attribute = True
