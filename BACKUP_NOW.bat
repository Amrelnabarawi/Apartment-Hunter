@echo off
chcp 65001 >nul
color 0B
title 🔒 Backup — Apartment Hunter AI

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║       🔒  عمل Backup لقاعدة البيانات             ║
echo  ╚══════════════════════════════════════════════════╝
echo.
python -c "
import json, sys
with open('config.json') as f:
    config = json.load(f)
from backup import run_backup, backup_database, get_stats
backup_database()
stats = get_stats()
print(f'')
print(f'  ✅ Backup تم بنجاح!')
print(f'  📦 إجمالي الإعلانات المحفوظة: {stats.get(\"total\", 0)}')
print(f'  ⭐ إعلانات كويسة: {stats.get(\"good\", 0)}')
print(f'  🆕 آخر 24 ساعة: {stats.get(\"last_24h\", 0)}')
print(f'')
print(f'  📁 الـ Backup محفوظ في مجلد backups/')
"
echo.
pause
