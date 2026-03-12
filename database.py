import sqlite3
import hashlib
from datetime import datetime

DB_FILE = "apartments.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            size REAL,
            rooms REAL,
            address TEXT,
            url TEXT,
            source TEXT,
            ai_score INTEGER,
            ai_summary TEXT,
            found_at TEXT,
            notified INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def listing_exists(listing_id: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM listings WHERE id = ?", (listing_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def save_listing(listing: dict):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO listings 
        (id, title, price, size, rooms, address, url, source, ai_score, ai_summary, found_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        listing['id'],
        listing.get('title', ''),
        listing.get('price', 0),
        listing.get('size', 0),
        listing.get('rooms', 0),
        listing.get('address', ''),
        listing.get('url', ''),
        listing.get('source', ''),
        listing.get('ai_score', 0),
        listing.get('ai_summary', ''),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def make_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def get_all_listings(limit=50):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM listings ORDER BY found_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
