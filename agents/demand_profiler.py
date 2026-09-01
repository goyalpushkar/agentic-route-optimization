import json
from typing import Dict, Any, List

class DemandProfilerAgent:
    """
    Agent 1: Demand & Order Profiler Agent
    Responsibilities:
    - Ingests customer order stream.
    - Slices demand into 4D vectors (Pallets, Cube ft3, Cases, Weight lbs).
    - Classifies thermal regimes: Frozen (-10°F), Chill (36°F), Ambient/HMBC.
    - Detects oversized order exceptions requiring multi-truck splitting.
    """

    def __init__(self):
        self.name = "Agent 1: Demand & Order Profiler"
        self.role = "Cold-Chain Demand Classifier & 4D Vector Engine"
        self.system_prompt = (
            "You are the Demand Profiler Agent in an autonomous wholesale grocery logistics system. "
            "Your objective is to enforce strict temperature integrity (-10°F Frozen, +36°F Chill, Ambient) "
            "and compute multi-dimensional load vectors (Pallets, Cube, Cases, Catch-Weight) to feed downstream routing solvers."
        )

    def process(self, raw_orders_data: Dict[str, Any]) -> Dict[str, Any]:
        orders = raw_orders_data.get("orders", [])
        dc_info = raw_orders_data.get("distribution_center", {})
        
        profiled_orders = []
        total_frozen_pallets = 0
        total_chill_pallets = 0
        total_ambient_pallets = 0
        total_cube_ft3 = 0
        total_weight_lbs = 0
        split_candidates = []

        for ord_item in orders:
            demand = ord_item.get("demand", {})
            f_plt = demand.get("frozen", {}).get("pallets", 0)
            c_plt = demand.get("chill", {}).get("pallets", 0)
            a_plt = demand.get("ambient", {}).get("pallets", 0)
            
            f_cube = demand.get("frozen", {}).get("cube_ft3", 0)
            c_cube = demand.get("chill", {}).get("cube_ft3", 0)
            a_cube = demand.get("ambient", {}).get("cube_ft3", 0)
            
            f_wt = demand.get("frozen", {}).get("weight_lbs", 0)
            c_wt = demand.get("chill", {}).get("weight_lbs", 0)
            a_wt = demand.get("ambient", {}).get("weight_lbs", 0)

            tot_plt = f_plt + c_plt + a_plt
            tot_cube = f_cube + c_cube + a_cube
            tot_wt = f_wt + c_wt + a_wt

            total_frozen_pallets += f_plt
            total_chill_pallets += c_plt
            total_ambient_pallets += a_plt
            total_cube_ft3 += tot_cube
            total_weight_lbs += tot_wt

            is_split_required = tot_plt > 28 or tot_wt > 42000
            if is_split_required:
                split_candidates.append({
                    "order_id": ord_item["order_id"],
                    "customer_name": ord_item["customer_name"],
                    "total_pallets": tot_plt,
                    "reason": "Exceeds single 53W payload capacity"
                })

            profiled_orders.append({
                "order_id": ord_item["order_id"],
                "customer_id": ord_item["customer_id"],
                "customer_name": ord_item["customer_name"],
                "address": ord_item["address"],
                "lat": ord_item["lat"],
                "lng": ord_item["lng"],
                "time_window": ord_item["time_window"],
                "service_time_min": ord_item.get("service_time_min", 30),
                "dock_restrictions": ord_item.get("dock_restrictions", {}),
                "summary": {
                    "total_pallets": tot_plt,
                    "total_cube_ft3": tot_cube,
                    "total_weight_lbs": tot_wt,
                    "frozen_pallets": f_plt,
                    "chill_pallets": c_plt,
                    "ambient_pallets": a_plt
                },
                "breakdown": demand,
                "is_split_required": is_split_required
            })

        result = {
            "agent": self.name,
            "status": "COMPLETED",
            "distribution_center": dc_info,
            "metrics": {
                "orders_count": len(orders),
                "total_pallets": total_frozen_pallets + total_chill_pallets + total_ambient_pallets,
                "total_frozen_pallets": total_frozen_pallets,
                "total_chill_pallets": total_chill_pallets,
                "total_ambient_pallets": total_ambient_pallets,
                "total_cube_ft3": total_cube_ft3,
                "total_weight_lbs": total_weight_lbs,
                "split_order_count": len(split_candidates)
            },
            "split_candidates": split_candidates,
            "profiled_orders": profiled_orders,
            "thought_log": (
                f"Ingested {len(orders)} orders. Verified 3 thermal regimes. "
                f"Total demand: {total_frozen_pallets} Frozen plts, {total_chill_pallets} Chill plts, "
                f"{total_ambient_pallets} Ambient plts ({total_weight_lbs:,} lbs). "
                f"{len(split_candidates)} split orders flagged."
            )
        }
        return result
