import os
import json
from flask import Flask, render_template, jsonify, request, send_from_directory
from inspection_report import generate_random_report, build_report
from datetime import datetime
import cv2
import numpy as np

app = Flask(__name__)

# where we'll store the last-submitted report
REPORT_PATH = os.path.join(app.root_path, "custom_report.json")
# IMG_UPLOAD_FOLDER = os.path.join(app.root_path, "data/img")
IMG_UPLOAD_FOLDER = os.path.join(app.root_path, "data", "img")
os.makedirs(IMG_UPLOAD_FOLDER, exist_ok=True)

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
        # report = generate_random_report()
        return jsonify({"error": "No report available"}), 404
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
    try:
        os.remove(IMG_UPLOAD_FOLDER)
        print("% s removed successfully" % IMG_UPLOAD_FOLDER)
    except OSError as error:
        print(error)
        print("File path can not be removed")
    if not os.path.exists(REPORT_PATH):
        return jsonify({"error": "No report to delete"}), 404

    delete_report_file()
    return jsonify({"message": "Report deleted successfully"})

@app.route("/api/report/image", methods=["POST"])
def upload_image():
    global latest_image
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image provided"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "Empty filename"}), 400

        # filename = secure_filename(f"{int(time.time())}_{file.filename}")
        filename = file.filename
        filepath = os.path.join(IMG_UPLOAD_FOLDER, filename)
        # Read image file as bytes and convert to numpy array
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({"success": False, "error": "Invalid image file"}), 400

        # Save image using OpenCV
        cv2.imwrite(filepath, img)

        return jsonify({"success": True, "filename": filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/uploads/<path:filename>")
def serve_uploaded_image(filename):
    """
    Serve the file “data/img/<filename>” whenever someone hits /uploads/<filename>.
    """
    return send_from_directory(IMG_UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)