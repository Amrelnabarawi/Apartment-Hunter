🏠 Apartment Hunter AI – Freiburg im Breisgau
=============================================

A smart automation tool that continuously searches for apartments in **Freiburg im Breisgau** and sends instant notifications via **WhatsApp** and **Email** whenever a suitable listing appears.

📛 Badges
---------

https://img.shields.io/badge/Python-3.10+-bluehttps://img.shields.io/badge/Status-Active-successhttps://img.shields.io/badge/License-MIT-greenhttps://img.shields.io/badge/AI-Claude API-orangehttps://img.shields.io/badge/Platform-Windows | Linux | macOS-lightgrey

📸 Screenshots
--------------

> _(Replace these with real screenshots later)_

### Dashboard Example

https://via.placeholder.com/900x400?text=Dashboard+Preview

### WhatsApp Notification Example

https://via.placeholder.com/600x200?text=WhatsApp+Notification

### Email Notification Example

https://via.placeholder.com/600x200?text=Email+Notification

🧩 System Architecture
----------------------

كتابة تعليمات برمجية

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML `┌──────────────────────────┐   │ Apartment Websites        │   │ (ImmoScout, WG-Gesucht…) │   └──────────────┬───────────┘                  │ Scraper   ┌──────────────▼──────────────┐   │ Data Extraction & Cleaning   │   └──────────────┬──────────────┘                  │   ┌──────────────▼──────────────┐   │ AI Scoring (Claude API)      │   │ - Relevance scoring           │   │ - Filtering                   │   └──────────────┬──────────────┘                  │   ┌──────────────▼──────────────┐   │ Duplicate Checker (SQLite)   │   └──────────────┬──────────────┘                  │   ┌──────────────▼──────────────┐   │ Notification Engine          │   │ - WhatsApp (CallMeBot)       │   │ - Email (Gmail App Password) │   └──────────────┬──────────────┘                  │   ┌──────────────▼──────────────┐   │ Logging & Monitoring         │   └──────────────────────────────┘`

✨ Features
----------

*   🔎 Automatically scans multiple apartment websites
    
*   🤖 AI-powered filtering to detect the best listings
    
*   📲 WhatsApp notifications
    
*   📧 Email notifications
    
*   ⏱ Runs automatically every few minutes
    
*   💾 Saves already-seen listings to avoid duplicates
    
*   🧠 AI scoring for relevance
    
*   🛡️ Configurable filters (size, rooms, rent, keywords)
    

🌍 Supported Websites
---------------------

WebsiteLink🏢 ImmoScout24https://immobilienscout24.de🏠 WG-Gesuchthttps://wg-gesucht.de🏘 Immowelthttps://immowelt.de📦 eBay Kleinanzeigenhttps://kleinanzeigen.de🏡 Wohnverdienthttps://wohnverdient.de

🚀 Setup Guide
--------------

### 1️⃣ Install Python

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python --version   `

Requires **Python 3.10+**.

### 2️⃣ Install Dependencies

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

📧 Email Configuration (Gmail)
------------------------------

Enable:

*   2-Step Verification
    
*   App Passwords → Create password for _Mail_ on _Windows Computer_
    

Add to config.json:

json

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   "email": {    "sender_email": "your_email@gmail.com",    "sender_password": "xxxx xxxx xxxx xxxx",    "recipient_email": "your_email@gmail.com"  }   `

📲 WhatsApp Notifications (CallMeBot)
-------------------------------------

1.  Send this message to **+34 644 52 74 68**:
    

كتابة تعليمات برمجية

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   I allow callmebot to send me messages   `

1.  Add your API key to config.json:
    

json

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   "whatsapp": {    "phone": "+4917612345678",    "callmebot_apikey": "123456"  }   `

🤖 Claude AI Setup
------------------

Create an account at:

https://console.anthropic.com

Add your API key:

json

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   "ai": {    "anthropic_api_key": "sk-ant-..."  }   `

⚙️ Search Configuration
-----------------------

Example:

json

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   "search": {    "city": "Freiburg im Breisgau",    "min_size_m2": 40,    "max_size_m2": 60,    "min_rooms": 2,    "max_rooms": 2,    "max_rent_warm": 1400,    "keywords_blacklist": ["tausch", "zwischenmiete"]  }   `

### Parameter Explanation

SettingDescriptionmin\_size\_m2Minimum apartment sizemax\_size\_m2Maximum apartment sizemin\_roomsMinimum number of roomsmax\_roomsMaximum number of roomsmax\_rent\_warmMaximum warm rentkeywords\_blacklistIgnore listings containing these keywords

🧠 AI Filtering
---------------

ScoreMeaning8–10Excellent match6–7Good matchIgnored

Default:

كتابة تعليمات برمجية

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   min_score = 6   `

▶️ Running the Program
----------------------

### Test notifications

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python main.py --test   `

### Run once

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python main.py   `

### Continuous monitoring

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python main.py --loop   `

🤖 Run in Background
--------------------

### Windows

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   start /B python main.py --loop > output.log 2>&1   `

### macOS / Linux

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   nohup python main.py --loop &   `

⏰ Automatic Scheduling
----------------------

### Linux / macOS (Cron)

كتابة تعليمات برمجية

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   */10 * * * * cd /path/to/apartment_hunter && python main.py >> cron.log 2>&1   `

### Windows

Use **Task Scheduler**.

📊 Logs
-------

View logs:

bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   tail -f apartment_hunter.log   `

### Files

FileDescriptionapartment\_hunter.logSystem logsapartments.dbSaved listings database

🎥 Demo (Optional)
------------------

> _(Replace with real GIF or video)_

https://via.placeholder.com/900x400?text=Demo+Video+Placeholder

🧪 Example Output
-----------------

### WhatsApp Message

كتابة تعليمات برمجية

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   🏠 New Apartment Found!  📍 Location: Freiburg im Breisgau  📏 Size: 52 m²  💶 Rent: 1,200€ warm  🔗 Link: https://example.com/listing   `

### Email Example

كتابة تعليمات برمجية

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Subject: New Apartment Match – Freiburg  A new apartment listing matches your criteria:  Location: Freiburg im Breisgau  Size: 48 m²  Rent: 1,150€ warm  Rooms: 2  Link: https://example.com/listing   `

🆘 Common Issues
----------------

ProblemSolutionEmail not sendingUse Gmail App PasswordWhatsApp not workingSend activation message to CallMeBotAPI key errorCheck anthropic\_api\_keyNo listings foundWebsites may temporarily block scraping

📄 License
----------

This project is licensed under the **MIT License**.
