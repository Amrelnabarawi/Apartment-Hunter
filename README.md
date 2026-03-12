🏠 Apartment Hunter AI – Freiburg im Breisgau

A smart tool that automatically searches for apartments in Freiburg and sends you instant notifications via WhatsApp and Email whenever it finds a suitable listing.

✨ Features

🔎 Automatically scans multiple apartment websites

🤖 Uses AI filtering to detect the best listings

📲 Sends notifications via WhatsApp

📧 Sends notifications via Email

⏱ Runs automatically every few minutes

💾 Saves already-seen listings to avoid duplicates

🌍 Supported Websites
Website	Link
🏢 ImmoScout24	https://immobilienscout24.de

🏠 WG-Gesucht	https://wg-gesucht.de

🏘 Immowelt	https://immowelt.de

📦 eBay Kleinanzeigen	https://kleinanzeigen.de

🏡 Wohnverdient	https://wohnverdient.de
🚀 Setup Guide
1️⃣ Install Python

Make sure Python 3.10 or higher is installed.

python --version
2️⃣ Install Dependencies
pip install -r requirements.txt
📧 Email Configuration (Gmail)

Open your Google Account

Navigate to:

Security → 2-Step Verification

Enable it if it's not already enabled.

Then open:

App Passwords → Create

Choose:

App: Mail
Device: Windows Computer

Google will generate a 16-character password.

Add it to config.json:

"email": {
  "sender_email": "your_email@gmail.com",
  "sender_password": "xxxx xxxx xxxx xxxx",
  "recipient_email": "your_email@gmail.com"
}
📲 WhatsApp Notifications (CallMeBot)

Open WhatsApp

Send this message to:

+34 644 52 74 68

Message:

I allow callmebot to send me messages

You will receive an API Key

Add it to config.json:

"whatsapp": {
  "phone": "+4917612345678",
  "callmebot_apikey": "123456"
}
🤖 Claude AI Setup

Create an account:

https://console.anthropic.com

Generate an API Key

Add it to config.json:

"ai": {
  "anthropic_api_key": "sk-ant-..."
}
⚙️ Search Configuration

Example settings in config.json

"search": {
  "city": "Freiburg im Breisgau",
  "min_size_m2": 40,
  "max_size_m2": 60,
  "min_rooms": 2,
  "max_rooms": 2,
  "max_rent_warm": 1400,
  "keywords_blacklist": ["tausch", "zwischenmiete"]
}
Setting Explanation
Setting	Description
min_size_m2	Minimum apartment size
max_size_m2	Maximum apartment size
min_rooms	Minimum number of rooms
max_rooms	Maximum number of rooms
max_rent_warm	Maximum warm rent
keywords_blacklist	Ignore listings containing these keywords
🧠 AI Filtering

The system uses AI to rate each apartment listing.

Score	Meaning
8 – 10	Excellent match
6 – 7	Good match
Below 6	Ignored

Default configuration:

min_score = 6
▶️ Running the Program
Test notifications
python main.py --test

This checks if Email and WhatsApp notifications work correctly.

Run once
python main.py
Continuous monitoring (recommended)
python main.py --loop

The script will check for new apartments every 10 minutes.

🤖 Run in Background
Windows
start /B python main.py --loop > output.log 2>&1
Mac / Linux
nohup python main.py --loop &
⏰ Automatic Scheduling
Linux / Mac (Cron)

Run every 10 minutes:

*/10 * * * * cd /path/to/apartment_hunter && python main.py >> cron.log 2>&1
Windows

Use Task Scheduler to run the script periodically.

📊 Logs

Monitor logs in real time:

tail -f apartment_hunter.log

Saved files:

File	Description
apartment_hunter.log	System logs
apartments.db	Saved listings database
💡 Tips

Adjust scanning frequency using:

interval_minutes

inside config.json.

The script avoids sending duplicate listings.

🆘 Common Issues
Problem	Solution
Email not sending	Use a Gmail App Password, not your normal password
WhatsApp notifications not working	Send the activation message to CallMeBot first
API key error	Verify anthropic_api_key in config.json
No listings found	Websites may temporarily block scraping
