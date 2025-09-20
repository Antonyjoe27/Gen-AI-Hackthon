# services/gamify_service.py
import sqlite3, os, time

DB = "data/db.sqlite3"
def _conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY, points INTEGER, updated REAL
    )""")
    return conn

def reward_user(user_id: str, points: int, reason: str = None):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT points FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    if row:
        new = row[0] + points
        cur.execute("UPDATE users SET points=?, updated=? WHERE id=?", (new, time.time(), user_id))
    else:
        new = points
        cur.execute("INSERT INTO users(id, points, updated) VALUES (?,?,?)", (user_id, points, time.time()))
    conn.commit()
    return {"user": user_id, "points": new}

def get_leaderboard(limit=5):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id as user_id, points FROM users ORDER BY points DESC LIMIT ?", (limit,))
    return [{"user_id": r[0], "points": r[1]} for r in cur.fetchall()]
