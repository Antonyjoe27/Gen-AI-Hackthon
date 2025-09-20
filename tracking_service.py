# services/tracking_service.py
import sqlite3, time, os

DB = "data/db.sqlite3"
def _conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS cases(
        id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, techniques TEXT, region TEXT, lang TEXT, ts REAL
    )""")
    return conn

def log_case(content, detected_techniques, region=None, lang="en"):
    conn = _conn()
    conn.execute("INSERT INTO cases(content, techniques, region, lang, ts) VALUES (?,?,?,?,?)",
                 (content[:1000], ",".join(detected_techniques or []), region, lang, time.time()))
    conn.commit()

def get_hotspots(limit=50):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT region, COUNT(*) as cases FROM cases WHERE region IS NOT NULL GROUP BY region ORDER BY cases DESC LIMIT ?", (limit,))
    res = [{"region": row[0], "cases": row[1]} for row in cur.fetchall()]
    return res
