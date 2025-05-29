import sqlite3

DB_PATH = "inspection.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_report(report):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO reports (team, email, pilot, phone, mission_time, mission_no, duration, battery_before, battery_after, kp_index, infra_map)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report['team'], report['email'], report['pilot'], report['phone'],
        report['mission_time'], report['mission_no'], report['duration'],
        report['battery_before'], report['battery_after'], report['kp_index'],
        report.get('infra_map', '/static/img/mapa.jpg')
    ))
    report_id = cur.lastrowid

    for ch in report.get('infrastructure_changes', []):
        cur.execute("""
            INSERT INTO infrastructure_changes (report_id, category, detection_time, location, image, jury)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (report_id, ch['category'], ch['detection_time'], ch['location'], ch['image'], ch['jury']))

    for inc in report.get('incidents', []):
        cur.execute("""
            INSERT INTO incidents (report_id, event, time, location, image, notified, jury)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (report_id, inc['event'], inc['time'], inc['location'], inc['image'], inc['notified'], inc['jury']))

    for ar in report.get('arucos', []):
        cur.execute("""
            INSERT INTO arucos (report_id, content, location, location_changed, content_changed, image, jury)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (report_id, ar['content'], ar['location'], ar['location_changed'], ar['content_changed'], ar['image'], ar['jury']))

    db.commit()
    db.close()
    return report_id

def get_latest_report():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM reports ORDER BY id DESC LIMIT 1")
    report = cur.fetchone()
    if not report:
        db.close()
        return None
    report = dict(report)
    report_id = report['id']

    cur.execute("SELECT * FROM infrastructure_changes WHERE report_id=?", (report_id,))
    report['infrastructure_changes'] = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM incidents WHERE report_id=?", (report_id,))
    report['incidents'] = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT * FROM arucos WHERE report_id=?", (report_id,))
    report['arucos'] = [dict(row) for row in cur.fetchall()]

    db.close()
    return report

def update_latest_report(data):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM reports ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if not row:
        db.close()
        return False
    report_id = row['id']
    for key, value in data.items():
        if key in ['team', 'email', 'pilot', 'phone', 'mission_time', 'mission_no', 'duration', 'battery_before', 'battery_after', 'kp_index', 'infra_map']:
            cur.execute(f"UPDATE reports SET {key}=? WHERE id=?", (value, report_id))
    db.commit()
    db.close()
    return True

def delete_latest_report():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM reports ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if not row:
        db.close()
        return False
    report_id = row['id']
    cur.execute("DELETE FROM reports WHERE id=?", (report_id,))
    db.commit()
    db.close()
    return True
