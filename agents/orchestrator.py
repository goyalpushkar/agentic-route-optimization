import json
import os
import time
from typing import Dict, Any, List

from .demand_profiler import DemandProfilerAgent
from .fleet_allocator import FleetAllocatorAgent
from .route_optimizer import RouteOptimizerAgent
from .carrier_aggregator import CarrierAggregatorAgent
from .carrier_decision import CarrierDecisionAgent
from .telematics_monitor import TelematicsMonitorAgent

class AgentOrchestrator:
    """
    Multi-Agent Orchestrator & State Machine
    Coordinates execution sequence across Agents 1 to 6 with Human-in-the-Loop governance.
    """

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Fallback to relative data path
            data_dir = "data"
            if not os.path.exists(data_dir):
                data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir

        self.agent1_profiler = DemandProfilerAgent()
        self.agent2_fleet = FleetAllocatorAgent()
        self.agent3_router = RouteOptimizerAgent()
        self.agent4_aggregator = CarrierAggregatorAgent()
        self.agent5_decision = CarrierDecisionAgent()
        self.agent6_monitor = TelematicsMonitorAgent()

    def load_json(self, filename: str) -> Dict[str, Any]:
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, "r") as f:
            return json.load(f)

    def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Executes the full end-to-end multi-agent lifecycle.
        """
        execution_start = time.time()
        pipeline_log = []

        # 1. Load Data
        orders_data = self.load_json("orders.json")
        fleet_data = self.load_json("fleet.json")
        carriers_data = self.load_json("carriers.json")

        # Step 1: Agent 1 - Demand Profiling
        step1_out = self.agent1_profiler.process(orders_data)
        pipeline_log.append({
            "step": 1,
            "agent": self.agent1_profiler.name,
            "summary": step1_out["thought_log"],
            "data": step1_out["metrics"]
        })

        # Step 2: Agent 2 - Fleet & Dock Allocation
        step2_out = self.agent2_fleet.process(fleet_data, step1_out)
        pipeline_log.append({
            "step": 2,
            "agent": self.agent2_fleet.name,
            "summary": step2_out["thought_log"],
            "data": step2_out["metrics"]
        })

        # Step 3: Agent 3 - Cold-Chain Route Optimization
        step3_out = self.agent3_router.process(step1_out, step2_out)
        pipeline_log.append({
            "step": 3,
            "agent": self.agent3_router.name,
            "summary": step3_out["thought_log"],
            "data": step3_out["summary_metrics"]
        })

        # Step 4: Agent 4 - Live Carrier Quoting
        step4_out = self.agent4_aggregator.process(step3_out, carriers_data)
        pipeline_log.append({
            "step": 4,
            "agent": self.agent4_aggregator.name,
            "summary": step4_out["thought_log"],
            "data": step4_out["metrics"]
        })

        # Step 5: Agent 5 - Carrier Scoring & Booking Decision (40/30/20/10)
        step5_out = self.agent5_decision.process(step4_out)
        pipeline_log.append({
            "step": 5,
            "agent": self.agent5_decision.name,
            "summary": step5_out["thought_log"],
            "data": step5_out["summary_metrics"]
        })

        # Step 6: Agent 6 - Telematics & Dynamic IoT Monitoring
        step6_out = self.agent6_monitor.process(step5_out)
        pipeline_log.append({
            "step": 6,
            "agent": self.agent6_monitor.name,
            "summary": step6_out["thought_log"],
            "data": {"active_monitored": step6_out["active_trailers_tracked"], "alerts": len(step6_out["alerts"])}
        })

        total_duration = round(time.time() - execution_start, 3)

        return {
            "status": "SUCCESS",
            "execution_duration_sec": total_duration,
            "pipeline_log": pipeline_log,
            "results": {
                "step1_demand_profiling": step1_out,
                "step2_fleet_allocation": step2_out,
                "step3_route_optimization": step3_out,
                "step4_carrier_quoting": step4_out,
                "step5_carrier_booking": step5_out,
                "step6_telematics_monitoring": step6_out
            }
        }
