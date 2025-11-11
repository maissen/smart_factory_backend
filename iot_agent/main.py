"""
Advanced IoT Machine Simulator with Realistic State Transitions
Generates time-series metrics for industrial machines using Markov chains
"""
import time
import random
import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


# ============================================================================
# CONFIGURATION
# ============================================================================
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend_app:7000")
API_MACHINES_ENDPOINT = os.getenv("API_MACHINES_ENDPOINT", "/api/machine/all")
API_INFLUX_ENDPOINT = os.getenv("API_INFLUX_ENDPOINT", "/api/influx/insert")
GENERATION_FREQUENCY = int(os.getenv("GENERATION_FREQUENCY", "30"))  # seconds
METRICS_DIR = Path(os.getenv("METRICS_DIR", "metrics_data"))
STATE_DIR = Path(os.getenv("STATE_DIR", "machine_states"))
HISTORY_DIR = Path(os.getenv("HISTORY_DIR", "history"))
HISTORY_WINDOW_HOURS = int(os.getenv("HISTORY_WINDOW_HOURS", "24"))

# Create directories
METRICS_DIR.mkdir(exist_ok=True)
STATE_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)


# ============================================================================
# STATE TRANSITION MATRIX (Markov Chain)
# ============================================================================
STATE_TRANSITIONS = {
    "Running": {
        "Running": 0.45,
        "Idle": 0.40,
        "Maintenance": 0.10,
        "Stopped": 0.05
    },
    "Idle": {
        "Running": 0.60,
        "Idle": 0.25,
        "Maintenance": 0.05,
        "Stopped": 0.10
    },
    "Maintenance": {
        "Running": 0.80,
        "Idle": 0.10,
        "Maintenance": 0.05,
        "Stopped": 0.05
    },
    "Stopped": {
        "Running": 0.50,
        "Idle": 0.30,
        "Maintenance": 0.10,
        "Stopped": 0.10
    }
}


# State duration ranges (min, max in seconds)
STATE_DURATIONS = {
    "Running": (3600, 28800),      # 1-8 hours
    "Idle": (1800, 7200),          # 30 min - 2 hours
    "Maintenance": (1800, 10800),  # 30 min - 3 hours
    "Stopped": (3600, 14400)       # 1-4 hours
}


# Metric ranges per state: (temp_min, temp_max, power_min, power_max)
STATE_METRICS = {
    "Running": {
        "temperature": (70.0, 95.0),
        "power": (350.0, 500.0),
        "temp_volatility": 3.0,
        "power_volatility": 20.0
    },
    "Idle": {
        "temperature": (55.0, 70.0),
        "power": (50.0, 150.0),
        "temp_volatility": 1.5,
        "power_volatility": 10.0
    },
    "Maintenance": {
        "temperature": (45.0, 60.0),
        "power": (20.0, 80.0),
        "temp_volatility": 0.8,
        "power_volatility": 5.0
    },
    "Stopped": {
        "temperature": (40.0, 55.0),
        "power": (5.0, 30.0),
        "temp_volatility": 0.5,
        "power_volatility": 3.0
    }
}


# ============================================================================
# DATA MODELS
# ============================================================================
@dataclass
class MachineState:
    """Current state of a machine"""
    machine_id: int
    machine_name: str
    status: str
    entered_at: float
    duration_seconds: int
    temperature: float
    power_usage: float
    wear_level: float = 0.0
    cycle_count: int = 0
    last_maintenance: Optional[float] = None
    total_uptime: float = 0.0


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: float
    temperature: float
    power_usage: float
    status: str


# ============================================================================
# MACHINE SIMULATOR
# ============================================================================
class RealisticMachineSimulator:
    """Simulates a single machine with realistic behavior"""
    
    def __init__(self, machine_id: int, machine_name: str, initial_status: str = "Idle"):
        self.machine_id = machine_id
        self.machine_name = machine_name
        self.state_file = STATE_DIR / f"machine_{machine_id}.json"
        self.history_file = HISTORY_DIR / f"machine_{machine_id}_history.json"
        
        # Load or initialize state
        self.state = self._load_or_create_state(initial_status)
        self.history = self._load_history()
        
    def _load_or_create_state(self, initial_status: str) -> MachineState:
        """Load existing state or create new one"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return MachineState(**data)
            except Exception as e:
                print(f"[Machine-{self.machine_id}] Error loading state: {e}")
        
        # Create fresh state
        config = STATE_METRICS[initial_status]
        return MachineState(
            machine_id=self.machine_id,
            machine_name=self.machine_name,
            status=initial_status,
            entered_at=time.time(),
            duration_seconds=random.randint(*STATE_DURATIONS[initial_status]),
            temperature=random.uniform(*config["temperature"]),
            power_usage=random.uniform(*config["power"]),
            last_maintenance=time.time()
        )
    
    def _load_history(self) -> List[MetricPoint]:
        """Load metric history from last 24 hours"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                
            # Filter to keep only last HISTORY_WINDOW_HOURS
            cutoff = time.time() - (HISTORY_WINDOW_HOURS * 3600)
            history = [
                MetricPoint(**point) 
                for point in data 
                if point['timestamp'] > cutoff
            ]
            
            return history
        except Exception as e:
            print(f"[Machine-{self.machine_id}] Error loading history: {e}")
            return []
    
    def _save_state(self):
        """Persist state to disk"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            print(f"[Machine-{self.machine_id}] Error saving state: {e}")
    
    def _save_history(self):
        """Persist history to disk"""
        try:
            # Keep only recent history
            cutoff = time.time() - (HISTORY_WINDOW_HOURS * 3600)
            recent_history = [
                asdict(point) 
                for point in self.history 
                if point.timestamp > cutoff
            ]
            
            with open(self.history_file, 'w') as f:
                json.dump(recent_history, f, indent=2)
        except Exception as e:
            print(f"[Machine-{self.machine_id}] Error saving history: {e}")
    
    def _should_transition(self) -> bool:
        """Check if machine should change state"""
        elapsed = time.time() - self.state.entered_at
        return elapsed >= self.state.duration_seconds
    
    def _get_next_state(self) -> str:
        """Use Markov chain to determine next state"""
        current = self.state.status
        
        # Force maintenance if wear is critical
        if self.state.wear_level > 85 and current != "Maintenance":
            return "Maintenance"
        
        # Use transition probabilities
        transitions = STATE_TRANSITIONS.get(current, STATE_TRANSITIONS["Idle"])
        states = list(transitions.keys())
        probabilities = list(transitions.values())
        
        # Weighted random choice
        return random.choices(states, weights=probabilities, k=1)[0]
    
    def _transition_to_new_state(self):
        """Perform state transition"""
        new_state = self._get_next_state()
        config = STATE_METRICS[new_state]
        
        # Reset wear if entering maintenance
        if new_state == "Maintenance":
            self.state.wear_level = 0
            self.state.last_maintenance = time.time()
        
        # Update state
        self.state.status = new_state
        self.state.entered_at = time.time()
        self.state.duration_seconds = random.randint(*STATE_DURATIONS[new_state])
        
        # Gradually adjust metrics toward new state baseline
        target_temp = random.uniform(*config["temperature"])
        target_power = random.uniform(*config["power"])
        
        # Smooth transition (move 30% toward target)
        self.state.temperature += (target_temp - self.state.temperature) * 0.3
        self.state.power_usage += (target_power - self.state.power_usage) * 0.3
        
        self._save_state()
        print(f"[Machine-{self.machine_id}] → {new_state} for {self.state.duration_seconds}s")
    
    def _update_metrics_smoothly(self):
        """Update metrics with realistic variations"""
        config = STATE_METRICS[self.state.status]
        
        # Add small random walk with mean reversion
        temp_range = config["temperature"]
        power_range = config["power"]
        temp_volatility = config["temp_volatility"]
        power_volatility = config["power_volatility"]
        
        # Temperature: random walk with bounds
        temp_change = random.gauss(0, temp_volatility)
        new_temp = self.state.temperature + temp_change
        # Mean reversion toward center of range
        target_temp = (temp_range[0] + temp_range[1]) / 2
        new_temp += (target_temp - new_temp) * 0.05
        self.state.temperature = max(temp_range[0], min(temp_range[1], new_temp))
        
        # Power: similar logic
        power_change = random.gauss(0, power_volatility)
        new_power = self.state.power_usage + power_change
        target_power = (power_range[0] + power_range[1]) / 2
        new_power += (target_power - new_power) * 0.05
        self.state.power_usage = max(power_range[0], min(power_range[1], new_power))
        
        # Update wear (increases faster when Running)
        wear_rate = {"Running": 0.1, "Idle": 0.02, "Maintenance": -0.5, "Stopped": 0.0}
        self.state.wear_level += wear_rate.get(self.state.status, 0.05)
        self.state.wear_level = max(0, min(100, self.state.wear_level))
        
        # Increment cycle counter if running
        if self.state.status == "Running":
            self.state.cycle_count += 1
    
    def generate_metrics(self) -> Dict:
        """Generate current metrics snapshot"""
        timestamp_sec = time.time()
        timestamp_ns = int(timestamp_sec * 1e9)
        
        # Force 0 values for Stopped and Maintenance states
        if self.state.status in ["Stopped", "Maintenance"]:
            temperature = 0.0
            power_usage = 0.0
        else:
            temperature = round(self.state.temperature, 2)
            power_usage = round(self.state.power_usage, 2)
        
        return {
            "machine_id": self.machine_id,
            "machine_name": self.machine_name,
            "status": self.state.status,
            "temperature": temperature,
            "power_usage": power_usage,
            "timestamp": datetime.now().isoformat(),
            "timestamp_ns": timestamp_ns
        }
    
    def generate_influx_line(self, metrics: Dict) -> str:
        """Convert to InfluxDB Line Protocol"""
        measurement = "machine_metrics"
        
        # Tags (indexed, low cardinality)
        tags = [
            f"machine_id={metrics['machine_id']}",
            f"machine_name={metrics['machine_name'].replace(' ', '_')}",
            f"status={metrics['status']}"
        ]
        tag_set = ",".join(tags)
        
        # Fields (not indexed, actual values)
        fields = [
            f"temperature={metrics['temperature']}",
            f"power_usage={metrics['power_usage']}"
        ]
        field_set = ",".join(fields)
        
        # InfluxDB line format: measurement,tags fields timestamp
        return f"{measurement},{tag_set} {field_set} {metrics['timestamp_ns']}"
    
    def update(self) -> Dict:
        """Main update: check transitions, update metrics, return data"""
        # Check for state transition
        if self._should_transition():
            self._transition_to_new_state()
        
        # Update metrics smoothly
        self._update_metrics_smoothly()
        
        # Generate current snapshot
        metrics = self.generate_metrics()
        
        # Add InfluxDB line
        metrics['influx_line'] = self.generate_influx_line(metrics)
        
        # Record in history (use time.time() for timestamp)
        self.history.append(MetricPoint(
            timestamp=time.time(),
            temperature=metrics['temperature'],
            power_usage=metrics['power_usage'],
            status=metrics['status']
        ))
        
        # Persist
        self._save_state()
        self._save_history()
        
        return metrics


# ============================================================================
# MULTI-MACHINE ORCHESTRATOR
# ============================================================================
class MultiMachineSimulator:
    """Manages all machine simulators"""
    
    def __init__(self):
        self.simulators: List[RealisticMachineSimulator] = []
        self.api_machines_url = f"{API_BASE_URL}{API_MACHINES_ENDPOINT}"
        self.api_influx_url = f"{API_BASE_URL}{API_INFLUX_ENDPOINT}"
        self.iteration = 0
    
    def fetch_machines_from_api(self):
        """Fetch machine list from API"""
        print(f"[Simulator] Fetching machines from: {self.api_machines_url}")
        
        try:
            response = requests.get(self.api_machines_url, timeout=10)
            response.raise_for_status()
            
            machines = response.json()
            
            if not machines:
                print("[Simulator] ⚠️  No machines returned from API")
                return
            
            print(f"[Simulator] ✓ Found {len(machines)} machines")
            
            # Clear existing simulators
            self.simulators.clear()
            
            # Create simulator for each machine
            for machine in machines:
                machine_id = machine.get('id') or machine.get('machine_id')
                machine_name = machine.get('name') or machine.get('machine_name')
                machine_status = machine.get('status', 'Idle')
                
                if machine_id and machine_name:
                    sim = RealisticMachineSimulator(
                        machine_id=machine_id,
                        machine_name=machine_name,
                        initial_status=machine_status
                    )
                    self.simulators.append(sim)
                    print(f"  → {machine_name} (ID:{machine_id}, Status:{machine_status})")
            
        except requests.exceptions.RequestException as e:
            print(f"[Simulator] ✗ API error: {e}")
            raise
    
    def push_to_influx_api(self, metrics_batch: List[Dict]):
        """Push metrics to backend InfluxDB endpoint"""
        
        # Clean up metrics to match API schema
        cleaned_metrics = []
        for m in metrics_batch:
            cleaned_metric = {
                "machine_id": m["machine_id"],
                "machine_name": m["machine_name"],
                "status": m["status"],
                "temperature": m["temperature"],
                "power_usage": m["power_usage"],
                "timestamp": m["timestamp"],  # Already ISO format
                "timestamp_ns": m["timestamp_ns"],
                "influx_line": m["influx_line"]
            }
            cleaned_metrics.append(cleaned_metric)
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "metrics": cleaned_metrics
        }
        
        try:
            
            response = requests.post(
                self.api_influx_url, 
                json=payload, 
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print(f"[Push] ✓ Sent {len(cleaned_metrics)} metrics to InfluxDB API")
        
        except requests.exceptions.HTTPError as e:
            print(f"[Push] ✗ HTTP Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"[Push] Response body: {e.response.text}")
            # Try to parse error details
            try:
                error_detail = e.response.json()
                print(f"[Push] Error details: {json.dumps(error_detail, indent=2)}")
            except:
                pass
                
        except requests.exceptions.RequestException as e:
            print(f"[Push] ✗ Request failed: {e}")
    
    def export_to_influx_file(self, metrics_batch: List[Dict]):
        """Write InfluxDB lines to timestamped file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = METRICS_DIR / f"influx_{timestamp}.txt"
        
        try:
            with open(filepath, 'w') as f:
                for m in metrics_batch:
                    f.write(m['influx_line'] + '\n')
            print(f"[Export] ✓ Saved to {filepath.name}")
        except Exception as e:
            print(f"[Export] ✗ Error: {e}")
    
    def export_to_json(self, metrics_batch: List[Dict]):
        """Export full metrics as JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = METRICS_DIR / f"metrics_{timestamp}.json"
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "iteration": self.iteration,
                "count": len(metrics_batch),
                "metrics": metrics_batch
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[Export] ✓ JSON saved to {filepath.name}")
        except Exception as e:
            print(f"[Export] ✗ Error: {e}")
    
    def run(self):
        """Main simulation loop"""
        print("\n" + "="*80)
        print("🚀 Starting IoT Machine Simulator")
        print("="*80)
        
        while True:
            try:
                self.iteration += 1
                print(f"\n{'='*80}")
                print(f"Iteration {self.iteration} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*80}")
                
                # Fetch latest machine list
                self.fetch_machines_from_api()
                
                if not self.simulators:
                    print("[Simulator] No machines to simulate, waiting...")
                    time.sleep(GENERATION_FREQUENCY)
                    continue
                
                # Generate metrics for all machines
                metrics_batch = []
                
                print(f"\n📊 Generating metrics:")
                for sim in self.simulators:
                    metrics = sim.update()
                    metrics_batch.append(metrics)
                    
                    print(f"  [{sim.machine_name:20}] "
                          f"{metrics['status']:12} | "
                          f"🌡️  {metrics['temperature']:6.2f}°C | "
                          f"⚡ {metrics['power_usage']:6.2f}W")
                
                # Push to backend
                self.push_to_influx_api(metrics_batch)
                
                # Export to files
                self.export_to_influx_file(metrics_batch)
                self.export_to_json(metrics_batch)
                
                print(f"\n⏱️  Sleeping {GENERATION_FREQUENCY}s...")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Simulator stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error in simulation loop: {e}")
                print(f"Retrying in {GENERATION_FREQUENCY}s...")
            
            time.sleep(GENERATION_FREQUENCY)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
def main():
    """Main entry point with startup checks"""
    print("\n" + "="*80)
    print("IoT Machine Simulator - Realistic State Transitions")
    print("="*80)
    print(f"API Base URL:         {API_BASE_URL}")
    print(f"Machines Endpoint:    {API_MACHINES_ENDPOINT}")
    print(f"InfluxDB Endpoint:    {API_INFLUX_ENDPOINT}")
    print(f"Generation Frequency: {GENERATION_FREQUENCY}s")
    print(f"Metrics Directory:    {METRICS_DIR.absolute()}")
    print(f"State Directory:      {STATE_DIR.absolute()}")
    print(f"History Window:       {HISTORY_WINDOW_HOURS} hours")
    print("="*80)
    
    # Retry logic for initial connection
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n[Startup] Attempt {attempt}/{max_retries}")
            simulator = MultiMachineSimulator()
            simulator.fetch_machines_from_api()
            
            if simulator.simulators:
                print(f"\n✓ Successfully initialized with {len(simulator.simulators)} machines")
                simulator.run()
                break
            else:
                raise ValueError("No machines loaded from API")
                
        except Exception as e:
            if attempt < max_retries:
                print(f"❌ Startup failed: {e}")
                print(f"⏱️  Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"\n❌ Failed after {max_retries} attempts")
                print("Please check:")
                print("  1. API server is running")
                print("  2. API_BASE_URL is correct")
                print("  3. Machines endpoint returns data")
                raise


if __name__ == "__main__":
    main()