import requests
import json
from datetime import datetime

# Base URL of your running Flask app
BASE_URL = "http://127.0.0.1:5000"

# Step 1: Create test data to POST
custom_data = {
    "team": "dupa Team",
    "email": "kontakt@dronix.pl",
    "pilot": "Jan Nowak",
    "phone": "+48123456789",
    "mission_time": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    "mission_no": "MISSION-42",
    "duration": "12:34",
    "battery_before": "95% / 16.7 V",
    "battery_after": "60% / 15.6 V",
    "kp_index": 5,
    "infrastructure_changes": [],
    "incidents": [],
    "arucos": [],
    "infra_map": "/static/img/mapa.jpg",
    "final_info": [
        {"desc": "Test punkt 1", "points": "3"},
        {"desc": "Suma punktów", "points": "3", "class": "bold"}
    ]
}

# Step 2: POST the data
post_response = requests.post(f"{BASE_URL}/api/report", json=custom_data)
print("POST Status:", post_response.status_code)
print("POST Response:", post_response.json())

# Step 3: GET the data back
get_response = requests.get(f"{BASE_URL}/api/report")
print("\nGET Status:", get_response.status_code)
print("GET Response:", get_response.json())
# print(json.dumps(get_response.json(), indent=2, ensure_ascii=False))
