"""
🔒 Backup System — Apartment Hunter AI
=======================================
3 levels of backup:
1. Local backup: copies apartments.db to backups/ folder daily
2. Daily email summary: sends all found listings to your email every morning
3. GitHub Artifact: the workflow uploads the DB as artifact (90 days retention)
"""

import sqlite3
import json
import shutil
import os
import logging
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)
DB_FILE = "apartments.db"
BACKUP_DIR = "backups"


# ─────────────────────────────────────────────
# 1. Local DB Backup
# ─────────────────────────────────────────────
def backup_database():
    """Copy apartments.db to backups/apartments_YYYY-MM-DD.db"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    backup_path = os.path.join(BACKUP_DIR, f"apartments_{today}.db")

    if os.path.exists(DB_FILE):
        shutil.copy2(DB_FILE, backup_path)
        logger.info(f"✅ Database backed up to: {backup_path}")

        # Keep only last 7 backups
        backups = sorted([
            f for f in os.listdir(BACKUP_DIR)
            if f.startswith("apartments_") and f.endswith(".db")
        ])
        while len(backups) > 7:
            old = os.path.join(BACKUP_DIR, backups.pop(0))
            os.remove(old)
            logger.info(f"🗑️ Removed old backup: {old}")
    else:
        logger.warning("No database found to backup yet.")

    return backup_path if os.path.exists(DB_FILE) else None


# ─────────────────────────────────────────────
# 2. Get stats from database
# ─────────────────────────────────────────────
def get_stats():
    """Return summary statistics from the database."""
    if not os.path.exists(DB_FILE):
        return {}

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM listings")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM listings WHERE ai_score >= 6")
    good = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM listings WHERE found_at >= datetime('now', '-24 hours')")
    last_24h = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM listings WHERE found_at >= datetime('now', '-24 hours') AND ai_score >= 6")
    good_24h = c.fetchone()[0]

    c.execute("""
        SELECT title, price, size, rooms, address, url, source, ai_score, ai_summary, found_at
        FROM listings
        WHERE ai_score >= 7
        ORDER BY found_at DESC
        LIMIT 10
    """)
    top_listings = c.fetchall()

    c.execute("""
        SELECT source, COUNT(*) as cnt
        FROM listings
        GROUP BY source
        ORDER BY cnt DESC
    """)
    by_source = c.fetchall()

    conn.close()

    return {
        "total": total,
        "good": good,
        "last_24h": last_24h,
        "good_24h": good_24h,
        "top_listings": top_listings,
        "by_source": by_source,
    }


# ─────────────────────────────────────────────
# 3. Daily Summary Email
# ─────────────────────────────────────────────
def send_daily_summary(config: dict):
    """Send a beautiful daily summary email with all stats and top listings."""
    cfg = config["notifications"]["email"]
    if not cfg.get("enabled"):
        return

    stats = get_stats()
    if not stats:
        logger.warning("No stats available for summary email.")
        return

    today = datetime.now().strftime("%A, %d %B %Y")

    # Build listings HTML
    listings_html = ""
    if stats["top_listings"]:
        for row in stats["top_listings"]:
            title, price, size, rooms, address, url, source, score, summary, found_at = row
            score_stars = "⭐" * min(int(score or 0), 10)
            found_date = found_at[:16] if found_at else ""
            listings_html += f"""
            <div style="background:#f8f9fa;border-radius:10px;padding:16px;margin-bottom:12px;
                        border-right:4px solid {'#2E7D32' if score >= 8 else '#F57F17'}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div style="font-weight:700;font-size:15px;color:#1a1a1a;flex:1">{title}</div>
                <div style="font-weight:900;color:{'#2E7D32' if score >= 8 else '#F57F17'};font-size:18px;margin-right:10px">{score}/10</div>
              </div>
              <div style="color:#666;font-size:13px;margin:6px 0">{score_stars}</div>
              <div style="display:flex;gap:16px;margin:8px 0;flex-wrap:wrap">
                <span style="color:#C62828;font-weight:700">💰 {price:.0f}€/Monat</span>
                <span style="color:#1565C0">📐 {size:.0f}m²</span>
                <span style="color:#4527A0">🚪 {rooms} Zimmer</span>
                <span style="color:#666;font-size:12px">🌐 {source}</span>
              </div>
              <div style="color:#555;font-size:13px;margin-bottom:8px">📍 {address}</div>
              <div style="color:#388E3C;font-size:13px;margin-bottom:10px;font-style:italic">🤖 {summary}</div>
              <div style="color:#888;font-size:11px;margin-bottom:10px">🕐 {found_date}</div>
              <a href="{url}" style="background:#2E7D32;color:white;padding:8px 16px;
                 border-radius:6px;text-decoration:none;font-size:13px;font-weight:700">
                👁️ شوف الإعلان
              </a>
            </div>
            """
    else:
        listings_html = '<div style="text-align:center;color:#999;padding:20px">لم يتم العثور على شقق ممتازة حتى الآن</div>'

    # Build sources HTML
    sources_html = ""
    for source, cnt in stats["by_source"]:
        sources_html += f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #eee"><span>{source}</span><strong>{cnt}</strong></div>'

    html = f"""
    <html><body style="font-family:Arial,sans-serif;direction:rtl;background:#f0f2f5;padding:20px;margin:0">
    <div style="max-width:620px;margin:auto">

      <!-- Header -->
      <div style="background:linear-gradient(135deg,#1a237e,#283593);border-radius:14px;
                  padding:24px;margin-bottom:16px;color:white;text-align:center">
        <div style="font-size:36px;margin-bottom:8px">🏠</div>
        <div style="font-size:22px;font-weight:800">Apartment Hunter AI</div>
        <div style="font-size:14px;opacity:0.8;margin-top:4px">التقرير اليومي — {today}</div>
        <div style="font-size:12px;opacity:0.6;margin-top:2px">Freiburg im Breisgau • 40–70m² • حتى 1000€</div>
      </div>

      <!-- Stats -->
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin-bottom:16px">
        {''.join([f'''
        <div style="background:white;border-radius:10px;padding:14px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
          <div style="font-size:24px">{item[0]}</div>
          <div style="font-size:22px;font-weight:800;color:{item[2]}">{item[1]}</div>
          <div style="font-size:11px;color:#999;margin-top:2px">{item[3]}</div>
        </div>''' for item in [
            ("📦", stats['total'], "#1565C0", "إجمالي الإعلانات"),
            ("✅", stats['good'], "#2E7D32", "إعلانات كويسة"),
            ("🆕", stats['last_24h'], "#E65100", "آخر 24 ساعة"),
            ("⭐", stats['good_24h'], "#F9A825", "كويسة اليوم"),
        ]])}
      </div>

      <!-- Top Listings -->
      <div style="background:white;border-radius:14px;padding:20px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:17px;font-weight:800;margin-bottom:16px;color:#1a237e">
          🏆 أفضل الشقق المكتشفة (تقييم 7+)
        </div>
        {listings_html}
      </div>

      <!-- Sources -->
      <div style="background:white;border-radius:14px;padding:20px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:15px;font-weight:700;margin-bottom:12px;color:#333">📊 الإعلانات حسب الموقع</div>
        {sources_html}
      </div>

      <!-- Backup notice -->
      <div style="background:#E8F5E9;border-radius:10px;padding:14px;text-align:center;margin-bottom:16px">
        <div style="color:#2E7D32;font-size:13px">
          ✅ قاعدة البيانات محفوظة تلقائياً على GitHub كـ Artifact لمدة 90 يوم
        </div>
      </div>

      <!-- Footer -->
      <div style="text-align:center;color:#aaa;font-size:11px">
        تم الإرسال تلقائياً بواسطة Apartment Hunter AI •
        {datetime.now().strftime('%d/%m/%Y %H:%M')}
      </div>
    </div>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🏠 تقرير يومي — وجدنا {stats['good_24h']} شقة كويسة اليوم!"
        msg["From"] = cfg["sender_email"]
        msg["To"] = cfg["recipient_email"]
        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["sender_email"], cfg["sender_password"])
            server.sendmail(cfg["sender_email"], cfg["recipient_email"], msg.as_string())

        logger.info("📊 Daily summary email sent!")
    except Exception as e:
        logger.error(f"Summary email error: {e}")


# ─────────────────────────────────────────────
# Run all backups
# ─────────────────────────────────────────────
def run_backup(config: dict):
    """Run all backup tasks."""
    logger.info("🔒 Running backup system...")

    # 1. Local backup
    backup_database()

    # 2. Daily summary email (once per day at 8am)
    hour = datetime.now().hour
    if hour == 8:
        logger.info("📧 Sending daily summary email (8am)...")
        send_daily_summary(config)
    else:
        logger.info(f"⏭️ Skipping daily email (hour={hour}, sends at 8am)")

    logger.info("✅ Backup complete.")
