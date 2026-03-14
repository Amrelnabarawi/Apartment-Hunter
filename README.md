# 🏠 Apartment Hunter AI — Freiburg im Breisgau

An automated apartment hunting tool that monitors 5 German rental websites 24/7, scores listings using AI, and sends instant notifications via Email and Telegram — even when your laptop is completely off.

---

## ✨ Features

- 🔍 **Monitors 5 websites** every hour automatically
- 🤖 **AI scoring** — each listing is rated 1–10 by Claude AI
- 📧 **Email + Telegram** notifications for good listings (score 6+)
- 📊 **Daily summary email** every morning at 8:00 AM
- 🔒 **3-level backup system** — local, GitHub cache, and 90-day artifacts
- 💌 **One-click application** — sends your German cover letter directly to landlords
- ☁️ **Runs in the cloud** via GitHub Actions — no laptop needed

---

## 🌐 Websites Monitored

| Website | Type |
|---------|------|
| ImmoScout24 | Germany's largest rental platform |
| Immowelt | Major rental platform |
| WG-Gesucht | Apartments and rooms |
| eBay Kleinanzeigen | Private listings |
| Wohnverdient.de | Additional listings |

---

## 🔎 Search Criteria

| Parameter | Value |
|-----------|-------|
| Location | Freiburg im Breisgau + 15km radius |
| Size | 40 – 70 m² |
| Rooms | 2 Zimmer |
| Cold rent | 500 – 700€ |
| Max warm rent | 1,000€ |
| Blacklist | WG, Tausch, Zwischenmiete, WG-Zimmer |

---

## ⚙️ How It Works

```
Every hour → GitHub Actions runs the tool
                    ↓
        Scrapes 5 websites for new listings
                    ↓
        AI filters and scores each listing
                    ↓
        Score 6+ ? → Email + Telegram sent ✅
        Score < 6 ? → Skipped ❌
                    ↓
        Database saved + backup uploaded
```

---

## 🚀 Setup

### Requirements
- GitHub account (free)
- Anthropic API key — console.anthropic.com
- Gmail account + App Password
- Telegram bot token + chat ID

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Claude AI API key |
| `EMAIL_SENDER` | Your Gmail address |
| `EMAIL_PASSWORD` | Gmail App Password (16 characters) |
| `EMAIL_RECIPIENT` | Email to receive alerts |
| `TELEGRAM_BOT_TOKEN` | Token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram user ID |

### Getting Your Telegram Credentials
1. Open Telegram → search **@BotFather** → send `/newbot`
2. Follow the steps → copy the **Bot Token**
3. Search **@userinfobot** → send any message → copy your **Chat ID**

### Getting Gmail App Password
1. Go to myaccount.google.com → Security → 2-Step Verification → enable it
2. Go to App Passwords → create one → copy the 16 characters

---

## 📁 File Structure

```
apartment_hunter/
├── main.py              # Entry point
├── scrapers.py          # Website scrapers (5 sites)
├── ai_filter.py         # Claude AI scoring engine
├── notifier.py          # Email + Telegram notifications
├── backup.py            # 3-level backup system
├── database.py          # SQLite database handler
├── apply.py             # Cover letter sender
├── config.json          # All settings
├── SETUP_AND_RUN.bat    # Windows: install & run locally
├── APPLY_NOW.bat        # Windows: send application to landlord
├── BACKUP_NOW.bat       # Windows: manual backup
└── .github/
    └── workflows/
        └── hunt.yml     # GitHub Actions automation
```

---

## 📬 Notifications

### Telegram Message
```
🏠 New Apartment in Freiburg!

⭐⭐⭐⭐⭐⭐⭐⭐ AI Score: 8/10
📌 Schöne 2-Zimmer Wohnung in Freiburg-Altstadt
💰 650€/Monat
📐 55m²  🚪 2 Zimmer
📍 Freiburg im Breisgau
🤖 Great location near city center, balcony included
🔗 View Listing
```

### Email
A full HTML email with all listing details and a direct link to the listing.

### Daily Summary (8:00 AM)
A daily report with total listings found, top-scored apartments, and statistics by website.

---

## 💌 Applying for an Apartment

When you find a listing you like:
1. Double-click **APPLY_NOW.bat** on your Windows laptop
2. Select the listing from the list
3. The tool sends your German cover letter directly to the landlord

---

## 🔒 Backup System

| Level | Method | Retention |
|-------|--------|-----------|
| 1 | Local backups/ folder | Last 7 days |
| 2 | GitHub Actions cache | Per run |
| 3 | GitHub Artifact | 90 days |

---

## 📄 License

Personal use only. Built for apartment hunting in Freiburg im Breisgau, Germany.
