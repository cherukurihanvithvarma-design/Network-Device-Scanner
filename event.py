import csv
import os
from datetime import datetime

CSV_FILE = "router_events.csv"

def add_event(mac, ip, network_id):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "MAC",
                "IP",
                "Network"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            mac,
            ip,
            network_id
        ])