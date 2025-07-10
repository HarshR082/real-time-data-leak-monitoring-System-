from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.alert import Alert
from schemas.alert import AlertResponse
from routes.auth import get_current_user
from models.user import User

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get all alerts for the authenticated user
    """
    return db.query(Alert).filter(Alert.user_id == user.id).all()
