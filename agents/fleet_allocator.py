import json
from typing import Dict, Any, List

class FleetAllocatorAgent:
    """
    Agent 2: Fleet & Dock Allocator Agent
    Responsibilities:
    - Analyzes available private and dedicated multi-temp reefer inventory.
    - Matches trailer capabilities (46W, 48W, 53W) with store dock constraints.
    - Reserves eligible equipment pool for routing solver.
    """

    def __init__(self):
        self.name = "Agent 2: Fleet & Dock Allocator"
        self.role = "Reefer Fleet Capacity & Physical Dock Compatibility Engine"
        self.system_prompt = (
            "You are the Fleet & Dock Allocator Agent. Your responsibility is to analyze available trailer equipment "
            "(46W City Reefers, 48W Reefers, 53W Multi-Temp Trailers), verify store dock restrictions (tight turning radii, "
            "length caps, liftgates), and allocate eligible capacity to fulfill wholesale demand."
        )

    def process(self, fleet_data: Dict[str, Any], profiled_demand: Dict[str, Any]) -> Dict[str, Any]:
        trailers = fleet_data.get("fleet_inventory", [])
        profiled_orders = profiled_demand.get("profiled_orders", [])

        # Check dock restrictions across orders
        dock_constraints_summary = {
            "require_liftgate": 0,
            "max_46w_only": 0,
            "max_48w_only": 0,
            "can_accept_53w": 0
        }

        for ord_item in profiled_orders:
            restr = ord_item.get("dock_restrictions", {})
            max_len = restr.get("max_trailer_len", "53W")
            liftgate = restr.get("liftgate_required", False)

            if liftgate:
                dock_constraints_summary["require_liftgate"] += 1
            if max_len == "46W":
                dock_constraints_summary["max_46w_only"] += 1
            elif max_len == "48W":
                dock_constraints_summary["max_48w_only"] += 1
            else:
                dock_constraints_summary["can_accept_53w"] += 1

        allocated_trailers = []
        total_fleet_pallets = 0
        total_fleet_payload_lbs = 0

        for t in trailers:
            if t.get("status") == "AVAILABLE":
                allocated_trailers.append(t)
                total_fleet_pallets += t.get("max_pallets", 0)
                total_fleet_payload_lbs += t.get("max_payload_lbs", 0)

        result = {
            "agent": self.name,
            "status": "COMPLETED",
            "dock_constraints_summary": dock_constraints_summary,
            "allocated_fleet": allocated_trailers,
            "metrics": {
                "available_trailers_count": len(allocated_trailers),
                "total_fleet_pallet_capacity": total_fleet_pallets,
                "total_fleet_payload_capacity_lbs": total_fleet_payload_lbs
            },
            "thought_log": (
                f"Audited {len(trailers)} fleet assets. Allocated {len(allocated_trailers)} active reefers "
                f"({total_fleet_pallets} total pallet capacity). Found {dock_constraints_summary['max_46w_only']} "
                f"stops requiring 46W city-reefers and {dock_constraints_summary['require_liftgate']} requiring liftgates."
            )
        }
        return result
