import os
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000"
IMAGE_FOLDER = "static/img"  # folder, do którego wrzucasz zdjęcia


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


def upload_image(filename):
    path = os.path.join(IMAGE_FOLDER, filename)
    try:
        with open(path, 'rb') as f:
            files = {'image': f}
            resp = requests.post(f"{BASE_URL}/api/report/image", files=files)
            print(f"[UPLOAD] {filename} → {resp.status_code} → {resp.text}")
            if resp.status_code == 200:
                return resp.json().get("filename")
    except Exception as e:
        print(f"Błąd otwierania pliku {filename}: {e}")
    return None


def add_to_report(entry_type, entry_data_list):
    payload = {entry_type: entry_data_list}
    resp = requests.post(f"{BASE_URL}/api/report/update", json=payload)
    if resp.ok:
        print(f"✅ Dodano {len(entry_data_list)} do {entry_type}")
    else:
        print(f"❌ Błąd dodawania do {entry_type}: {resp.text}")


def prepare_entries_from_images():
    all_files = os.listdir(IMAGE_FOLDER)
    all_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print("[INFO] Wczytano zdjęcia:", all_files)

    infra, incidents, arucos, employees = [], [], [], []

    for idx, fname in enumerate(sorted(all_files)):
        fname_lower = fname.lower()
        uploaded = upload_image(fname)
        if not uploaded:
            continue

        now_str = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        image_path = f"/static/img/{uploaded}"

        if "infra" in fname_lower:
            infra.append({
                "category": f"Uszkodzenie {idx}",
                "detection_time": now_str,
                "location": f"Lat 52.{idx}, Long 21.{idx}",
                "image": image_path,
                "jury": "+"
            })

        elif "aruco" in fname_lower:
            arucos.append({
                "content": f"Kod {idx}",
                "location": f"Lat 52.{idx}, Long 21.{idx}",
                "location_changed": "Nie",
                "content_changed": "Nie",
                "image": image_path,
                "jury": "-"
            })

        elif "inc" in fname_lower or "event" in fname_lower:
            incidents.append({
                "event": f"Zdarzenie {idx}",
                "time": now_str,
                "location": f"Lat 52.{idx}, Long 21.{idx}",
                "image": image_path,
                "notified": "Tak",
                "jury": "+"
            })

        elif "emp" in fname_lower or "worker" in fname_lower:
            employees.append({
                "present": "Jest",
                "bhp": "Tak",
                "location": f"Lat 52.{idx}, Long 21.{idx}",
                "location_changed": "Nie",
                "image": image_path,
                "jury": "+"
            })

    return infra, incidents, arucos, employees


if __name__ == "__main__":
    if not report_exists():
        create_report()

    infra, incs, arus, emps = prepare_entries_from_images()

    if infra:
        add_to_report("infrastructure_changes", infra)
    if incs:
        add_to_report("incidents", incs)
    if arus:
        add_to_report("arucos", arus)
    if emps:
        add_to_report("employees", emps)
