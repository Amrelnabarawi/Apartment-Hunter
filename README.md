🏠 Apartment Hunter AI – Freiburg im Breisgau
A smart automation tool that continuously searches for apartments in Freiburg im Breisgau and sends instant notifications via WhatsApp and Email whenever a suitable listing appears.

📛 Badges
https://img.shields.io/badge/Python-3.10%2B-blue
https://img.shields.io/badge/Status-Active-success
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/AI-Claude%20API-orange
https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey

📸 Screenshots
(Replace these with real screenshots later)

Dashboard Example
https://via.placeholder.com/900x400?text=Dashboard+Preview

WhatsApp Notification Example
https://via.placeholder.com/600x200?text=WhatsApp+Notification

Email Notification Example
https://via.placeholder.com/600x200?text=Email+Notification

🧩 System Architecture
كتابة تعليمات برمجية
 ┌──────────────────────────┐
 │ Apartment Websites        │
 │ (ImmoScout, WG-Gesucht…) │
 └──────────────┬───────────┘
                │ Scraper
 ┌──────────────▼──────────────┐
 │ Data Extraction & Cleaning   │
 └──────────────┬──────────────┘
                │
 ┌──────────────▼──────────────┐
 │ AI Scoring (Claude API)      │
 │ - Relevance scoring           │
 │ - Filtering                   │
 └──────────────┬──────────────┘
                │
 ┌──────────────▼──────────────┐
 │ Duplicate Checker (SQLite)   │
 └──────────────┬──────────────┘
                │
 ┌──────────────▼──────────────┐
 │ Notification Engine          │
 │ - WhatsApp (CallMeBot)       │
 │ - Email (Gmail App Password) │
 └──────────────┬──────────────┘
                │
 ┌──────────────▼──────────────┐
 │ Logging & Monitoring         │
 └──────────────────────────────┘
✨ Features
🔎 Automatically scans multiple apartment websites

🤖 AI-powered filtering to detect the best listings

📲 WhatsApp notifications

📧 Email notifications

⏱ Runs automatically every few minutes

💾 Saves already-seen listings to avoid duplicates

🧠 AI scoring for relevance

🛡️ Configurable filters (size, rooms, rent, keywords)

🌍 Supported Websites
Website	Link
🏢 ImmoScout24	https://immobilienscout24.de
🏠 WG-Gesucht	https://wg-gesucht.de
🏘 Immowelt	https://immowelt.de
📦 eBay Kleinanzeigen	https://kleinanzeigen.de
🏡 Wohnverdient	https://wohnverdient.de
🚀 Setup Guide
1️⃣ Install Python
bash
python --version
Requires Python 3.10+.

2️⃣ Install Dependencies
bash
pip install -r requirements.txt
📧 Email Configuration (Gmail)
Enable:

2-Step Verification

App Passwords → Create password for Mail on Windows Computer

Add to config.json:

json
"email": {
  "sender_email": "your_email@gmail.com",
  "sender_password": "xxxx xxxx xxxx xxxx",
  "recipient_email": "your_email@gmail.com"
}
📲 WhatsApp Notifications (CallMeBot)
Send this message to +34 644 52 74 68:

كتابة تعليمات برمجية
I allow callmebot to send me messages
Add your API key to config.json:

json
"whatsapp": {
  "phone": "+4917612345678",
  "callmebot_apikey": "123456"
}
🤖 Claude AI Setup
Create an account at:

https://console.anthropic.com

Add your API key:

json
"ai": {
  "anthropic_api_key": "sk-ant-..."
}
⚙️ Search Configuration
Example:

json
"search": {
  "city": "Freiburg im Breisgau",
  "min_size_m2": 40,
  "max_size_m2": 60,
  "min_rooms": 2,
  "max_rooms": 2,
  "max_rent_warm": 1400,
  "keywords_blacklist": ["tausch", "zwischenmiete"]
}
Parameter Explanation
Setting	Description
min_size_m2	Minimum apartment size
max_size_m2	Maximum apartment size
min_rooms	Minimum number of rooms
max_rooms	Maximum number of rooms
max_rent_warm	Maximum warm rent
keywords_blacklist	Ignore listings containing these keywords
🧠 AI Filtering
Score	Meaning
8–10	Excellent match
6–7	Good match
Ignored
Default:

كتابة تعليمات برمجية
min_score = 6
▶️ Running the Program
Test notifications
bash
python main.py --test
Run once
bash
python main.py
Continuous monitoring
bash
python main.py --loop
🤖 Run in Background
Windows
bash
start /B python main.py --loop > output.log 2>&1
macOS / Linux
bash
nohup python main.py --loop &
⏰ Automatic Scheduling
Linux / macOS (Cron)
كتابة تعليمات برمجية
*/10 * * * * cd /path/to/apartment_hunter && python main.py >> cron.log 2>&1
Windows
Use Task Scheduler.

📊 Logs
View logs:

bash
tail -f apartment_hunter.log
Files
File	Description
apartment_hunter.log	System logs
apartments.db	Saved listings database
🎥 Demo (Optional)
(Replace with real GIF or video)

https://via.placeholder.com/900x400?text=Demo+Video+Placeholder

🧪 Example Output
WhatsApp Message
كتابة تعليمات برمجية
🏠 New Apartment Found!
📍 Location: Freiburg im Breisgau
📏 Size: 52 m²
💶 Rent: 1,200€ warm
🔗 Link: https://example.com/listing
Email Example
كتابة تعليمات برمجية
Subject: New Apartment Match – Freiburg

A new apartment listing matches your criteria:

Location: Freiburg im Breisgau
Size: 48 m²
Rent: 1,150€ warm
Rooms: 2

Link: https://example.com/listing
🆘 Common Issues
Problem	Solution
Email not sending	Use Gmail App Password
WhatsApp not working	Send activation message to CallMeBot
API key error	Check anthropic_api_key
No listings found	Websites may temporarily block scraping
📄 License
This project is licensed under the MIT License.
