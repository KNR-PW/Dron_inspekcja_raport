import os
import json
from flask import Flask, render_template, jsonify, request
from inspection_report import generate_random_report, build_report
from datetime import datetime

app = Flask(__name__)

# where we'll store the last-submitted report
REPORT_PATH = os.path.join(app.root_path, "custom_report.json")

def load_report():
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_report(report):
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

def delete_report_file():
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

@app.route("/")
def index():
    return render_template("inspection-report.html")

@app.route("/api/report", methods=["GET"])
def get_report():
    report = load_report()
    if not report:
        # Jeśli nie ma zapisanej wersji, generuj losowy raport
        report = generate_random_report()
    return jsonify(report)

@app.route("/api/report/create", methods=["POST"])
def create_report():
    data = request.get_json(force=True)

    try:
        mission_time = datetime.strptime(data.get("mission_time"), "%d/%m/%Y, %H:%M:%S") if data.get("mission_time") else datetime.now()
    except ValueError:
        return jsonify({"error": "Invalid datetime format, expected 'dd/mm/YYYY, HH:MM:SS'"}), 400

    report = build_report(
        team=data.get("team", ""),
        email=data.get("email", ""),
        pilot=data.get("pilot", ""),
        phone=data.get("phone", ""),
        mission_time=mission_time,
        mission_no=data.get("mission_no", ""),
        duration=data.get("duration", ""),
        battery_before=data.get("battery_before", ""),
        battery_after=data.get("battery_after", ""),
        kp_index=data.get("kp_index", 0),
        employees=data.get("employees", []),
        infrastructure_changes=data.get("infrastructure_changes", []),
        incidents=data.get("incidents", []),
        arucos=data.get("arucos", []),
        infra_map=data.get("infra_map", "/static/img/mapa.jpg")
    )

    save_report(report)
    return jsonify({"message": "Report created successfully", "report": report})

@app.route("/api/report/update", methods=["POST"])
def update_report():
    report = load_report()
    if not report:
        return jsonify({"error": "No existing report to update. Use /api/report/create first."}), 400

    data = request.get_json(force=True)

    if "mission_time" in data:
        try:
            data["mission_time"] = datetime.strptime(data["mission_time"], "%d/%m/%Y, %H:%M:%S").strftime("%d/%m/%Y, %H:%M:%S")
        except ValueError:
            return jsonify({"error": "Invalid datetime format, expected 'dd/mm/YYYY, HH:MM:SS'"}), 400

    for key, value in data.items():
        if key in report and value is not None:
            report[key] = value

    save_report(report)
    return jsonify({"message": "Report updated successfully", "report": report})

@app.route("/api/report/delete", methods=["DELETE"])
def delete_report():
    if not os.path.exists(REPORT_PATH):
        return jsonify({"error": "No report to delete"}), 404

    delete_report_file()
    return jsonify({"message": "Report deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)