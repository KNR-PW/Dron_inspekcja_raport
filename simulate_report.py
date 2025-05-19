# Symulacja testowa – generuje i zapisuje przykładowy raport do pliku JSON

from inspection_report import generate_random_report
import json

if __name__ == "__main__":
    report = generate_random_report()
    with open("sample_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("Wygenerowano przykładowy raport: sample_report.json")