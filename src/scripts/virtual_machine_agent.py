import time
import random
# import requests
import os

MACHINE_ID = os.getenv("MACHINE_ID")

while True:
    metrics = {
        "machine_id": MACHINE_ID,
        "temperature": random.uniform(50, 120),
        "power_usage": random.uniform(100, 500),
        "uptime": random.uniform(90, 100)
    }

    try:
        print(f"[VM-{MACHINE_ID}] Sent:", metrics)

    except Exception as e:
        print(f"[VM-{MACHINE_ID}] Error:", e)

    time.sleep(1)
