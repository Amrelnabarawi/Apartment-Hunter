@echo off
chcp 65001 >nul
color 0B
title 🔄 تسجيل الأداة في Task Scheduler

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   🔄  بيسجّل الأداة تشتغل تلقائياً              ║
echo  ║      حتى لو أعدت تشغيل اللاب توب                ║
echo  ╚══════════════════════════════════════════════════╝
echo.

:: Get current directory (where this bat file lives)
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

echo  📁 مجلد الأداة: %SCRIPT_DIR%
echo.

:: Create a VBS script that runs Python hidden (no black window)
echo Set WshShell = CreateObject("WScript.Shell") > "%SCRIPT_DIR%\run_hidden.vbs"
echo WshShell.Run "cmd /c cd /d """ & "%SCRIPT_DIR%" & """ && python main.py --loop >> apartment_hunter.log 2>&1", 0, False >> "%SCRIPT_DIR%\run_hidden.vbs"

echo  [1/2] بيسجّل المهمة في Task Scheduler...

schtasks /create /tn "ApartmentHunterAI" ^
  /tr "wscript.exe \"%SCRIPT_DIR%\run_hidden.vbs\"" ^
  /sc ONLOGON ^
  /rl HIGHEST ^
  /f >nul 2>&1

if %errorlevel% equ 0 (
    echo  ✅ اتسجّلت بنجاح!
) else (
    echo  ⚠️  محتاج صلاحيات Admin - جرّب كليك يمين على الملف ده واختار "Run as administrator"
    pause
    exit
)

echo  [2/2] بيشغّل الأداة دلوقتي...
start "" wscript.exe "%SCRIPT_DIR%\run_hidden.vbs"

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   🎉  كل حاجة جاهزة!                            ║
echo  ║                                                   ║
echo  ║   ✅  الأداة شغّالة دلوقتي في الخلفية            ║
echo  ║   ✅  هتشتغل تلقائي كل ما تفتح اللاب توب        ║
echo  ║   ✅  مش هتشوف أي نافذة سوداء                   ║
echo  ║   ✅  الإشعارات هتيجيلك على إيميلك وواتساب       ║
echo  ║                                                   ║
echo  ║   📧  صحّي وشوف إيميلك!                          ║
echo  ╚══════════════════════════════════════════════════╝
echo.
pause
