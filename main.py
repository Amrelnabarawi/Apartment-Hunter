#!/usr/bin/env python3
"""
🏠 Apartment Hunter AI — Freiburg im Breisgau
==============================================
Monitors ImmoScout24, WG-Gesucht, Immowelt,
eBay Kleinanzeigen & Wohnverdient automatically.
Sends WhatsApp + Email alerts for good listings.

Usage:
    python main.py              # Run once
    python main.py --loop       # Run continuously (every N minutes)
    python main.py --test       # Test notifications only
"""

import json
import logging
import time
import argparse
from datetime import datetime

from database import init_db, listing_exists, save_listing, make_id
from scrapers import run_all_scrapers
from ai_filter import filter_listings
from notifier import notify
from backup import run_backup

# ── Logging Setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("apartment_hunter.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def load_config(path="config.json") -> dict:
    """Load config from file, override with env vars if set (GitHub Actions)."""
    import os
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    if os.getenv("ANTHROPIC_API_KEY"):
        config["ai"]["anthropic_api_key"] = os.getenv("ANTHROPIC_API_KEY")
    if os.getenv("EMAIL_SENDER"):
        config["notifications"]["email"]["sender_email"] = os.getenv("EMAIL_SENDER")
        config["notifications"]["email"]["recipient_email"] = os.getenv("EMAIL_RECIPIENT", os.getenv("EMAIL_SENDER"))
    if os.getenv("EMAIL_PASSWORD"):
        config["notifications"]["email"]["sender_password"] = os.getenv("EMAIL_PASSWORD")
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        config["notifications"]["telegram"]["bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
    if os.getenv("TELEGRAM_CHAT_ID"):
        config["notifications"]["telegram"]["chat_id"] = os.getenv("TELEGRAM_CHAT_ID")
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        config["notifications"]["telegram"]["bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
    if os.getenv("TELEGRAM_CHAT_ID"):
        config["notifications"]["telegram"]["chat_id"] = os.getenv("TELEGRAM_CHAT_ID")
    return config


def run_once(config: dict):
    logger.info("=" * 60)
    logger.info(f"🔍 Starting scan at {datetime.now().strftime('%H:%M:%S')}")
    logger.info("=" * 60)

    # 1. Scrape all sites
    all_listings = run_all_scrapers(config)
    logger.info(f"📦 Total raw listings fetched: {len(all_listings)}")

    # 2. Filter out already-seen
    new_listings = [l for l in all_listings if not listing_exists(l["id"])]
    logger.info(f"🆕 New listings (not seen before): {len(new_listings)}")

    if not new_listings:
        logger.info("Nothing new. Will check again later.")
        return

    # 3. AI evaluation & filtering
    good_listings = filter_listings(new_listings, config)
    logger.info(f"✅ Listings passing AI filter: {len(good_listings)}")

    # 4. Notify & save
    for listing in good_listings:
        try:
            notify(listing, config)
            save_listing(listing)
            logger.info(f"💾 Saved & notified: {listing['title']}")
        except Exception as e:
            logger.error(f"Error processing {listing['id']}: {e}")

    # 5. Save all seen (even bad ones) so we don't re-evaluate them
    for listing in new_listings:
        if not any(g["id"] == listing["id"] for g in good_listings):
            # Save with score=0 so we skip it next time
            listing.setdefault("ai_score", 0)
            listing.setdefault("ai_summary", "لم يجتز الفلتر")
            save_listing(listing)

    logger.info(f"✨ Scan complete. Found {len(good_listings)} good listings.")

    # Run backup system
    run_backup(config)


def test_notifications(config: dict):
    """Send a test notification to verify setup."""
    dummy = {
        "id": "test_123",
        "title": "Test: Schöne 2-Zimmer Wohnung in Freiburg-Altstadt",
        "price": 950,
        "size": 52,
        "rooms": 2,
        "address": "Münsterplatz 1, 79098 Freiburg im Breisgau",
        "url": "https://www.immobilienscout24.de",
        "source": "TEST",
        "ai_score": 9,
        "ai_summary": "هذا إشعار تجريبي – الأداة تعمل بشكل صحيح! 🎉",
        "recommended": True,
    }
    logger.info("Sending test notifications...")
    notify(dummy, config)
    logger.info("Done! Check your email and WhatsApp.")


def main():
    parser = argparse.ArgumentParser(description="Apartment Hunter AI")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--test", action="store_true", help="Send test notification")
    parser.add_argument("--config", default="config.json", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)
    init_db()

    if args.test:
        test_notifications(config)
        return

    if args.loop:
        interval = config["scraper"]["interval_minutes"] * 60
        logger.info(f"🔄 Running in loop mode every {config['scraper']['interval_minutes']} minutes")
        while True:
            try:
                run_once(config)
            except Exception as e:
                logger.error(f"Scan error: {e}")
            logger.info(f"😴 Sleeping {config['scraper']['interval_minutes']} minutes...")
            time.sleep(interval)
    else:
        run_once(config)


if __name__ == "__main__":
    main()
