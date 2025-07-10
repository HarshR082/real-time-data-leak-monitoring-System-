import asyncio
from scraper.pastebin_scraper import fetch_public_pastes
from database import SessionLocal
from models.leakevent import LeakEvent

def start_scheduler():
    # Runs in the background
    import threading
    threading.Thread(target=run_scraper_loop, daemon=True).start()

def run_scraper_loop():
    import time
    while True:
        print("[Scheduler] Starting scrape cycle...")
        asyncio.run(run_scraper_once())
        time.sleep(3600)  # Run hourly

async def run_scraper_once():
    print("[Scheduler] Running scrape task...")
    new_pastes = await fetch_public_pastes()

    db = SessionLocal()
    for paste in new_pastes:
        exists = db.query(LeakEvent).filter(LeakEvent.source == paste["source"]).first()
        if exists:
            continue

        event = LeakEvent(
            title=paste["title"],
            description=paste["description"],
            severity=paste["severity"],
            source=paste["source"]
        )
        db.add(event)
    db.commit()
    db.close()
    print(f"[Scheduler] Inserted {len(new_pastes)} new pastes.")
