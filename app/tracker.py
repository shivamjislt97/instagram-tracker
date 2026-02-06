from datetime import datetime
from pathlib import Path

from app.database import engine, SessionLocal
from app.models import Base, Profile, ProfileHistory
from app.scraper import fetch_profile
from app.utils import text_hash, image_hash, download_image
from app.telegram_alert import send_telegram_photo
from app.hd_dp import download_hd_dp


import os
from dotenv import load_dotenv

load_dotenv()

TEST_URL = os.getenv("INSTAGRAM_URL")


def start_tracker():

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    profile = db.query(Profile).filter_by(instagram_url=TEST_URL).first()
    if not profile:
        username = TEST_URL.rstrip("/").split("/")[-1]
        profile = Profile(instagram_url=TEST_URL, username=username)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    data = fetch_profile(TEST_URL)

    if not data or not data.get("image"):
        print("⚠️ Instagram blocked / no data. Skipping this run.")
        db.close()
        return

    bio = data.get("bio")
    image_url = data.get("image")

    bio_h = text_hash(bio)

    last = (
        db.query(ProfileHistory)
        .filter_by(profile_id=profile.id)
        .order_by(ProfileHistory.checked_at.desc())
        .first()
    )

    img_path = Path("images") / profile.username / f"profile_{datetime.utcnow().date()}.jpg"
    img_bytes = download_image(image_url, img_path)
    img_h = image_hash(img_bytes)

    changed = (
        not last
        or last.bio_hash != bio_h
        or last.image_hash != img_h
    )

    if not changed:
        print("ℹ️ No change detected")
        db.close()
        return

    history = ProfileHistory(
        profile_id=profile.id,
        bio=bio,
        bio_hash=bio_h,
        image_path=str(img_path),
        image_hash=img_h,
        checked_at=datetime.utcnow(),
    )
    db.add(history)
    db.commit()

    print("🚀 Downloading HD DP")
    hd_image_path = download_hd_dp(profile.username)

    if hd_image_path:
        caption = (
            f"🔔 DP Updated (HD)\n"
            f"🧑 Username: {profile.username}\n\n"
            f"📝 Bio:\n{bio[:900] if bio else ''}"
        )

        send_telegram_photo(hd_image_path, caption=caption)
        print("📤 Sent image to Telegram")

    db.close()
