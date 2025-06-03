# drone_uploader.py
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000"


def report_exists():
    resp = requests.get(f"{BASE_URL}/api/report")
    return resp.status_code == 200


def create_report():
    print("Tworzę nowy raport...")
    payload = {
        "team": "Dronix",
        "email": "kontakt@dronix.pl",
        "pilot": "Jan Kowalski",
        "phone": "+48123456789",
        "mission_time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "mission_no": "01",
        "duration": "10:00",
        "battery_before": "95% / 16.7 V",
        "battery_after": "40% / 15.3 V",
        "kp_index": 4,
        "employees": [],
        "infrastructure_changes": [],
        "incidents": [],
        "arucos": [],
        "infra_map": "/static/img/mapa.jpg"
    }
    resp = requests.post(f"{BASE_URL}/api/report/create", json=payload)
    print(f"Raport utworzony: {resp.status_code}")


def upload_image_and_add_to_report(image_path, entry_type, entry_data):
    with open(image_path, 'rb') as f:
        files = {'image': f}
        upload_resp = requests.post(f"{BASE_URL}/api/report/image", files=files)

    if upload_resp.status_code != 200:
        print("Upload failed:", upload_resp.text)
        return

    filename = upload_resp.json().get("filename")
    if not filename:
        print("No filename in response.")
        return

    entry_data['image'] = f"/static/img/{filename}"


    update_payload = {entry_type: [entry_data]}
    update_resp = requests.post(f"{BASE_URL}/api/report/update", json=update_payload)

    if update_resp.ok:
        print("✅ Report updated successfully.")
    else:
        print("❌ Report update failed:", update_resp.text)


if __name__ == "__main__":
    # 1. Check if report exists, create if not
    if not report_exists():
        create_report()

    # 2. Upload image and append data
    upload_image_and_add_to_report(
        image_path="static/img/test.jpg",  # <- podmień na własną ścieżkę
        entry_type="infrastructure_changes",  # lub "incidents", "arucos"
        entry_data={
            "category": "Nowa rysa",
            "detection_time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "location": "Słup C3",
            "jury": "TAK"
        }
    )

    upload_image_and_add_to_report(
        image_path="static/img/test.jpg",  # <- podmień na własną ścieżkę
        entry_type="incidents",  # lub "incidents", "arucos"
        entry_data={
            "category": "Nowa rysa",
            "detection_time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "location": "Słup C3",
            "jury": "TAK"
        }
    )
