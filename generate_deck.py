import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    COLOR_PRIMARY_DARK = RGBColor(15, 23, 42)     # #0F172A
    COLOR_SECONDARY_DARK = RGBColor(30, 41, 59)   # #1E293B
    COLOR_CYAN = RGBColor(6, 182, 212)            # #06B6D4
    COLOR_EMERALD = RGBColor(16, 185, 129)        # #10B981
    COLOR_AMBER = RGBColor(245, 158, 11)          # #F59E0B
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_TEXT_PRIMARY = RGBColor(15, 23, 42)
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)
    COLOR_CARD_BG = RGBColor(255, 255, 255)

    blank_slide_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text=""):
        if category_text:
            cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
            tf_cat = cat_box.text_frame
            tf_cat.word_wrap = True
            tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
            p_cat = tf_cat.paragraphs[0]
            p_cat.text = category_text.upper()
            p_cat.font.size = Pt(10)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_DARK

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # SLIDE 1: TITLE
    s1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg1.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p_sub = tf1.paragraphs[0]
    p_sub.text = "AI-POWERED WHOLESALE GROCERY LOGISTICS & ROUTE OPTIMIZATION"
    p_sub.font.size = Pt(13); p_sub.font.bold = True; p_sub.font.color.rgb = COLOR_CYAN; p_sub.space_after = Pt(14)

    p_title = tf1.add_paragraph()
    p_title.text = "Autonomous Multi-Temperature Routing &\nLive Dynamic Carrier Booking Engine"
    p_title.font.size = Pt(32); p_title.font.bold = True; p_title.font.color.rgb = COLOR_WHITE; p_title.space_after = Pt(20)

    p_desc = tf1.add_paragraph()
    p_desc.text = "An end-to-end multi-agent platform on Google Cloud optimizing trailer cube utilization (46W-53W),\nflexible multi-temp bulkheads, soft ±1hr time windows, and parallel automated carrier procurement."
    p_desc.font.size = Pt(14); p_desc.font.color.rgb = RGBColor(148, 163, 184); p_desc.space_after = Pt(36)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Executive Pitch & Architectural Approval Proposal | Evaluation & Funding Request"
    p_meta.font.size = Pt(11); p_meta.font.bold = True; p_meta.font.color.rgb = COLOR_AMBER

    # SLIDE 2: PROBLEM & BUSINESS VALUE
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_header(s2, "Executive Summary: Transforming Grocery Delivery Economics", "1. Industry Relevance & Challenge")
    col_w = Inches(3.64); top_pos = Inches(1.5); card_h = Inches(5.3)

    add_card(s2, Inches(0.8), top_pos, col_w, card_h)
    tb = s2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Grocery Logistics Friction"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(10)
    items1 = [
        ("Multi-Temp Silos", "Frozen, Chill, Ambient, and HMBC orders often dispatched on separate dedicated trucks, causing redundant miles."),
        ("Sub-Optimal Cube Fill", "Manual route planning averages only 74-78% trailer cube utilization across 46W, 48W, and 53W fleets."),
        ("Time Window Penalties", "Strict retail delivery schedules lead to expensive late-dock correction penalties when windows are missed."),
        ("Wave Lockouts", "Goods picked in WMS before carrier capacity is locked, clogging staging docks and risking perishables.")
    ]
    for h, d in items1:
        p1 = tf.add_paragraph(); p1.text = f"• {h}: "; p1.font.bold = True; p1.font.size = Pt(11); p1.font.color.rgb = COLOR_PRIMARY_DARK
        p1.add_run().text = d; p1.runs[1].font.bold = False; p1.runs[1].font.size = Pt(11); p1.runs[1].font.color.rgb = COLOR_TEXT_MUTED
        p1.space_after = Pt(6)

    add_card(s2, Inches(4.84), top_pos, col_w, card_h)
    tb = s2.shapes.add_textbox(Inches(5.04), top_pos + Inches(0.2), col_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Autonomous AI Solution"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(10)
    items2 = [
        ("Flexible Bulkhead Packing", "Solves Multi-Compartment VRP with dynamically positioned bulkheads (2-pallet increments) per route."),
        ("Soft-Window Tolerance", "Optimizes routes with ±1 hr window flexibility and 30-min standard dock service dwell times."),
        ("Parallel Rate Discovery", "Sub-3s broadcast to freight exchanges & contracted carriers to secure the cheapest compliant reefer."),
        ("WMS Wave Sync", "Locks carrier booking and pickup capacity BEFORE warehouse picking waves are released.")
    ]
    for h, d in items2:
        p1 = tf.add_paragraph(); p1.text = f"• {h}: "; p1.font.bold = True; p1.font.size = Pt(11); p1.font.color.rgb = COLOR_PRIMARY_DARK
        p1.add_run().text = d; p1.runs[1].font.bold = False; p1.runs[1].font.size = Pt(11); p1.runs[1].font.color.rgb = COLOR_TEXT_MUTED
        p1.space_after = Pt(6)

    add_card(s2, Inches(8.88), top_pos, col_w, card_h, bg_color=RGBColor(240, 253, 250), border_color=COLOR_EMERALD)
    tb = s2.shapes.add_textbox(Inches(9.08), top_pos + Inches(0.2), col_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Targeted Business Value"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD; p.space_after = Pt(10)
    roi_metrics = [
        ("92%+", "Trailer Cube Utilization", "Up from ~76% baseline via intelligent multi-temp consolidation."),
        ("14-18%", "Fleet Mileage & Fuel Reduction", "Optimized stop sequencing and single-drop consolidation."),
        ("98.5%", "OTIF Delivery Compliance", "Eliminates dock penalty fees through soft-window mathematical optimization."),
        ("$1.8M+", "Projected Net Annual Savings", "Across fleet operations, fuel, spot freight procurement, and reduced perishable write-offs.")
    ]
    for val, label, sub in roi_metrics:
        p1 = tf.add_paragraph(); p1.text = val; p1.font.bold = True; p1.font.size = Pt(20); p1.font.color.rgb = COLOR_EMERALD
        p2 = tf.add_paragraph(); p2.text = label; p2.font.bold = True; p2.font.size = Pt(11); p2.font.color.rgb = COLOR_PRIMARY_DARK
        p3 = tf.add_paragraph(); p3.text = sub; p3.font.size = Pt(10); p3.font.color.rgb = COLOR_TEXT_MUTED; p3.space_after = Pt(6)

    # SLIDE 3: GROCERY COLD-CHAIN & FLEET REALITIES
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_header(s3, "Grocery Domain Depth: Heterogeneous Fleets & Cold-Chain", "1. Industry Relevance & Logistics Complexity")
    card_w4 = Inches(2.7); gap4 = Inches(0.3)
    fleet_specs = [
        ("Multi-Temp Reefers", "Flexible Bulkheads", "46W, 48W, 52W, 53W", "Insulated movable bulkheads adjusted in 2-pallet increments. Allows Frozen (-10°F), Chill (36°F), and Dry Grocery in one single drop."),
        ("Dedicated Reefers", "Single-Temp Fleet", "100% Frozen / 100% Dry", "Used for dedicated large store replenishments. Integrated with multi-temp solver to avoid splitting unless volume exceeds trailer capacity."),
        ("Customer Dock Rules", "Physical Constraints", "Length & Liftgate Limits", "Downtown retail locations restricted to 46W/48W; elevated docks vs liftgate/electric pallet jack requirements mapped to vehicle dispatch."),
        ("4D Order Dimensions", "Volume & Catch-Weight", "Cube, Pallet, Case, Lbs", "Handles full SKU physical profiles including gross catch-weight for meats/produce to ensure legal axle weight compliance.")
    ]
    for idx, (title, tag, sub, desc) in enumerate(fleet_specs):
        x = Inches(0.8) + idx * (card_w4 + gap4)
        add_card(s3, x, Inches(1.5), card_w4, Inches(5.3))
        tb = s3.shapes.add_textbox(x + Inches(0.15), Inches(1.7), card_w4 - Inches(0.3), Inches(4.9))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = tag.upper(); p.font.size = Pt(9); p.font.bold = True; p.font.color.rgb = COLOR_CYAN; p.space_after = Pt(4)
        p1 = tf.add_paragraph(); p1.text = title; p1.font.size = Pt(15); p1.font.bold = True; p1.font.color.rgb = COLOR_PRIMARY_DARK; p1.space_after = Pt(4)
        p2 = tf.add_paragraph(); p2.text = sub; p2.font.size = Pt(11); p2.font.bold = True; p2.font.color.rgb = COLOR_AMBER; p2.space_after = Pt(12)
        p3 = tf.add_paragraph(); p3.text = desc; p3.font.size = Pt(11); p3.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 4: 6-AGENT ECOSYSTEM
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_header(s4, "6-Agent Autonomous Architecture: From Sourcing to Booking", "3. AI Tools & Agentic Framework")
    agents = [
        ("Agent 1: DC Sourcing & Demand Profiler", "Normalizes 4D demand vectors (Pallets, Cube, Cases, Catch-Weight) across Frozen, Chill, Ambient, HMBC. Selects optimal origin DC.", "Vertex AI + BigQuery"),
        ("Agent 2: Cold-Chain Fleet Allocator", "Validates trailer sizes (46W, 48W, 53W), bulkhead increments, driver HOS limits, and customer dock constraints.", "Fleet Master DB"),
        ("Agent 3: Cold-Chain Route Optimizer", "Formulates Multi-Compartment VRP with Soft Time Windows (±1hr). Enforces priority: OTIF > Overtime > Miles > Fleet count.", "Cloud Optimization API / OR-Tools"),
        ("Agent 4: Live Carrier Rate Aggregator", "Broadcasts parallel asynchronous RFQs across carrier APIs and EDI 204 freight exchanges in <3 seconds.", "Cloud Pub/Sub + Cloud Functions"),
        ("Agent 5: Carrier Scoring & Booking Agent", "Evaluates live bids using 40/30/20/10 multi-criteria matrix; locks booking confirmation BEFORE WMS wave picking starts.", "BigQuery Scorecard + EDI Gateway"),
        ("Agent 6: Dynamic Cold-Chain Monitor", "Continuously tracks in-transit IoT reefer temperatures and GPS dwell times against 30-min baseline to trigger recovery.", "IoT Telematics + Google Maps API")
    ]
    for idx, (aname, adesc, atech) in enumerate(agents):
        row = idx // 3; col = idx % 3
        x = Inches(0.8) + col * Inches(3.95); y = Inches(1.5) + row * Inches(2.7)
        add_card(s4, x, y, Inches(3.75), Inches(2.5))
        tb = s4.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), Inches(3.45), Inches(2.2))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = aname; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(6)
        p1 = tf.add_paragraph(); p1.text = adesc; p1.font.size = Pt(10.5); p1.font.color.rgb = COLOR_TEXT_MUTED; p1.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = f"Tech: {atech}"; p2.font.size = Pt(9.5); p2.font.bold = True; p2.font.color.rgb = COLOR_CYAN

    # SLIDE 5: MATHEMATICAL OPTIMIZATION
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_header(s5, "Mathematical Optimization: Multi-Compartment VRP with Time Windows", "2. Development Methodology & Core Algorithms")
    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Hierarchical Objective Formulation"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(10)
    p1 = tf.add_paragraph()
    p1.text = "Min Z = w1·Cost(OTIF) + w2·Cost(Overtime) + w3·Cost(Miles) + w4·Cost(Fleet)"
    p1.font.size = Pt(11); p1.font.bold = True; p1.font.color.rgb = COLOR_CYAN; p1.space_after = Pt(12)
    math_details = [
        ("Strict Priority Hierarchy", "w1 >> w2 >> w3 >> w4 (OTIF compliance is prioritized first, then driver overtime prevention, then fuel/mileage, then asset activation)."),
        ("Flexible Bulkhead Partitioning", "For each multi-temp trailer: ∑ Pallets(Frozen + Chill + Dry) ≤ Capacity, with bulkheads dynamically constrained to 2-pallet increments."),
        ("Soft Time Windows (±1 hr)", "Delivery windows [Ei, Li] penalized with graduated linear slopes outside the 1-hour buffer; standard 30 min service time per stop."),
        ("LIFO Unloading Constraint", "Enforces reverse-stop loading order so pallets for later stops never block early-stop unloading access.")
    ]
    for h, d in math_details:
        p_m = tf.add_paragraph(); p_m.text = f"• {h}: "; p_m.font.bold = True; p_m.font.size = Pt(10.5); p_m.font.color.rgb = COLOR_PRIMARY_DARK
        p_m.add_run().text = d; p_m.runs[1].font.bold = False; p_m.runs[1].font.size = Pt(10.5); p_m.runs[1].font.color.rgb = COLOR_TEXT_MUTED
        p_m.space_after = Pt(6)

    add_card(s5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb_r = s5.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "Dual Operational Engine Modes"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(10)
    modes = [
        ("Mode A: Operational Daily Dispatch Optimizer", "Runs nightly on firm customer orders. Generates exact turn-by-turn routes, bulkhead divider positions, driver manifests, and triggers live carrier tenders."),
        ("Mode B: Tactical 2-Month Capacity Simulator", "Runs Monte Carlo simulations over 2-month probabilistic demand forecasts to predict weekly trailer requirements (46W vs 53W) and identify peak bottlenecks weeks in advance."),
        ("Historical 3-Month Backtesting Engine", "Re-runs historical actual order streams to compare AI routes against human manual dispatch, benchmarking miles saved, fuel reductions, and cube utilization gains.")
    ]
    for h, d in modes:
        p_m = tf_r.add_paragraph(); p_m.text = f"• {h}: "; p_m.font.bold = True; p_m.font.size = Pt(11); p_m.font.color.rgb = COLOR_PRIMARY_DARK
        p_m.add_run().text = d; p_m.runs[1].font.bold = False; p_m.runs[1].font.size = Pt(10.5); p_m.runs[1].font.color.rgb = COLOR_TEXT_MUTED
        p_m.space_after = Pt(8)

    # SLIDE 6: CARRIER SCORING (40/30/20/10)
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_header(s6, "Automated Carrier Sourcing & Multi-Criteria Decision Scoring", "2. Methodology & Business Value")
    w_sc = Inches(2.7); g_sc = Inches(0.3)
    score_cards = [
        ("40%", "Live Freight Rate", "Cost Competitiveness", "Scores live spot and contracted rates in parallel against current lane benchmarks. Prevents overpaying on stale contracted rate cards."),
        ("30%", "Historical Reliability", "On-Time Pickup & Acceptance", "Calculated from BigQuery trailing 3-month carrier performance: 60% On-Time Pickup Rate + 40% Tender Acceptance Rate."),
        ("20%", "Cold-Chain SLA Fit", "Reefer & Equipment Spec", "Evaluates FSMA certification, continuous IoT temperature logging capabilities, pre-cooling compliance, and reefer unit age (<5 yrs)."),
        ("10%", "Preferred Status", "Strategic Partnership", "Prioritizes dedicated strategic fleet partners (Tier-1 = 100pts, Tier-2 = 60pts, Spot Broker = 0pts) to maintain carrier relationships.")
    ]
    for idx, (pct, title, sub, desc) in enumerate(score_cards):
        x = Inches(0.8) + idx * (w_sc + g_sc)
        add_card(s6, x, Inches(1.5), w_sc, Inches(3.2))
        tb = s6.shapes.add_textbox(x + Inches(0.15), Inches(1.65), w_sc - Inches(0.3), Inches(2.9))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = pct; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = COLOR_CYAN; p.space_after = Pt(2)
        p1 = tf.add_paragraph(); p1.text = title; p1.font.size = Pt(13); p1.font.bold = True; p1.font.color.rgb = COLOR_PRIMARY_DARK; p1.space_after = Pt(2)
        p2 = tf.add_paragraph(); p2.text = sub; p2.font.size = Pt(10); p2.font.bold = True; p2.font.color.rgb = COLOR_AMBER; p2.space_after = Pt(6)
        p3 = tf.add_paragraph(); p3.text = desc; p3.font.size = Pt(10); p3.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s6, Inches(0.8), Inches(4.9), Inches(11.7), Inches(1.9), bg_color=RGBColor(241, 245, 249), border_color=COLOR_CYAN)
    tb_b = s6.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(11.3), Inches(1.7))
    tf_b = tb_b.text_frame; tf_b.word_wrap = True
    p = tf_b.paragraphs[0]; p.text = "Capacity Lockout Prevention: Synchronized WMS Wave Release"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(4)
    p1 = tf_b.add_paragraph()
    p1.text = "The system enforces a strict time-locked gateway: Carrier booking is confirmed via EDI 990 / API FIRST. Only when carrier capacity is 100% locked does the system signal the WMS to release picking waves. This completely eliminates warehouse staging congestion, wasted picker labor, and perishable spoilage caused by dropped carrier tenders."
    p1.font.size = Pt(11); p1.font.color.rgb = COLOR_TEXT_PRIMARY

    # SLIDE 7: HITL DISPATCHER COCKPIT
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_header(s7, "Human-in-the-Loop (HITL) Dispatcher Cockpit & Visual Controls", "4. Presentation & Interactive UX")
    hitl_views = [
        ("Interactive Map & Stop Drag-and-Drop", "Interactive Google Maps view color-coded by trailer type (46W/48W/53W) with temp icons.\n• Dispatchers drag & drop stops between routes.\n• In-memory Redis cache recalculates arrival ETAs, time windows, and cost deltas in <300ms.", "Mapbox / Deck.gl + Redis"),
        ("2D/3D Trailer Bulkhead Visualizer", "Top-down cross section of 22 to 30 pallet floor positions.\n• Interactive bulkhead slider shifts temperature zones in 2-pallet increments.\n• Real-time LIFO check warns if early-stop pallets are trapped behind late-stop loads.", "React + Tailwind Canvas"),
        ("Two-Stage Approval Gates", "Gate 1: Route Review & Manual Edit (One-click route approval unlocks carrier RFQ).\nGate 2: Carrier Tender Review (Dispatcher confirms top 40/30/20/10 AI carrier or overrides before WMS release).", "FastAPI + WebSockets")
    ]
    for idx, (title, desc, stack) in enumerate(hitl_views):
        x = Inches(0.8) + idx * (col_w + Inches(0.39))
        add_card(s7, x, Inches(1.5), col_w, Inches(5.3))
        tb = s7.shapes.add_textbox(x + Inches(0.15), Inches(1.7), col_w - Inches(0.3), Inches(4.9))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(10)
        p1 = tf.add_paragraph(); p1.text = desc; p1.font.size = Pt(10.5); p1.font.color.rgb = COLOR_TEXT_MUTED; p1.space_after = Pt(14)
        p2 = tf.add_paragraph(); p2.text = f"Stack: {stack}"; p2.font.size = Pt(10); p2.font.bold = True; p2.font.color.rgb = COLOR_CYAN

    # SLIDE 8: GCP ARCHITECTURE TABLE
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_header(s8, "GCP Cloud-Native Architecture: Scalable, Secure & Serverless", "3. AI Tools & Technical Architecture")
    table_shape = s8.shapes.add_table(7, 3, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    table = table_shape.table
    table.columns[0].width = Inches(2.5); table.columns[1].width = Inches(3.2); table.columns[2].width = Inches(6.0)
    headers = ["GCP Component", "Architectural Role", "Logistics Capability & Purpose"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid(); cell.fill.fore_color.rgb = COLOR_PRIMARY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = COLOR_WHITE
    gcp_rows = [
        ("Vertex AI (Gemini 2.5)", "Agent Reasoning & NL Briefings", "Powers Agent decision explanations, exception handling, and dispatcher copilot dialogues."),
        ("Cloud Optimization API / OR-Tools", "Mathematical Solver Engine", "High-performance solver computing Multi-Compartment VRP with flexible bulkheads & soft windows."),
        ("BigQuery Lakehouse", "Historical & Forecast Data Store", "Stores 3mo historical actuals, 2mo probabilistic demand models, and carrier scorecards (OTP/OTD)."),
        ("Cloud Run & LangGraph", "Microservices & Agent Runtime", "Hosts the scalable agent state machine, FastAPI backend, and Next.js dispatcher UI."),
        ("Cloud Pub/Sub & Cloud Functions", "Parallel Rate Procurement", "Broadcasts parallel quote requests to dozens of carrier APIs asynchronously in <3 seconds."),
        ("Cloud Firestore & Redis", "Low-Latency Live State", "Sub-second state machine for live drag-and-drop route recalculations and collaborative editing.")
    ]
    for row_idx, data in enumerate(gcp_rows, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if row_idx % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = text; p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK
            elif col_idx == 1:
                p.font.bold = True; p.font.color.rgb = COLOR_CYAN
            else:
                p.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 9: DEVELOPMENT METHODOLOGY
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_header(s9, "Engineering Methodology: Agile TDD & Rigorous Validation", "2. Development Methodology")
    meth_cards = [
        ("Phase 1: Foundation & Solver", "Weeks 1 - 4", "• BigQuery historical & forecast schemas.\n• C++/Python OR-Tools MC-VRPTW solver with 2-pallet bulkhead logic.\n• Automated unit & integration tests on synthetic grocery orders."),
        ("Phase 2: Agent Ecosystem", "Weeks 5 - 8", "• LangGraph 6-agent orchestrator on Cloud Run.\n• Pub/Sub parallel carrier rate aggregator.\n• 40/30/20/10 carrier scoring engine integration with EDI 204 gateways."),
        ("Phase 3: Dispatcher UI & HITL", "Weeks 9 - 12", "• Next.js interactive route map with drag-and-drop stop editing.\n• 2D/3D trailer bulkhead visualizer with LIFO unloading validation.\n• Two-stage approval state machine."),
        ("Phase 4: Pilot & Backtesting", "Weeks 13 - 16", "• Backtesting on past 3 months of actual order runs.\n• Shadow runs alongside human dispatchers.\n• Live pilot across 2 regional Distribution Centers.")
    ]
    for idx, (title, dur, desc) in enumerate(meth_cards):
        x = Inches(0.8) + idx * (card_w4 + gap4)
        add_card(s9, x, Inches(1.5), card_w4, Inches(5.3))
        tb = s9.shapes.add_textbox(x + Inches(0.15), Inches(1.7), card_w4 - Inches(0.3), Inches(4.9))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(2)
        p1 = tf.add_paragraph(); p1.text = dur; p1.font.size = Pt(11); p1.font.bold = True; p1.font.color.rgb = COLOR_CYAN; p1.space_after = Pt(10)
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(10); p2.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 10: BUSINESS ROI
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_header(s10, "Quantified Business ROI & Investment Impact", "4. Presentation Quality & Investment Justification")
    top_w = Inches(2.7)
    metrics_top = [
        ("$1.8M - $2.4M", "Annual Net Cost Savings", "Fleet, fuel, and carrier rate optimization"),
        ("16.2%", "Mileage & Fuel Reduction", "Consolidated single-drop multi-temp routing"),
        ("14.5%", "Trailer Fill Rate Increase", "Average cube utilization up from 76% to 91%"),
        ("< 5 Months", "Payback Period", "Rapid time-to-value on existing GCP infrastructure")
    ]
    for idx, (val, title, sub) in enumerate(metrics_top):
        x = Inches(0.8) + idx * (top_w + Inches(0.3))
        add_card(s10, x, Inches(1.5), top_w, Inches(1.8), bg_color=RGBColor(240, 253, 250), border_color=COLOR_EMERALD)
        tb = s10.shapes.add_textbox(x + Inches(0.1), Inches(1.6), top_w - Inches(0.2), Inches(1.6))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = val; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD; p.space_after = Pt(2)
        p1 = tf.add_paragraph(); p1.text = title; p1.font.size = Pt(11); p1.font.bold = True; p1.font.color.rgb = COLOR_PRIMARY_DARK; p1.space_after = Pt(2)
        p2 = tf.add_paragraph(); p2.text = sub; p2.font.size = Pt(9.5); p2.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s10, Inches(0.8), Inches(3.6), Inches(5.7), Inches(3.2))
    tb_l = s10.shapes.add_textbox(Inches(1.0), Inches(3.75), Inches(5.3), Inches(2.9))
    tf_l = tb_l.text_frame; tf_l.word_wrap = True
    p = tf_l.paragraphs[0]; p.text = "Legacy Manual Process (Before)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = RGBColor(239, 68, 68); p.space_after = Pt(6)
    b_items = [
        "Siloed dispatchers plan Dry and Frozen routes independently.",
        "Static contracted carrier rates used without checking live spot savings.",
        "Frequent dock congestion and dropped tenders after picking has already started.",
        "Late arrival correction penalties on tight retail grocery delivery windows."
    ]
    for bi in b_items:
        p_b = tf_l.add_paragraph(); p_b.text = f"❌  {bi}"; p_b.font.size = Pt(10); p_b.font.color.rgb = COLOR_TEXT_MUTED; p_b.space_after = Pt(4)

    add_card(s10, Inches(6.8), Inches(3.6), Inches(5.7), Inches(3.2))
    tb_r = s10.shapes.add_textbox(Inches(7.0), Inches(3.75), Inches(5.3), Inches(2.9))
    tf_r = tb_r.text_frame; tf_r.word_wrap = True
    p = tf_r.paragraphs[0]; p.text = "AI Autonomous Engine (After)"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD; p.space_after = Pt(6)
    a_items = [
        "Single-drop multi-temp consolidation with dynamic 2-pallet bulkhead splits.",
        "Parallel rate discovery scores live carriers (40/30/20/10) in <3 seconds.",
        "Guaranteed carrier capacity locked BEFORE WMS picking waves commence.",
        "Interactive dispatcher UI with real-time drag-and-drop constraint validation."
    ]
    for ai in a_items:
        p_a = tf_r.add_paragraph(); p_a.text = f"✅  {ai}"; p_a.font.size = Pt(10); p_a.font.color.rgb = COLOR_TEXT_PRIMARY; p_a.space_after = Pt(4)

    # SLIDE 11: ROADMAP & ASK
    s11 = prs.slides.add_slide(blank_slide_layout)
    add_header(s11, "Project Roadmap, Live MVP Demonstration & Approval Ask", "4. Executive Decision & Next Steps")
    add_card(s11, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))
    tb_rm = s11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.9))
    tf_rm = tb_rm.text_frame; tf_rm.word_wrap = True
    p = tf_rm.paragraphs[0]; p.text = "Implementation Milestones"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY_DARK; p.space_after = Pt(8)
    milestones = [
        ("Sprint 1-2: Interactive MVP Sandbox", "Build the live working demonstrator showcasing route mapping, 2D trailer bulkhead adjustment, and carrier 40/30/20/10 scoring on real sample data."),
        ("Sprint 3-4: 3-Month Historical Backtesting", "Ingest the 3-month historical dataset into BigQuery to prove empirical cost and mileage savings over legacy dispatch logs."),
        ("Sprint 5-6: 2-Month Forward Capacity Simulator", "Run Monte Carlo optimization over the 2-month forecast to simulate peak season trailer fleet adequacy."),
        ("Sprint 7-8: Pilot Deployment", "Connect Cloud Run backend to live WMS/TMS APIs at pilot Distribution Center.")
    ]
    for title, desc in milestones:
        p_m = tf_rm.add_paragraph(); p_m.text = f"{title}: "; p_m.font.bold = True; p_m.font.size = Pt(10.5); p_m.font.color.rgb = COLOR_PRIMARY_DARK
        p_m.add_run().text = desc; p_m.runs[1].font.bold = False; p_m.runs[1].font.size = Pt(10); p_m.runs[1].font.color.rgb = COLOR_TEXT_MUTED
        p_m.space_after = Pt(6)

    add_card(s11, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.3), bg_color=COLOR_PRIMARY_DARK, border_color=None)
    tb_ask = s11.shapes.add_textbox(Inches(7.3), Inches(1.7), Inches(5.0), Inches(4.9))
    tf_ask = tb_ask.text_frame; tf_ask.word_wrap = True
    p = tf_ask.paragraphs[0]; p.text = "Executive Approval & Next Steps"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = COLOR_WHITE; p.space_after = Pt(14)
    ask_items = [
        ("Phase 1 Funding Approval", "Approve budget for GCP infrastructure, mathematical solver licensing, and multi-agent development sprint."),
        ("Data Ingestion Access", "Provide secure GCS/BigQuery pipeline access for the 3-month historical and 2-month forecast order streams."),
        ("Dispatcher Stakeholder Alignment", "Assign lead dispatchers to participate in HITL UX design and live MVP validation."),
        ("Next Step: Live Interactive MVP", "Proceed immediately to construct the interactive MVP demonstrator for real-time executive evaluation.")
    ]
    for h, d in ask_items:
        p_a = tf_ask.add_paragraph(); p_a.text = f"✔  {h}: "; p_a.font.bold = True; p_a.font.color.rgb = COLOR_CYAN
        p_a.add_run().text = d; p_a.runs[1].font.bold = False; p_a.runs[1].font.size = Pt(10.5); p_a.runs[1].font.color.rgb = RGBColor(203, 213, 225)
        p_a.space_after = Pt(10)

    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_pptx = os.path.join(output_dir, "Wholesale_Grocery_Route_Optimization_Executive_Deck.pptx")
    prs.save(output_pptx)
    print(f"Successfully generated PowerPoint: {output_pptx}")

if __name__ == "__main__":
    create_presentation()
