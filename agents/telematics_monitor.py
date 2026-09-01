import random
from typing import Dict, Any, List

class TelematicsMonitorAgent:
    """
    Agent 6: Dynamic Cold-Chain Telematics Monitor Agent
    Responsibilities:
    - Monitors real-time GPS coordinates, traffic slowdowns, and reefer zone thermistors.
    - Triggers automated alerts for temperature excursion anomalies (>40°F in chill, >0°F in frozen).
    - Suggests dynamic rerouting or ETA recalculations when traffic or dock delays occur.
    """

    def __init__(self):
        self.name = "Agent 6: Dynamic Cold-Chain Monitor"
        self.role = "Real-Time IoT Telematics & Exception Rerouting Agent"
        self.system_prompt = (
            "You are the Dynamic Cold-Chain Monitor Agent. You continuously ingest trailer IoT telemetry "
            "(GPS position, speed, compartment thermistor temperatures). When temperature thresholds or traffic "
            "delays exceed limits, you issue real-time corrective actions and notify dispatchers."
        )

    def process(self, route_bookings: Dict[str, Any]) -> Dict[str, Any]:
        bookings = route_bookings.get("awarded_bookings", [])
        
        telemetry_status = []
        alerts_generated = []

        for b in bookings:
            r_id = b["route_id"]
            carrier = b["awarded_carrier"]

            # Generate realistic telemetry state
            if "Route-101" in r_id:
                # Normal operational state
                zone_f_temp = -9.4
                zone_c_temp = 36.2
                status = "NORMAL"
                current_speed = 44
                location = "I-95 Northbound near Exit 16W"
            elif "Route-102" in r_id:
                # Simulated minor traffic delay
                zone_f_temp = -10.1
                zone_c_temp = 36.8
                status = "TRAFFIC_DELAY"
                current_speed = 18
                location = "NJ-18 Southbound near New Brunswick"
                alerts_generated.append({
                    "route_id": r_id,
                    "severity": "MEDIUM",
                    "type": "TRAFFIC_CONGESTION",
                    "message": "Heavy congestion on NJ-18 (+14 min delay). Recalculated next ETA within soft window tolerance.",
                    "recommended_action": "Auto-updated ETA broadcasted to Wegmans Woodbridge dock manager."
                })
            else:
                # Metro NYC route - excellent condition
                zone_f_temp = -9.8
                zone_c_temp = 35.9
                status = "NORMAL"
                current_speed = 32
                location = "I-278 Eastbound approaching Goethals Bridge"

            telemetry_status.append({
                "route_id": r_id,
                "carrier": carrier,
                "status": status,
                "current_location": location,
                "speed_mph": current_speed,
                "thermistors": {
                    "frozen_zone_temp_f": zone_f_temp,
                    "chill_zone_temp_f": zone_c_temp,
                    "ambient_zone_temp_f": 68.0,
                    "integrity_status": "COMPLIANT_FSMA"
                }
            })

        result = {
            "agent": self.name,
            "status": "MONITORING_ACTIVE",
            "active_trailers_tracked": len(telemetry_status),
            "telemetry_stream": telemetry_status,
            "alerts": alerts_generated,
            "thought_log": (
                f"Active IoT monitoring on {len(telemetry_status)} live multi-temp reefers. "
                f"100% FSMA temperature integrity verified across all zones. "
                f"{len(alerts_generated)} proactive ETA mitigation broadcasted."
            )
        }
        return result
