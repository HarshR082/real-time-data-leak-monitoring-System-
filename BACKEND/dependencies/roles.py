from fastapi import Depends, HTTPException, status
from models.user import User
from utils.security import get_current_user
from dependencies.roles import admin_required


def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
