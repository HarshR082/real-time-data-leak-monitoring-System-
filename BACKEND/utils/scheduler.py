from apscheduler.schedulers.background import BackgroundScheduler
from scraper.my_scraper import scrape_new_leak_events
from database import SessionLocal
from models.leakevent import LeakEvent

def save_leak_events():
    print("[Scheduler] Running scrape job...")
    db = SessionLocal()
    try:
        new_events = scrape_new_leak_events()
        for event in new_events:
            exists = db.query(LeakEvent).filter(LeakEvent.title == event["title"]).first()
            if not exists:
                leak = LeakEvent(**event)
                db.add(leak)
        db.commit()
        print(f"[Scheduler] Saved {len(new_events)} new events.")
    except Exception as e:
        print("[Scheduler] Error:", e)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(save_leak_events, 'interval', minutes=30)  # every 30 mins
    scheduler.start()
    print("[Scheduler] Started background scraping job every 30 mins")
