import schedule
import time
from app.tracker import start_tracker

schedule.every(30).minutes.do(start_tracker)

print("🚀 Bot started (production mode)")

while True:
    schedule.run_pending()
    time.sleep(10)
