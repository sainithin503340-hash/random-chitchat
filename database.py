import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reports INTEGER DEFAULT 0,
    premium INTEGER DEFAULT 0
)
""")

conn.commit()


def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()


def total_users():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]


def add_report(user_id):
    cursor.execute(
        "UPDATE users SET reports = reports + 1 WHERE telegram_id=?",
        (user_id,)
    )
    conn.commit()


def get_reports(user_id):
    cursor.execute(
        "SELECT reports FROM users WHERE telegram_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return 0
def get_total_users():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]