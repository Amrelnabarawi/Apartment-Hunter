🏠 Apartment Hunter AI – Freiburg im Breisgau

A smart tool that automatically searches for apartments in Freiburg and sends you a notification via WhatsApp + Email whenever it finds a suitable listing.

✅ Supported Websites
Website	Link
ImmoScout24	immobilienscout24.de
WG-Gesucht	wg-gesucht.de
Immowelt	immowelt.de
eBay Kleinanzeigen	kleinanzeigen.de
Wohnverdient	wohnverdient.de
🚀 Setup – Step by Step
Step 1 – Install Python

Make sure Python 3.10+ is installed:

python --version
Step 2 – Install Dependencies
pip install -r requirements.txt
Step 3 – Configure Email (Gmail)

Go to your Gmail account

Open:
Manage your Google Account → Security → 2-Step Verification
(This must be enabled)

Then go to:
App Passwords → Create

Select:

App: Mail

Device: Windows Computer

Google will generate a 16-character password

Add it to config.json:

"email": {
    "sender_email": "your_email@gmail.com",
    "sender_password": "xxxx xxxx xxxx xxxx",
    "recipient_email": "your_email@gmail.com"
}
Step 4 – Setup WhatsApp Notifications (CallMeBot – Free)

Open WhatsApp

Send a message to:

+34 644 52 74 68

Message text:

I allow callmebot to send me messages

You will receive an API Key

Add your phone number and API key in config.json:

"whatsapp": {
    "phone": "+4917612345678",
    "callmebot_apikey": "123456"
}
Step 5 – Claude AI API Key

Create an account at:

https://console.anthropic.com

Generate a new API Key

Add it to config.json:

"ai": {
    "anthropic_api_key": "sk-ant-..."
}
⚙️ Search Settings (config.json)

Example configuration:

"search": {
    "city": "Freiburg im Breisgau",
    "min_size_m2": 40,
    "max_size_m2": 60,
    "min_rooms": 2,
    "max_rooms": 2,
    "max_rent_warm": 1400,
    "keywords_blacklist": ["tausch", "zwischenmiete"]
}
Explanation
Setting	Description
min_size_m2	Minimum apartment size
max_size_m2	Maximum apartment size
min_rooms	Minimum number of rooms
max_rooms	Maximum number of rooms
max_rent_warm	Maximum total rent (warm rent)
keywords_blacklist	Listings containing these keywords will be ignored
AI Filtering

min_score defines the minimum AI rating (0–10) required to trigger a notification.

Example:

8–10 → Excellent match

6–7 → Good match

Below 6 → Ignored

Default value:

min_score = 6
▶️ Running the Program
Test notifications
python main.py --test

This verifies that Email and WhatsApp notifications work correctly.

Run once
python main.py
Run continuously (recommended)
python main.py --loop

This checks for new apartments every 10 minutes.

🤖 Run in the Background
Windows
start /B python main.py --loop > output.log 2>&1
Mac / Linux
nohup python main.py --loop &
Automated Scheduling
Linux / Mac (Cron)

Run every 10 minutes:

*/10 * * * * cd /path/to/apartment_hunter && python main.py >> cron.log 2>&1
Windows

Use Task Scheduler to run the script periodically.

📊 View Logs

To monitor logs in real time:

tail -f apartment_hunter.log
💡 Tips

AI Score

8–10 → Excellent match

6–7 → Good match

Below 6 → Rejected

Logs are stored in:

apartment_hunter.log

Seen listings are stored in:

apartments.db

You can change the scanning frequency using:

interval_minutes

inside config.json.

🆘 Common Issues
Problem	Solution
Email not sending	Make sure you're using a Gmail App Password, not your normal password
WhatsApp notifications not working	Send the activation message to CallMeBot first
API key error	Verify anthropic_api_key in config.json
No listings found	Some websites may temporarily block scraping — try again later
