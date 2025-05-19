import random
from datetime import datetime, timedelta

def generate_random_report():
    now = datetime.now()
    start_time = now - timedelta(minutes=random.randint(10, 30))
    duration = (now - start_time).seconds

    report = {
        "team": "Dronix",
        "email": "kontakt@dronix.pl",
        "pilot": "Jan Kowalski",
        "phone": "+48123456789",
        "mission_time": start_time.strftime("%d/%m/%Y, %H:%M:%S"),
        "mission_no": random.choice(["ZERO", "01", "02", "03"]),
        "duration": f"{duration // 60:02}:{duration % 60:02}",
        "battery_before": f"{random.randint(80, 100)}% / {random.uniform(16.0, 16.8):.2f} V",
        "battery_after": f"{random.randint(30, 60)}% / {random.uniform(15.0, 16.0):.2f} V",
        "kp_index": random.randint(1, 10),
        "infrastructure_changes": [
            {
                "category": random.choice([
                    "Rurociąg", "Linia wysokiego napięcia", "Ogrodzenie", "Pozostawiony sprzęt"
                ]),
                "detection_time": now.strftime("%d/%m/%Y, %H:%M:%S"),
                "location": "Lat 41.40338, Long 2.17403",
                "image": "/static/img/pipe.jpg",
                "jury": random.choice(["+", "-"])
            } for _ in range(random.randint(2, 5))
        ],
        "incidents": [
            {
                "event": "Intruz",
                "time": now.strftime("%d/%m/%Y, %H:%M:%S"),
                "location": "Lat 41.40338, Long 2.17403",
                "image": "/static/img/intruder.jpg",
                "notified": random.choice(["Tak", "Nie"]),
                "jury": random.choice(["+", "-"])
            }
        ],
        "arucos": [
            {
                "content": f"{random.randint(10,99)}",
                "location": "Lat 41.40338, Long 2.17403",
                "location_changed": random.choice(["Tak", "Nie"]),
                "content_changed": random.choice(["Tak", "Nie", "LiczbaData Tak/Nie"]),
                "image": f"/static/img/aruco{random.randint(1,2)}.png",
                "jury": random.choice(["+", "-"])
            } for _ in range(2)
        ],
        "infra_map": "/static/img/mapa.jpg"
    }
    return report