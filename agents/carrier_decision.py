from typing import Dict, Any, List

class CarrierDecisionAgent:
    """
    Agent 5: Carrier Scoring & Booking Decision Agent
    Responsibilities:
    - Implements the 40/30/20/10 Multi-Criteria Decision Analysis (MCDA).
    - Ranks all candidate carriers with transparent scoring weights.
    - Generates EDI 204 Load Tender payload and locks booking.
    - Emits WMS Wave Release trigger to begin warehouse order picking.
    """

    def __init__(self):
        self.name = "Agent 5: Carrier Decision & Booking"
        self.role = "40/30/20/10 Carrier MCDA & WMS Wave Release Engine"
        self.system_prompt = (
            "You are the Carrier Decision & Booking Agent. You evaluate live carrier bids using the 40/30/20/10 scoring matrix: "
            "40% Freight Rate Competitiveness, 30% Historical On-Time Reliability, 20% FSMA/Cold-Chain SLA Fit, and 10% Preferred Partner Status. "
            "You select the top carrier, lock the EDI 204 tender, and trigger the warehouse WMS wave release."
        )

    def process(self, carrier_quotes: Dict[str, Any]) -> Dict[str, Any]:
        bids_by_route = carrier_quotes.get("bids_by_route", {})
        
        awarded_bookings = []
        overall_spend = 0.0

        for r_id, bids in bids_by_route.items():
            if not bids:
                continue

            min_quote = min(b["quote_breakdown"]["total_quote"] for b in bids)
            scored_bids = []

            for b in bids:
                q_total = b["quote_breakdown"]["total_quote"]
                
                # 1. Rate Score (Max 40 points) - Relative to lowest quote
                rate_score = round(40.0 * (min_quote / q_total), 1)

                # 2. Reliability Score (Max 30 points) - Based on historical %
                rel_pct = b.get("historical_on_time_pickup_pct", 90.0)
                rel_score = round(30.0 * (rel_pct / 100.0), 1)

                # 3. SLA & FSMA Fit Score (Max 20 points)
                sla_score = 0.0
                if b.get("fsma_certified", False):
                    sla_score += 10.0
                if b.get("reefer_telematics_connected", False):
                    sla_score += 10.0

                # 4. Preferred Status Score (Max 10 points)
                pref_score = float(b.get("preferred_score", 0))

                total_score = round(rate_score + rel_score + sla_score + pref_score, 1)

                scored_bids.append({
                    "carrier_id": b["carrier_id"],
                    "carrier_name": b["carrier_name"],
                    "tier": b["tier"],
                    "total_quote": q_total,
                    "effective_cpm": b["quote_breakdown"]["effective_cpm"],
                    "scores": {
                        "rate_score": rate_score,
                        "reliability_score": rel_score,
                        "sla_fit_score": sla_score,
                        "preferred_score": pref_score,
                        "composite_score": total_score
                    }
                })

            # Sort by total score descending
            scored_bids.sort(key=lambda x: x["scores"]["composite_score"], reverse=True)
            winner = scored_bids[0]
            overall_spend += winner["total_quote"]

            awarded_bookings.append({
                "route_id": r_id,
                "awarded_carrier": winner["carrier_name"],
                "carrier_id": winner["carrier_id"],
                "winning_score": winner["scores"]["composite_score"],
                "booked_rate": winner["total_quote"],
                "effective_cpm": winner["effective_cpm"],
                "score_breakdown": winner["scores"],
                "ranked_candidates": scored_bids,
                "edi_204_tender": {
                    "transaction_id": f"EDI204-{r_id}-20260901",
                    "status": "TENDERED_ACCEPTED",
                    "pickup_window": "05:00 - 05:30",
                    "equipment_type": "Multi-Temp Reefer",
                    "temperature_spec": "Frozen: -10F | Chill: +36F | Ambient: 68F"
                },
                "wms_wave_release": {
                    "wave_id": f"WAVE-{r_id}-PICK01",
                    "status": "RELEASED_TO_FLOOR",
                    "picking_staging_dock": "DOCK-BAY-04",
                    "synchronized": True
                },
                "decision_rationale": (
                    f"Selected {winner['carrier_name']} with composite score {winner['scores']['composite_score']}/100. "
                    f"Offered superior 3-mo reliability ({winner['scores']['reliability_score']}/30) and full FSMA telematics "
                    f"at ${winner['total_quote']:,} ({winner['effective_cpm']}/mi)."
                )
            })

        result = {
            "agent": self.name,
            "status": "COMPLETED",
            "decision_engine": "40/30/20/10 Multi-Criteria Scoring (Rate/Reliability/SLA/Preferred)",
            "summary_metrics": {
                "routes_booked": len(awarded_bookings),
                "total_freight_spend": round(overall_spend, 2),
                "avg_carrier_score": round(sum(b["winning_score"] for b in awarded_bookings) / len(awarded_bookings), 1) if awarded_bookings else 0.0,
                "wms_waves_synchronized": len(awarded_bookings)
            },
            "awarded_bookings": awarded_bookings,
            "thought_log": (
                f"Evaluated and scored carrier bids for {len(awarded_bookings)} routes. "
                f"Locked EDI 204 tenders for total freight cost ${overall_spend:,.2f}. "
                f"Synchronized and released {len(awarded_bookings)} WMS warehouse picking waves."
            )
        }
        return result
