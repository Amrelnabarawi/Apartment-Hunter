@echo off
chcp 65001 >nul
color 0A
title 🏠 Apartment Hunter AI - Setup

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║       🏠  Apartment Hunter AI - Freiburg         ║
echo  ║         Setup تلقائي - مش محتاج خبرة            ║
echo  ╚══════════════════════════════════════════════════╝
echo.

:: ─── Step 1: Check Python ───────────────────────────────
echo  [1/4] بيتحقق من Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ❌ Python مش مثبت!
    echo.
    echo  هيفتحلك صفحة التحميل دلوقتي...
    echo  المهم: ضع علامة صح على "Add Python to PATH" قبل التثبيت!
    echo.
    pause
    start https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    echo.
    echo  بعد ما تخلص التثبيت، اضغط Enter هنا...
    pause
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo  ❌ Python لسه مش شغال. تأكد إنك ضغطت "Add Python to PATH"
        pause
        exit
    )
)
echo  ✅ Python شغال!
echo.

:: ─── Step 2: Install libraries ──────────────────────────
echo  [2/4] بيحمّل المكتبات المطلوبة (ممكن ياخد دقيقة)...
pip install requests beautifulsoup4 anthropic lxml --quiet --no-warn-script-location
if %errorlevel% neq 0 (
    echo  ❌ في مشكلة في التحميل. تأكد من الإنترنت وجرب تاني.
    pause
    exit
)
echo  ✅ المكتبات اتحملت!
echo.

:: ─── Step 3: Open config.json ───────────────────────────
echo  [3/4] هيفتحلك ملف الإعدادات...
echo.
echo  ═══════════════════════════════════════════════════
echo   📝 هتحتاج تملا في ملف الإعدادات:
echo      - إيميلك + App Password بتاع Gmail
echo      - رقم الواتساب + API Key بتاع CallMeBot
echo      - API Key بتاع Claude AI
echo  ═══════════════════════════════════════════════════
echo.
echo  اضغط Enter وملف الإعدادات هيفتح في Notepad...
pause >nul
notepad config.json
echo.

:: ─── Step 4: Test notifications ─────────────────────────
echo  [4/4] تست الإشعارات...
echo.
echo  دوسة Enter وهيبعت إشعار تجريبي للإيميل والواتساب...
pause >nul
python main.py --test
echo.

echo  ═══════════════════════════════════════════════════
echo   ✅ كل حاجة جاهزة!
echo.
echo   ايه اللي تعمله دلوقتي؟
echo   اضغط أي زر وهيشتغل تلقائياً كل 10 دقايق 🚀
echo  ═══════════════════════════════════════════════════
echo.
pause >nul

python main.py --loop
pause

