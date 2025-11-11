# Possible notes for MACHINE_POSSIBLE_STATUS

running_notes = [
    "Started production batch #101",
    "Resumed operation after maintenance",
    "Operating at full capacity",
    "Processing order #547",
    "Running continuous shift",
    "Machine performing optimally",
    "Production line 3 active",
    "Executing scheduled task",
    "Running test batch",
    "Monitoring production parameters",
    "Operating at 95% efficiency",
    "Processing high-priority order",
    "Continuous operation without errors",
    "Executing standard run cycle",
    "Machine started after downtime",
    "Production ongoing smoothly",
    "Running quality check batch",
    "Production target met so far",
    "Operating under normal load",
    "Machine warmed up and running",
    "Start of morning shift",
    "Processing special request batch",
    "Running in automatic mode",
    "Machine running with reduced speed",
    "Executing standard production plan",
    "Continuous monitoring active",
    "Production output stable",
    "Running calibration batch",
    "Operating with minimal intervention",
    "Monitoring system logs while running",
    "Processing bulk order",
    "Running at 80% capacity",
    "Machine operating under normal load",
    "Production cycle started",
    "Executing routine task",
    "Machine running with backup power",
    "Continuous operation in progress",
    "Running scheduled maintenance checks",
    "Operating smoothly with no errors"
]

idle_notes = [
    "Machine idle between shifts",
    "Waiting for next production batch",
    "Paused due to low material supply",
    "Idle during maintenance check",
    "Machine stopped temporarily",
    "Awaiting operator input",
    "Idle while system updates",
    "Waiting for upstream process",
    "Machine on standby mode",
    "Paused to change tools",
    "Idle due to scheduling conflict",
    "Machine waiting for maintenance approval",
    "Idle during inspection",
    "Paused while operators adjust settings",
    "Idle for safety inspection",
    "Machine on hold",
    "Idle between jobs",
    "Paused for quality check",
    "Machine idle while calibrating sensors",
    "Waiting for batch assignment",
    "Idle during equipment upgrade",
    "Paused for cleaning",
    "Machine waiting for next instruction",
    "Idle while awaiting parts",
    "Paused due to low energy supply",
    "Machine in standby mode",
    "Idle while waiting for operator",
    "Paused between shifts",
    "Machine waiting for restart signal",
    "Idle due to shift change",
    "Paused for minor adjustments",
    "Machine idle for inventory check",
    "Waiting for production schedule",
    "Idle during tool replacement",
    "Paused for maintenance setup",
    "Machine waiting for process start",
    "Idle due to technical inspection",
    "Paused for safety protocols",
    "Machine waiting for calibration"
]

maintenance_notes = [
    "Performed routine lubrication",
    "Replaced worn-out belt",
    "Calibrated sensors",
    "Checked motor alignment",
    "Updated machine firmware",
    "Replaced faulty part",
    "Conducted preventive maintenance",
    "Cleaned machine components",
    "Tightened loose screws",
    "Checked hydraulic system",
    "Replaced coolant",
    "Tested emergency stop",
    "Inspected wiring connections",
    "Checked pneumatic system",
    "Performed software update",
    "Replaced filters",
    "Checked temperature sensors",
    "Calibrated machine speed",
    "Inspected bearings",
    "Replaced worn gears",
    "Checked alignment of rollers",
    "Performed vibration analysis",
    "Updated maintenance logs",
    "Lubricated moving parts",
    "Replaced drive belts",
    "Checked pressure valves",
    "Calibrated control panel",
    "Inspected safety shields",
    "Cleaned dust and debris",
    "Replaced defective sensors",
    "Checked electrical contacts",
    "Performed torque test",
    "Inspected hydraulic hoses",
    "Tested machine startup",
    "Performed software diagnostics",
    "Lubricated chain drive",
    "Adjusted conveyor alignment",
    "Checked cooling system",
    "Replaced worn seals"
]

stopped_notes = [
    "Machine stopped due to emergency",
    "Power outage caused halt",
    "Stopped for material shortage",
    "Production stopped for inspection",
    "Machine stopped after shift end",
    "Stopped due to equipment failure",
    "Production halted for safety check",
    "Stopped for unscheduled maintenance",
    "Machine stopped for cleaning",
    "Stopped due to operator request",
    "Production paused due to calibration",
    "Stopped to replace faulty component",
    "Machine stopped due to sensor error",
    "Stopped because of overload",
    "Production halted for tool change",
    "Stopped for routine inspection",
    "Machine stopped due to jam",
    "Stopped due to high temperature",
    "Production paused for quality review",
    "Stopped to reset control panel",
    "Machine stopped for system update",
    "Stopped after detecting vibration",
    "Production halted for software error",
    "Stopped for minor repair",
    "Machine stopped to prevent damage",
    "Stopped due to unexpected shutdown",
    "Production halted for cleaning",
    "Stopped for inventory check",
    "Machine stopped due to low coolant",
    "Stopped after shift completion",
    "Production halted due to maintenance",
    "Stopped to replace worn-out part",
    "Machine stopped for troubleshooting",
    "Stopped due to pneumatic failure",
    "Production paused for adjustment",
    "Stopped because of safety trigger",
    "Machine stopped due to overload",
    "Stopped due to operator intervention",
    "Production halted for inspection",
    "Stopped while waiting for spare parts"
]

import random
def get_random_note_for_status(status: str) -> str:
    """
    Returns a random note corresponding to the given machine status.
    
    Args:
        status (str): One of "Running", "Idle", "Maintenance", "Stopped"
        
    Returns:
        str: A random note from the appropriate list.
        
    Raises:
        ValueError: If the status is invalid.
    """
    status = status.capitalize()  # Ensure consistent capitalization
    if status == "Running":
        return random.choice(running_notes)
    elif status == "Idle":
        return random.choice(idle_notes)
    elif status == "Maintenance":
        return random.choice(maintenance_notes)
    elif status == "Stopped":
        return random.choice(stopped_notes)
    else:
        raise ValueError(f"Invalid status '{status}'. Must be one of: Running, Idle, Maintenance, Stopped")