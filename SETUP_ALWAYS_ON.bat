@echo off
chcp 65001 >nul
color 0A
title ⚡ إعداد اللاب توب عشان ميناموش

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   ⚡  بيضبط اللاب توب عشان يفضل شغّال           ║
echo  ║      حتى لو أقفلته أو طفيت الشاشة               ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  [1/3] بيمنع النوم لما تقفل الغطا...
powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0

echo  [2/3] بيمنع الشاشة من الإطفاء التلقائي بالكهرباء...
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 60

echo  [3/3] بيطبّق الإعدادات...
powercfg /setactive SCHEME_CURRENT

echo.
echo  ✅ تم! دلوقتي لو أقفلت الغطا اللاب توب هيفضل شغّال.
echo  ✅ الشاشة هتتطفى بس الأداة هتكمّل شغلها.
echo.
echo  ⚠️  تأكد إن الشاحن متوصل عشان البطارية ميخلصش!
echo.
pause
