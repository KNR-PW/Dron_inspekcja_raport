import rclpy
from rclpy.node import Node
import sqlite3
import requests
from inspection_report import build_report

DB_DEFAULT_PATH = 'inspection.db'

class ReportUpdaterNode(Node):
    def __init__(self):
        super().__init__('report_updater')
        # ROS parameters
        self.declare_parameter('db_path', DB_DEFAULT_PATH)
        self.declare_parameter('base_url', 'http://localhost:5000')
        self.declare_parameter('update_period', 10.0)
        self.declare_parameter('team', '')
        self.declare_parameter('email', '')
        self.declare_parameter('pilot', '')
        self.declare_parameter('phone', '')

        self.db_path = self.get_parameter('db_path').value
        self.base_url = self.get_parameter('base_url').value.rstrip('/')
        self.update_period = self.get_parameter('update_period').value
        self.team = self.get_parameter('team').value
        self.email = self.get_parameter('email').value
        self.pilot = self.get_parameter('pilot').value
        self.phone = self.get_parameter('phone').value

        # Initialize database
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute('PRAGMA foreign_keys=ON;')
        self.conn.row_factory = sqlite3.Row
        self._init_db_schema()

        # HTTP session
        self.session = requests.Session()

        # Create report record on server and local DB
        self.report_id = self._create_report_on_server()
        self._save_local_report_metadata()

        # Periodic update timer
        self.create_timer(self.update_period, self._timer_callback)

    def _init_db_schema(self):
        c = self.conn.cursor()
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
        """
        )
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
        """
        )
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
        """
        )
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
        """
        )
        self.conn.commit()

    def _create_report_on_server(self):
        # Initial empty report payload
        payload = build_report([], [], [], metadata={
            'team': self.team,
            'email': self.email,
            'pilot': self.pilot,
            'phone': self.phone
        })
        try:
            resp = self.session.post(f"{self.base_url}/api/report", json=payload, timeout=5.0)
            resp.raise_for_status()
            report = resp.json()
            rid = report.get('id')
            self.get_logger().info(f"Created report on server with id {rid}")
            # Insert into local reports table
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO reports (id, team, email, pilot, phone) VALUES (?, ?, ?, ?, ?)",
                (rid, self.team, self.email, self.pilot, self.phone)
            )
            self.conn.commit()
            return rid
        except Exception as e:
            self.get_logger().error(f"Failed to create remote report: {e}")
            return None

    def _save_local_report_metadata(self):
        # Ensure we have a local entry for the report
        if self.report_id is None:
            return
        # Already inserted during creation; can update other fields later if needed
        pass

    def _load_db_records(self):
        c = self.conn.cursor()
        # Load infrastructure changes
        c.execute("SELECT * FROM infrastructure_changes WHERE report_id = ? ORDER BY detection_time", (self.report_id,))
        infra = [dict(r) for r in c.fetchall()]
        # Load incidents
        c.execute("SELECT * FROM incidents WHERE report_id = ? ORDER BY time", (self.report_id,))
        incidents = [dict(r) for r in c.fetchall()]
        # Load arucos
        c.execute("SELECT * FROM arucos WHERE report_id = ? ORDER BY id", (self.report_id,))
        arucos = [dict(r) for r in c.fetchall()]
        return infra, incidents, arucos

    def _timer_callback(self):
        if self.report_id is None:
            self.get_logger().warning("No report ID; skipping update")
            return
        infra, incidents, arucos = self._load_db_records()
        # Build and send update
        payload = build_report(infra, incidents, arucos)
        try:
            resp = self.session.put(
                f"{self.base_url}/api/report/{self.report_id}",
                json=payload,
                timeout=5.0
            )
            resp.raise_for_status()
            self.get_logger().info(f"Updated report {self.report_id} successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to update report: {e}")

    def destroy_node(self):
        try:
            self.conn.close()
        except:
            pass
        self.session.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ReportUpdaterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
