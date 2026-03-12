#!/usr/bin/env python3
"""
📨 APPLY.py — بعت طلب السكن لصاحب الشقة
==========================================
شغّله لما تلاقي شقة عجبتك وعايز تبعت الطلب فوراً.

Usage:
    python apply.py                     ← بيعرضلك آخر الشقق الكويسة
    python apply.py --email owner@...   ← بيبعت إيميل لصاحب الشقة
    python apply.py --whatsapp          ← بيطبعلك الرسالة تنسخها على واتساب
"""

import json
import sqlite3
import argparse
import sys
from notifier import send_application, get_whatsapp_application_text

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_recent_good_listings(limit=10):
    conn = sqlite3.connect("apartments.db")
    c = conn.cursor()
    c.execute("""
        SELECT id, title, price, size, rooms, address, url, source, ai_score, ai_summary
        FROM listings
        WHERE ai_score >= 6
        ORDER BY found_at DESC
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def display_listings(listings):
    print("\n" + "="*60)
    print("  📋 آخر الشقق الكويسة اللي لقتها الأداة:")
    print("="*60)
    for i, row in enumerate(listings, 1):
        id_, title, price, size, rooms, address, url, source, score, summary = row
        stars = "⭐" * min(score, 10)
        print(f"\n  [{i}] {title}")
        print(f"      💰 {price:.0f}€  📐 {size:.0f}m²  🚪 {rooms} Zimmer")
        print(f"      📍 {address}")
        print(f"      🌐 {source}  |  تقييم AI: {score}/10 {stars}")
        print(f"      🤖 {summary}")
        print(f"      🔗 {url}")
    print("\n" + "="*60)

def listing_to_dict(row):
    id_, title, price, size, rooms, address, url, source, score, summary = row
    return {
        "id": id_, "title": title, "price": price, "size": size,
        "rooms": rooms, "address": address, "url": url,
        "source": source, "ai_score": score, "ai_summary": summary,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="إيميل صاحب الشقة", default=None)
    parser.add_argument("--whatsapp", action="store_true", help="اطبع الرسالة للواتساب")
    parser.add_argument("--listing", type=int, help="رقم الشقة من القائمة", default=None)
    args = parser.parse_args()

    config = load_config()
    listings = get_recent_good_listings()

    if not listings:
        print("\n  ❌ مفيش شقق متسجلة لسه. شغّل main.py الأول!")
        sys.exit(1)

    display_listings(listings)

    # Pick listing
    if args.listing:
        idx = args.listing - 1
    else:
        print("\n  اختار رقم الشقة اللي عايز تتقدملها:")
        idx = int(input("  > ")) - 1

    if idx < 0 or idx >= len(listings):
        print("  ❌ رقم غلط!")
        sys.exit(1)

    listing = listing_to_dict(listings[idx])
    print(f"\n  ✅ اخترت: {listing['title']}")

    if args.email:
        # Send directly
        print(f"\n  📨 بيبعت الإيميل لـ {args.email} ...")
        ok = send_application(args.email, listing, config)
        if ok:
            print("  ✅ اتبعت بنجاح!")
        else:
            print("  ❌ في مشكلة — شوف apartment_hunter.log")

    elif args.whatsapp:
        text = get_whatsapp_application_text(listing, config)
        print("\n" + "="*60)
        print("  📱 انسخ الكلام ده وابعته على واتساب:")
        print("="*60 + "\n")
        print(text)
        print("\n" + "="*60)

    else:
        print("\n  عايز تبعت الطلب إزاي؟")
        print("  [1] إيميل")
        print("  [2] واتساب (نسخ ولصق)")
        choice = input("  > ").strip()

        if choice == "1":
            email = input("  اكتب إيميل صاحب الشقة: ").strip()
            ok = send_application(email, listing, config)
            if ok:
                print("  ✅ الإيميل اتبعت!")
            else:
                print("  ❌ في مشكلة — شوف apartment_hunter.log")

        elif choice == "2":
            text = get_whatsapp_application_text(listing, config)
            print("\n" + "="*60)
            print("  📱 انسخ الكلام ده وابعته على واتساب لصاحب الشقة:")
            print("="*60 + "\n")
            print(text)
        else:
            print("  اختيار غير صحيح.")

if __name__ == "__main__":
    main()
