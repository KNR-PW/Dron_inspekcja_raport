import random
from datetime import datetime, timedelta

def generate_random_report():
    now = datetime.now()
    start_time = now - timedelta(minutes=random.randint(10, 30))
    duration = (now - start_time).seconds

    # Dodaj losowych pracowników (sekcja 3)
    employees = [
        {
            "present": random.choice(["Jest", "Nie ma"]),
            "bhp": random.choice(["Tak", "Nie"]),
            "location": "Lat 41.40338, Long 2.17403",
            "location_changed": random.choice(["Tak", "Nie"]),
            "image": "/static/img/employee.jpg",
            "jury": random.choice(["+", "-"])
        } for _ in range(random.randint(3, 6))
    ]

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
        "employees": employees,   # <-- dodane!
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
        "infra_map": "/static/img/mapa.jpg",
        "final_info": [
            {"desc": "Uzupełnia Komisja Sędziowska", "points": "", "class": "special"},
            {"desc": "Lot ZERO z poprawnym przygotowanym raportem początkowym", "points": "", "class": "crossed"},
            {"desc": "Automatyczny start, lot i lądowanie", "points": ""},
            {"desc": "Poprawne wykrycie i raportowanie zmiany w infrastrukturze stałej (zmiany statyczne)", "points": ""},
            {"desc": "Poprawne wykrycie i raportowanie o pracownikach", "points": ""},
            {"desc": "Poprawne wykrycie zdarzenia nadzwyczajnego", "points": ""},
            {"desc": "Wykrycie i odczytanie kodów ArUCo", "points": ""},
            {"desc": "Najkrótszy czas wykonania całej misji (lot + raport)", "points": ""},
            {"desc": "Premia za wysłanie raportu jeszcze w trakcie lotu lub jednocześnie wraz z lądowaniem", "points": ""},
            {"desc": "Punkty karne", "points": ""},
            {"desc": "Suma punktów", "points": "", "class": "bold"}
        ]
    }
    return report

def build_report(
    team: str = "",
    email: str = "",
    pilot: str = "",
    phone: str = "",
    mission_time: datetime = datetime.now(),
    mission_no: str = "",
    duration: str = "",
    battery_before: str = "",
    battery_after: str = "",
    kp_index: int = 0,
    employees: list = None,  # <-- dodane!
    infrastructure_changes: list = None,
    incidents: list = None,
    arucos: list = None,
    infra_map: str = "/static/img/mapa.jpg"
):
    if employees is None:
        employees = []
    if infrastructure_changes is None:
        infrastructure_changes = []
    if incidents is None:
        incidents = []
    if arucos is None:
        arucos = []

    return {
        "team": team,
        "email": email,
        "pilot": pilot,
        "phone": phone,
        "mission_time": mission_time.strftime("%d/%m/%Y, %H:%M:%S"),
        "mission_no": mission_no,
        "duration": duration,
        "battery_before": battery_before,
        "battery_after": battery_after,
        "kp_index": kp_index,
        "employees": employees,  # <-- dodane!
        "infrastructure_changes": infrastructure_changes,
        "incidents": incidents,
        "arucos": arucos,
        "infra_map": infra_map,
        "final_info": [
            {"desc": "Uzupełnia Komisja Sędziowska", "points": "", "class": "special"},
            {"desc": "Lot ZERO z poprawnym przygotowanym raportem początkowym", "points": "", "class": "crossed"},
            {"desc": "Automatyczny start, lot i lądowanie", "points": ""},
            {"desc": "Poprawne wykrycie i raportowanie zmiany w infrastrukturze stałej (zmiany statyczne)", "points": ""},
            {"desc": "Poprawne wykrycie i raportowanie o pracownikach", "points": ""},
            {"desc": "Poprawne wykrycie zdarzenia nadzwyczajnego", "points": ""},
            {"desc": "Wykrycie i odczytanie kodów ArUCo", "points": ""},
            {"desc": "Najkrótszy czas wykonania całej misji (lot + raport)", "points": ""},
            {"desc": "Premia za wysłanie raportu jeszcze w trakcie lotu lub jednocześnie wraz z lądowaniem", "points": ""},
            {"desc": "Punkty karne", "points": ""},
            {"desc": "Suma punktów", "points": "", "class": "bold"}
        ]
    }