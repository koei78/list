import os
import sqlite3
from contextlib import contextmanager


DB_PATH = os.getenv("DB_PATH", os.path.join("data", "leads.sqlite3"))


def ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def get_connection():
    ensure_dir(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_cursor():
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()


def init_db():
    with get_cursor() as cur:
        # datasets: グループ（店舗名+住所）単位
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shop_name TEXT NOT NULL,
                address TEXT NOT NULL,
                summary TEXT DEFAULT NULL,
                has_homepage INTEGER NOT NULL DEFAULT 0,
                homepage_url TEXT DEFAULT NULL,
                csv_name TEXT DEFAULT NULL,
                next_call_date TEXT DEFAULT NULL,
                next_call_time TEXT DEFAULT NULL,
                phone TEXT DEFAULT NULL,
                top_name TEXT DEFAULT NULL,
                time TEXT DEFAULT NULL,
                day TEXT DEFAULT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        # calls: 各CSV行（データセットに属する）
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER,
                start_user_type TEXT NOT NULL,
                callee TEXT NOT NULL,
                call_flow TEXT DEFAULT NULL,
                caller_number TEXT NOT NULL,
                content TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
            );
            """
        )
        # 旧カラムを持つ既存テーブルからの移行のため、足りない列を追加（SQLite簡易）
        try:
            cur.execute("ALTER TABLE calls ADD COLUMN dataset_id INTEGER")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE calls ADD COLUMN content TEXT")
        except Exception:
            pass
        # Ensure 'date' column exists on calls to store CSV-provided date values
        try:
            cur.execute("ALTER TABLE calls ADD COLUMN date TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN csv_name TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN summary TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN has_homepage INTEGER NOT NULL DEFAULT 0")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN homepage_url TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN phone TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN next_call_date TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN next_call_time TEXT")
        except Exception:
            pass
        # New fields to align with req.py (representative, business hours, holidays)
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN top_name TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN time TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE datasets ADD COLUMN day TEXT")
        except Exception:
            pass
