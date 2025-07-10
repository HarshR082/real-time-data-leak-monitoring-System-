from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.keyword import Keyword
from schemas.keyword import KeywordCreate, KeywordResponse
from database import get_db
from routes.auth import get_current_user
from models.user import User

router = APIRouter()

@router.post("/", response_model=KeywordResponse)
def create_keyword(keyword: KeywordCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_keyword = Keyword(word=keyword.word, user_id=user.id)
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)
    return new_keyword

@router.get("/", response_model=List[KeywordResponse])
def list_keywords(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Keyword).filter(Keyword.user_id == user.id).all()

@router.delete("/{keyword_id}")
def delete_keyword(keyword_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    keyword = db.query(Keyword).filter(Keyword.id == keyword_id, Keyword.user_id == user.id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    db.delete(keyword)
    db.commit()
    return {"detail": "Keyword deleted"}
