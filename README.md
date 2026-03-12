# 🏠 Apartment Hunter AI – Freiburg im Breisgau

أداة ذكية تبحث عن شقق تلقائياً في **فريبورغ** وتبعتلك إشعار على **واتساب + إيميل** لما تلاقي إعلان مناسب.

---

## ✅ المواقع اللي بتراقبها

| الموقع | الرابط |
|--------|--------|
| ImmoScout24 | immobilienscout24.de |
| WG-Gesucht | wg-gesucht.de |
| Immowelt | immowelt.de |
| eBay Kleinanzeigen | kleinanzeigen.de |
| Wohnverdient | wohnverdient.de |

---

## 🚀 الإعداد خطوة بخطوة

### الخطوة 1 – تثبيت Python
تأكد إن Python 3.10+ مثبت:
```bash
python --version
```

### الخطوة 2 – تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### الخطوة 3 – إعداد الإيميل (Gmail)

1. روح على حسابك في Gmail
2. فتح: **Manage your Google Account → Security → 2-Step Verification** (لازم تكون مفعّلة)
3. بعدها: **App passwords → Create** → اختار "Mail" و"Windows Computer"
4. هيديك كلمة سر مكونة من 16 حرف → حطها في `config.json`

```json
"email": {
    "sender_email": "emailak@gmail.com",
    "sender_password": "xxxx xxxx xxxx xxxx",
    "recipient_email": "emailak@gmail.com"
}
```

### الخطوة 4 – إعداد WhatsApp (CallMeBot – مجاني)

1. افتح واتساب وابعت رسالة للرقم: **+34 644 52 74 68**
   - نص الرسالة: `I allow callmebot to send me messages`
2. هيرد عليك بـ API Key
3. حط رقمك والـ API Key في `config.json`:

```json
"whatsapp": {
    "phone": "+4917612345678",
    "callmebot_apikey": "123456"
}
```

### الخطوة 5 – Claude AI API Key

1. سجّل على: https://console.anthropic.com
2. اعمل API Key جديد
3. حطه في `config.json`:

```json
"ai": {
    "anthropic_api_key": "sk-ant-..."
}
```

---

## ⚙️ إعدادات البحث في config.json

```json
"search": {
    "city": "Freiburg im Breisgau",
    "min_size_m2": 40,
    "max_size_m2": 60,
    "min_rooms": 2,
    "max_rooms": 2,
    "max_rent_warm": 1400,
    "keywords_blacklist": ["tausch", "zwischenmiete"]
}
```

**`min_score`**: الدرجة الأدنى من 10 حتى يبعت إشعار (الافتراضي: 6)

---

## ▶️ التشغيل

```bash
# اختبار الإشعارات بس (تأكد إن كل حاجة شغالة)
python main.py --test

# تشغيل مرة وحدة
python main.py

# تشغيل تلقائي كل 10 دقايق (الأهم!)
python main.py --loop
```

---

## 🤖 تشغيل في الخلفية (على Windows)

```bash
# شغّل في خلفية Windows
start /B python main.py --loop > output.log 2>&1
```

### على Mac/Linux:
```bash
nohup python main.py --loop &
```

### أو استخدم Task Scheduler (Windows) / Cron (Linux/Mac):
```
# Cron كل 10 دقايق:
*/10 * * * * cd /path/to/apartment_hunter && python main.py >> cron.log 2>&1
```

---

## 📊 مشاهدة السجل

```bash
# شوف الـ log مباشرة
tail -f apartment_hunter.log
```

---

## 💡 تلميحات

- **الـ AI Score**: 8–10 = ممتاز، 6–7 = كويس، أقل = رفض
- اللوغ بيتحفظ في `apartment_hunter.log`
- الشقق اللي اتشافت بتتحفظ في `apartments.db`
- غيّر `interval_minutes` في config لو عايز تفحص أكتر أو أقل تكراراً

---

## 🆘 مشاكل شائعة

| المشكلة | الحل |
|---------|------|
| إيميل مش بيتبعت | تأكد من App Password مش كلمة السر العادية |
| واتساب مش شغال | ابعت رسالة التفعيل لـ CallMeBot أولاً |
| API Key خطأ | تأكد من anthropic_api_key في config.json |
| مفيش نتائج | المواقع ممكن تحجب الـ scraper، جرب بعد شوية |
