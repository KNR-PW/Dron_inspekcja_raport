import requests
import json

BASE_URL = "http://localhost:5000/api/report"

def print_response(response):
    print(f"\n{response.status_code} {response.reason}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(response.text)

def test_create():
    print("== CREATE REPORT ==")
    payload = {
        "team": "Dronix",
        "email": "kontakt@dronix.pl",
        "pilot": "Jan Kowalski",
        "phone": "+48123456789",
        "mission_time": "24/05/2025, 15:00:00",
        "mission_no": "01",
        "duration": "10:00",
        "battery_before": "95% / 16.7 V",
        "battery_after": "40% / 15.3 V",
        "kp_index": 4,
        "infrastructure_changes": [],
        "incidents": [],
        "arucos": []
    }
    response = requests.post(f"{BASE_URL}/create", json=payload)
    print_response(response)

def test_get():
    print("== GET REPORT ==")
    response = requests.get(BASE_URL)
    print_response(response)

def test_update():
    print("== UPDATE REPORT ==")
    payload = {
        "battery_after": "35% / 15.1 V",
        "kp_index": 6
    }
    response = requests.post(f"{BASE_URL}/update", json=payload)
    print_response(response)

def test_delete():
    print("== DELETE REPORT ==")
    response = requests.delete(f"{BASE_URL}/delete")
    print_response(response)

def run_all_tests():
    test_create()
    test_get()
    test_update()
    test_get()
    test_delete()
    test_get()

if __name__ == "__main__":
    run_all_tests()
