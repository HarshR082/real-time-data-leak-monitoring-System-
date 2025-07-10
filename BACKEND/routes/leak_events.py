from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from email.message import EmailMessage
import smtplib
import os

from models.leakevent import LeakEvent
from schemas.leakevent import LeakEventCreate, LeakEventResponse
from utils.security import get_db, get_current_user

router = APIRouter(
    prefix="/leak-events",
    tags=["Leak Events"]
)

def send_email(subject: str, body: str):
    try:
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_SENDER = os.getenv("your_email@gmail.com")
        EMAIL_PASSWORD = os.getenv("your_app_password")
        EMAIL_RECEIVER = os.getenv("yraj55636@gmail.com")

        msg = EmailMessage()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ✅ CREATE with email notification
@router.post("/", response_model=LeakEventResponse)
def create_leak_event(
    event: LeakEventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_event = LeakEvent(
        title=event.title,
        description=event.description,
        severity=event.severity
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    subject = f"New Leak Event Created: {new_event.title}"
    body = (
        f"A new leak event has been reported.\n\n"
        f"Title: {new_event.title}\n"
        f"Description: {new_event.description}\n"
        f"Severity: {new_event.severity}\n"
        f"Event ID: {new_event.id}\n"
    )
    background_tasks.add_task(send_email, subject, body)

    return new_event

# ✅ LIST with Search, Filters, Pagination
@router.get("/", response_model=List[LeakEventResponse])
def list_leak_events(
    search: Optional[str] = Query(None, description="Search in title/description"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(LeakEvent)

    if search:
        search_pattern = f"%{search.lower()}%"
        query = query.filter(
            (LeakEvent.title.ilike(search_pattern)) |
            (LeakEvent.description.ilike(search_pattern))
        )

    if severity:
        query = query.filter(LeakEvent.severity == severity)

    results = query.offset(offset).limit(limit).all()
    return results

# ✅ GET SINGLE
@router.get("/{event_id}", response_model=LeakEventResponse)
def get_leak_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    event = db.query(LeakEvent).filter(LeakEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Leak event not found")
    return event

# ✅ DELETE
@router.delete("/{event_id}")
def delete_leak_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    event = db.query(LeakEvent).filter(LeakEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Leak event not found")
    db.delete(event)
    db.commit()
    return {"message": "Leak event deleted successfully"}
