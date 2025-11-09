import time
import random
from src.core.settings import settings
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
