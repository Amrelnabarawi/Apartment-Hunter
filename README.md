# 🏠 Apartment Hunter AI — Freiburg im Breisgau

An automated apartment hunting tool that monitors 7 German rental websites every hour, filters listings by location and criteria, and sends instant notifications via Email and Telegram — completely free, no AI API needed, runs in the cloud 24/7 even when your laptop is off.

---

## ✨ Features

- 🔍 **Monitors 7 websites** every hour automatically
- 📍 **Strict location filter** — only Freiburg im Breisgau area (20km radius)
- 🧠 **Smart rule-based scoring** — rates each listing 1–10 for free (no API cost)
- 📧 **Email + Telegram** notifications for good listings (score 6+)
- 🔄 **No duplicate alerts** — only notifies when a truly NEW listing appears
- 📊 **Daily summary email** every morning at 8:00 AM
- ☁️ **Runs in the cloud** via GitHub Actions — laptop can be completely off
- 💌 **One-click application** — sends German cover letter to landlords
- 💰 **100% free** — no credit card, no API costs

---

## 🌐 Websites Monitored

| Website | Status |
|---------|--------|
| WG-Gesucht | ✅ Working |
| eBay Kleinanzeigen | ✅ Working |
| Immonet | ✅ Working |
| Kalaydo | ✅ Working |
| ImmoScout24 | ⚠️ Sometimes blocked |
| Immowelt | ⚠️ Sometimes blocked |
| Wohnverdient | ⚠️ Sometimes blocked |

---

## 🔎 Search Criteria

| Parameter | Value |
|-----------|-------|
| Location | Freiburg im Breisgau + 20km radius |
| Size | 40 – 70 m² |
| Rooms | 2 Zimmer |
| Cold rent | 500 – 700€ |
| Max warm rent | 1,000€ |
| Blacklist | WG, Tausch, Zwischenmiete, WG-Zimmer |

---

## 🧠 How the Smart Filter Works

No AI API needed — the filter scores each listing based on rules:

| Criteria | Points |
|----------|--------|
| Price ≤ 700€ | +2 |
| Price ≤ 850€ | +1 |
| Price > 1000€ | -2 |
| Size 40–70m² | +1 |
| Size > 70m² (spacious) | +2 |
| Has balcony | +1 |
| Has elevator | +1 |
| City center (Altstadt/Innenstadt) | +1 |
| 3+ positive features (EBK, renoviert...) | +1 |
| Negative features (Souterrain, befristet...) | -1 |

**Score 6+ → Email + Telegram notification sent immediately ✅**

---

## ⚙️ How It Works

```
Every hour → GitHub Actions runs the tool for free
                    ↓
        Scrapes 7 websites for new listings
                    ↓
        Rejects listings outside Freiburg area
                    ↓
        Checks if listing was seen before
                    ↓
        New listing? → Scores it (1-10)
                    ↓
        Score 6+ ? → Email + Telegram sent ✅
        Score < 6 ? → Skipped ❌
                    ↓
        Database saved for next run
```

---

## 🚀 Setup

### Requirements
- GitHub account (free) — github.com
- Gmail account + App Password (free)
- Telegram bot token + chat ID (free)

### GitHub Secrets Required

| Secret | Description | How to get |
|--------|-------------|------------|
| `EMAIL_SENDER` | Your Gmail address | Your Gmail |
| `EMAIL_PASSWORD` | Gmail App Password (16 chars) | Gmail → Security → App Passwords |
| `EMAIL_RECIPIENT` | Email to receive alerts | Any email you check |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | @BotFather on Telegram → /newbot |
| `TELEGRAM_CHAT_ID` | Your Telegram user ID | @userinfobot on Telegram |
| `ANTHROPIC_API_KEY` | Optional — not used for filtering | Not needed anymore |

### Getting Gmail App Password
1. Go to **myaccount.google.com → Security → 2-Step Verification** → enable it
2. Go to **App Passwords** → create one → copy the 16 characters
3. Use this as `EMAIL_PASSWORD` (NOT your normal Gmail password)

### Getting Telegram Credentials
1. Open Telegram → search **@BotFather** → send `/newbot`
2. Follow the steps → copy the **Bot Token**
3. Search **@userinfobot** → send any message → copy your **ID number**
4. Open your new bot and press **Start** (important!)

---

## 📁 File Structure

```
apartment_hunter/
├── main.py              # Entry point — runs once or in loop
├── scrapers.py          # Website scrapers (7 sites)
├── ai_filter.py         # Smart rule-based filter (free, no API)
├── notifier.py          # Email (Gmail) + Telegram notifications
├── backup.py            # Daily backup system
├── database.py          # SQLite — tracks seen listings
├── apply.py             # Cover letter sender
├── config.json          # All search settings
├── SETUP_AND_RUN.bat    # Windows: install & run locally
├── APPLY_NOW.bat        # Windows: send application to landlord
├── BACKUP_NOW.bat       # Windows: manual backup
└── .github/
    └── workflows/
        └── hunt.yml     # GitHub Actions — runs every hour
```

---

## ⚙️ GitHub Actions Workflow (hunt.yml)

```yaml
name: Apartment Hunter AI

on:
  schedule:
    - cron: '0 * * * *'   # Every hour
  workflow_dispatch:        # Manual trigger

jobs:
  hunt:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python 3.11
      - Install libraries (requests, beautifulsoup4, lxml)
      - Restore database from cache
      - Run the tool
      - Save database to cache
      - Upload DB as 90-day backup artifact
```

---

## 📬 Notifications

### Telegram Message
```
🏠 New Apartment in Freiburg!

⭐⭐⭐⭐⭐⭐⭐ AI Score: 7/10
📌 Schöne 2-Zimmer Wohnung mit Balkon
💰 620€/Monat
📐 52m²  🚪 2 Zimmer
📍 Freiburg im Breisgau, Wiehre
🤖 620€ • 52m² • Balcony ✅ • Great price
🔗 View Listing
```

### Email
Full HTML email with all listing details and a direct link.

### Daily Summary (8:00 AM)
Daily report with all listings found, top scores, and stats by website.

---

## 💌 Applying for an Apartment

When you like a listing:
1. Double-click **APPLY_NOW.bat** on your Windows laptop
2. Select the listing from the list
3. The tool sends your German cover letter directly to the landlord

---

## 🔒 Backup System

| Level | Method | Retention |
|-------|--------|-----------|
| 1 | GitHub Actions cache | Between runs |
| 2 | GitHub Artifact | 90 days |
| 3 | Local backups/ folder | Last 7 days (when run locally) |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| No notifications | Check GitHub Actions logs → Run the tool section |
| Wrong city listings | Location filter is strict — only Freiburg 20km |
| Duplicate notifications | Database cache is working — should not happen |
| Email not arriving | Check Gmail Spam folder |
| Workflow failing | Check GitHub Secrets are all set correctly |

---

## 📄 License

Personal use only. Built for apartment hunting in Freiburg im Breisgau, Germany.
