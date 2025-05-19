from flask import Flask, render_template, send_from_directory, jsonify
from inspection_report import generate_random_report

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("inspection-report.html")

@app.route("/api/report")
def api_report():
    report = generate_random_report()
    return jsonify(report)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)