import os
import json
from flask import Flask, render_template, jsonify, request, abort
from inspection_report import generate_random_report

app = Flask(__name__)

# where we'll store the last-submitted report
REPORT_FILE = os.path.join(app.root_path, "custom_report.json")

@app.route("/")
def index():
    return render_template("inspection-report.html")

@app.route("/api/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, "JSON payload must be an object")
        # save it
        with open(REPORT_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "ok"}), 201

    # GET: try to load custom, else random
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE) as f:
            payload = json.load(f)
    else:
        # payload = generate_random_report()
        payload = {}
    return jsonify(payload)

@app.route("/api/report", methods=["DELETE"])
def clear_report():
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
        return jsonify({"status": "deleted"}), 200
    return jsonify({"status": "no report to delete"}), 200

if __name__ == "__main__":
    app.run(debug=True)
