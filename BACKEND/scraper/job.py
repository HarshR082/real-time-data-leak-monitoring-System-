import asyncio
from scraper.pastebin_scraper import fetch_public_pastes
from scraper.utils import match_keywords
from scraper.email_utils import send_alert_email
from database import SessionLocal
from models.alert import Alert
from models.keyword import Keyword
from models.user import User

async def scraper_job():
    print("Running scraper job...")
    db = SessionLocal()
    try:
        # Fetch all keywords with user info
        keywords = db.query(Keyword).all()
        if not keywords:
            print("No keywords to match.")
            return

        # Group keywords by user
        user_keywords = {}
        for k in keywords:
            user_keywords.setdefault(k.user_id, []).append(k.word)

        pastes = await fetch_public_pastes()

        for paste in pastes:
            for user_id, words in user_keywords.items():
                matched_keywords = match_keywords(paste["content"], words)
                if matched_keywords:
                    user = db.query(User).filter(User.id == user_id).first()
                    if not user:
                        continue

                    for kw in matched_keywords:
                        # Save alert in DB
                        alert = Alert(
                            user_id=user.id,
                            keyword=kw,
                            source="Pastebin",
                            snippet=paste["content"][:200],
                            link=paste["link"]
                        )
                        db.add(alert)
                        db.commit()
                        db.refresh(alert)

                        # Send email
                        send_alert_email(
                            recipient_email=user.email,
                            keyword=kw,
                            snippet=paste["content"][:200],
                            link=paste["link"]
                        )
        print("Scraper job completed.")
    except Exception as e:
        print(f"Error during scraper job: {e}")
    finally:
        db.close()
