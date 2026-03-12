@echo off
chcp 65001 >nul
color 0C
title ⏹ إيقاف الأداة

echo.
echo  بيوقّف الأداة...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im wscript.exe >nul 2>&1
echo  ✅ الأداة اتوقفت.
echo.
echo  عشان توقفها بشكل دايم من Task Scheduler:
echo  schtasks /delete /tn "ApartmentHunterAI" /f
echo.
pause
