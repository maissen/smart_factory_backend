"""
Advanced IoT Machine Simulator with State Persistence
Generates realistic time-series metrics for industrial machines
"""
import time
import random
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from src.core.settings import settings
from src.schema.machine_schema import MachineResponseSchema

# State persistence file
STATE_FILE = Path(f".machine_state_{os.getenv('MACHINE_ID', 'default')}.json")


@dataclass
class MachineState:
    """Represents the current state of a machine"""
    status: str
    entered_at: float
    duration_seconds: int
    cycle_count: int = 0
    total_uptime: float = 0
    last_maintenance: Optional[float] = None
    temperature_baseline: float = 70.0
    wear_level: float = 0.0  # 0-100


class RealisticMachineSimulator:
    """Simulates realistic machine behavior with state transitions"""
    
    def __init__(self, machine_id: str):
        self.machine_id = machine_id
        self.state = self._load_or_create_state()
        
        # Status transition probabilities and durations (in seconds)
        self.status_config = {
            "Running": {
                "min_duration": 3600,      # 1 hour
                "max_duration": 28800,     # 8 hours
                "transitions": {
                    "Idle": 0.4,
                    "Maintenance": 0.1,
                    "Stopped": 0.05
                }
            },
            "Idle": {
                "min_duration": 1800,      # 30 minutes
                "max_duration": 7200,      # 2 hours
                "transitions": {
                    "Running": 0.7,
                    "Stopped": 0.2,
                    "Maintenance": 0.05
                }
            },
            "Maintenance": {
                "min_duration": 1800,      # 30 minutes
                "max_duration": 10800,     # 3 hours
                "transitions": {
                    "Running": 0.6,
                    "Idle": 0.3,
                    "Stopped": 0.1
                }
            },
            "Stopped": {
                "min_duration": 3600,      # 1 hour
                "max_duration": 14400,     # 4 hours
                "transitions": {
                    "Idle": 0.6,
                    "Running": 0.3,
                    "Maintenance": 0.1
                }
            }
        }
    
    def _load_or_create_state(self) -> MachineState:
        """Load existing state or create new one"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    data = json.load(f)
                    return MachineState(**data)
            except Exception as e:
                print(f"[VM-{self.machine_id}] Error loading state: {e}")
        
        # Create new state
        return MachineState(
            status="Idle",
            entered_at=time.time(),
            duration_seconds=random.randint(1800, 7200),
            last_maintenance=time.time()
        )
    
    def _save_state(self):
        """Persist state to disk"""
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            print(f"[VM-{self.machine_id}] Error saving state: {e}")
    
    def _should_transition(self) -> bool:
        """Check if machine should transition to new state"""
        current_time = time.time()
        time_in_state = current_time - self.state.entered_at
        return time_in_state >= self.state.duration_seconds
    
    def _get_next_status(self) -> str:
        """Determine next status based on probabilities"""
        current_status = self.state.status
        transitions = self.status_config[current_status]["transitions"]
        
        # Add logic: force maintenance if wear level is high
        if self.state.wear_level > 85 and current_status != "Maintenance":
            return "Maintenance"
        
        # Weighted random choice
        statuses = list(transitions.keys())
        weights = list(transitions.values())
        
        # Normalize weights to ensure they sum to 1
        total = sum(weights)
        weights = [w/total for w in weights]
        
        rand = random.random()
        cumulative = 0
        for status, weight in zip(statuses, weights):
            cumulative += weight
            if rand <= cumulative:
                return status
        
        return statuses[0]  # Fallback
    
    def _transition_state(self):
        """Transition to a new state"""
        new_status = self._get_next_status()
        config = self.status_config[new_status]
        
        # Reset wear level if entering maintenance
        if new_status == "Maintenance":
            self.state.wear_level = 0
            self.state.last_maintenance = time.time()
        
        self.state.status = new_status
        self.state.entered_at = time.time()
        self.state.duration_seconds = random.randint(
            config["min_duration"],
            config["max_duration"]
        )
        
        # Adjust temperature baseline
        self.state.temperature_baseline = {
            "Running": random.uniform(75, 85),
            "Idle": random.uniform(60, 70),
            "Maintenance": random.uniform(50, 60),
            "Stopped": random.uniform(45, 55)
        }[new_status]
        
        self._save_state()
        print(f"[VM-{self.machine_id}] State transition: {new_status} for {self.state.duration_seconds}s")
    
    def _generate_metrics(self) -> dict:
        """Generate realistic metrics based on current state"""
        status = self.state.status
        
        # Base metrics per status
        metrics_map = {
            "Running": {
                "temperature": (self.state.temperature_baseline - 5, self.state.temperature_baseline + 15),
                "power_usage": (350, 500),
                "vibration": (0.8, 2.5),
                "speed_rpm": (1200, 1500),
                "efficiency": (85, 98)
            },
            "Idle": {
                "temperature": (self.state.temperature_baseline - 5, self.state.temperature_baseline + 5),
                "power_usage": (50, 150),
                "vibration": (0.1, 0.5),
                "speed_rpm": (0, 200),
                "efficiency": (0, 20)
            },
            "Maintenance": {
                "temperature": (self.state.temperature_baseline - 3, self.state.temperature_baseline + 3),
                "power_usage": (20, 80),
                "vibration": (0.0, 0.3),
                "speed_rpm": (0, 50),
                "efficiency": (0, 0)
            },
            "Stopped": {
                "temperature": (self.state.temperature_baseline - 2, self.state.temperature_baseline + 2),
                "power_usage": (5, 30),
                "vibration": (0.0, 0.1),
                "speed_rpm": (0, 0),
                "efficiency": (0, 0)
            }
        }
        
        ranges = metrics_map[status]
        
        # Time in current state
        time_in_state = time.time() - self.state.entered_at
        
        # Generate metrics with realistic variations
        metrics = {
            "machine_id": self.machine_id,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "temperature": round(random.uniform(*ranges["temperature"]), 2),
            "power_usage": round(random.uniform(*ranges["power_usage"]), 2),
            "vibration": round(random.uniform(*ranges["vibration"]), 3),
            "speed_rpm": int(random.uniform(*ranges["speed_rpm"])),
            "efficiency": round(random.uniform(*ranges["efficiency"]), 2),
            "cycle_count": self.state.cycle_count,
            "wear_level": round(self.state.wear_level, 2),
            "time_in_state": round(time_in_state, 2),
            "state_remaining": round(self.state.duration_seconds - time_in_state, 2)
        }
        
        # Add anomalies occasionally (1% chance)
        if random.random() < 0.01:
            metrics["anomaly"] = True
            metrics["temperature"] += random.uniform(10, 25)
            metrics["vibration"] *= random.uniform(1.5, 3.0)
        else:
            metrics["anomaly"] = False
        
        # Update wear level for running machines
        if status == "Running":
            self.state.cycle_count += 1
            self.state.wear_level = min(100, self.state.wear_level + 0.01)
            
            # Calculate uptime
            if self.state.last_maintenance:
                uptime_hours = (time.time() - self.state.last_maintenance) / 3600
                metrics["hours_since_maintenance"] = round(uptime_hours, 2)
        
        return metrics
    
    def run(self):
        """Main simulation loop"""
        print(f"[VM-{self.machine_id}] Starting simulation...")
        print(f"[VM-{self.machine_id}] Initial state: {self.state.status}")
        print(f"[VM-{self.machine_id}] Reporting every {settings.PUSH_TS_DATA_PERIOD}s")
        
        while True:
            try:
                # Check for state transition
                if self._should_transition():
                    self._transition_state()
                
                # Generate and send metrics
                metrics = self._generate_metrics()
                
                # Format output for InfluxDB line protocol style
                print(f"[VM-{self.machine_id}] {metrics['status']:12} | "
                      f"Temp: {metrics['temperature']:6.2f}°C | "
                      f"Power: {metrics['power_usage']:6.2f}W | "
                      f"RPM: {metrics['speed_rpm']:4d} | "
                      f"Wear: {metrics['wear_level']:5.2f}% | "
                      f"Cycles: {metrics['cycle_count']}")
                
                # Here you would send to InfluxDB or your monitoring system
                # Example: influx_client.write_point(metrics)
                
                self._save_state()
                
            except Exception as e:
                print(f"[VM-{self.machine_id}] Error: {e}")
            
            time.sleep(settings.PUSH_TS_DATA_PERIOD)


# Main execution
if __name__ == "__main__":
    machine_id = os.getenv("MACHINE_ID", "MACHINE_001")
    simulator = RealisticMachineSimulator(machine_id)
    simulator.run()