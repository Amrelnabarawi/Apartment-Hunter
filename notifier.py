"""
Notifications via Outlook email + Telegram (replaces Gmail + WhatsApp).
"""

import smtplib
import urllib.request
import urllib.parse
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────
# Outlook Email (smtp.gmail.com)
# ─────────────────────────────────────────────────
def send_email(listing: dict, config: dict):
    cfg = config["notifications"]["email"]
    if not cfg.get("enabled"):
        return

    subject = f"🏠 New apartment in Freiburg! {listing['ai_score']}/10 – {listing['source']}"

    html = f"""
    <html><body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:20px">
    <div style="background:white;border-radius:12px;padding:24px;max-width:600px;margin:auto;
                box-shadow:0 2px 12px rgba(0,0,0,0.08)">
      <h2 style="color:#2E7D32;margin-top:0">🏠 New apartment found by AI!</h2>

      <div style="background:#E8F5E9;border-radius:8px;padding:16px;margin-bottom:16px">
        <div style="font-size:28px;font-weight:bold;color:#1B5E20">
          AI Score: {listing['ai_score']}/10 {'⭐' * min(listing['ai_score'],10)}
        </div>
        <div style="color:#388E3C;margin-top:4px">{listing.get('ai_summary','')}</div>
      </div>

      <table style="width:100%;border-collapse:collapse">
        <tr><td style="padding:8px;color:#666;width:120px">📌 Title</td>
            <td style="padding:8px;font-weight:bold">{listing.get('title','')}</td></tr>
        <tr style="background:#f9f9f9">
            <td style="padding:8px;color:#666">💰 Rent</td>
            <td style="padding:8px;font-weight:bold;color:#C62828">{listing.get('price',0):.0f} € / Monat</td></tr>
        <tr><td style="padding:8px;color:#666">📐 Size</td>
            <td style="padding:8px">{listing.get('size',0):.0f} m²</td></tr>
        <tr style="background:#f9f9f9">
            <td style="padding:8px;color:#666">🚪 Rooms</td>
            <td style="padding:8px">{listing.get('rooms',0)} Zimmer</td></tr>
        <tr><td style="padding:8px;color:#666">📍 Address</td>
            <td style="padding:8px">{listing.get('address','')}</td></tr>
        <tr style="background:#f9f9f9">
            <td style="padding:8px;color:#666">🌐 Source</td>
            <td style="padding:8px">{listing.get('source','')}</td></tr>
      </table>

      <a href="{listing.get('url','')}"
         style="display:block;background:#2E7D32;color:white;text-align:center;
                padding:14px;border-radius:8px;text-decoration:none;font-size:18px;
                font-weight:bold;margin-top:20px">
        View Listing Now
      </a>

      <p style="color:#999;font-size:12px;margin-top:16px;text-align:center">
        Sent automatically on {datetime.now().strftime('%d/%m/%Y %H:%M')} by Apartment Hunter AI
      </p>
    </div>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = cfg["sender_email"]
        msg["To"] = cfg["recipient_email"]
        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(cfg["sender_email"], cfg["sender_password"])
            server.sendmail(cfg["sender_email"], cfg["recipient_email"], msg.as_string())

        logger.info(f"✉️  Email sent: {listing['title']}")
    except Exception as e:
        logger.error(f"Email error: {e}")


# ─────────────────────────────────────────────────
# Telegram Bot (free, no phone tricks needed)
# ─────────────────────────────────────────────────
def send_telegram(listing: dict, config: dict):
    cfg = config["notifications"]["telegram"]
    if not cfg.get("enabled"):
        return

    token = cfg["bot_token"]
    chat_id = cfg["chat_id"]

    score = listing.get('ai_score', 0)
    stars = "⭐" * min(score, 10)
    message = (
        f"🏠 *New Apartment in Freiburg!*\n\n"
        f"{stars} *AI Score: {score}/10*\n"
        f"📌 {listing.get('title','')}\n"
        f"💰 {listing.get('price',0):.0f}€/Monat\n"
        f"📐 {listing.get('size',0):.0f}m²  🚪 {listing.get('rooms',0)} Zimmer\n"
        f"📍 {listing.get('address','')}\n"
        f"🌐 {listing.get('source','')}\n\n"
        f"🤖 _{listing.get('ai_summary','')}_\n\n"
        f"🔗 [View Listing]({listing.get('url','')})"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info(f"📱 Telegram sent: {listing['title']}")
    except Exception as e:
        logger.error(f"Telegram error: {e}")


def notify(listing: dict, config: dict):
    send_email(listing, config)
    send_telegram(listing, config)


# ─────────────────────────────────────────────────
# Application letter to landlord
# ─────────────────────────────────────────────────
def send_application(landlord_email: str, listing: dict, config: dict):
    cfg_email = config["notifications"]["email"]
    applicant = config.get("applicant", {})
    cover_letter = applicant.get("cover_letter_de", "")
    subject = f"Bewerbung um die Wohnung: {listing.get('title', 'Wohnungsanzeige')}"

    html = f"""
    <html><body style="font-family:Arial,sans-serif;background:#f9f9f9;padding:20px">
    <div style="background:white;border-radius:12px;padding:32px;max-width:680px;
                margin:auto;box-shadow:0 2px 12px rgba(0,0,0,0.08)">
      <div style="white-space:pre-line;line-height:1.8;font-size:15px;color:#212121">
{cover_letter}
      </div>
    </div>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = cfg_email["sender_email"]
        msg["To"] = landlord_email
        msg["Reply-To"] = applicant.get("email", cfg_email["sender_email"])
        msg.attach(MIMEText(cover_letter, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP(cfg_email["smtp_server"], cfg_email["smtp_port"]) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(cfg_email["sender_email"], cfg_email["sender_password"])
            server.sendmail(cfg_email["sender_email"], landlord_email, msg.as_string())

        logger.info(f"📨 Application sent to {landlord_email}")
        return True
    except Exception as e:
        logger.error(f"Application error: {e}")
        return False
