import sqlite3
from datetime import datetime

DB_NAME = "devices.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            mac TEXT PRIMARY KEY,
            ip TEXT,
            vendor TEXT,
            os TEXT,
            first_seen TEXT,
            last_seen TEXT,
            trusted INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def upsert_device(device):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT mac FROM devices WHERE mac = ?", (device["mac"],))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
            UPDATE devices
            SET ip=?, vendor=?, os=?, last_seen=?
            WHERE mac=?
        """, (
            device["ip"],
            device["vendor"],
            device["os"],
            now,
            device["mac"]
        ))
        is_new = False
    else:
        cursor.execute("""
            INSERT INTO devices
            (mac, ip, vendor, os, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            device["mac"],
            device["ip"],
            device["vendor"],
            device["os"],
            now,
            now
        ))
        is_new = True

    conn.commit()
    conn.close()
    return is_new
