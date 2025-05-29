import sqlite3

DB_PATH = "inspection.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT,
        email TEXT,
        pilot TEXT,
        phone TEXT,
        mission_time TEXT,
        mission_no TEXT,
        duration TEXT,
        battery_before TEXT,
        battery_after TEXT,
        kp_index INTEGER,
        infra_map TEXT
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS infrastructure_changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        category TEXT,
        detection_time TEXT,
        location TEXT,
        image TEXT,
        jury TEXT,
        FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        event TEXT,
        time TEXT,
        location TEXT,
        image TEXT,
        notified TEXT,
        jury TEXT,
        FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS arucos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        content TEXT,
        location TEXT,
        location_changed TEXT,
        content_changed TEXT,
        image TEXT,
        jury TEXT,
        FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
