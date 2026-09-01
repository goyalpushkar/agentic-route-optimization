# Overnight MVP Build: Timing Estimate + GCP Agent Platform Deployment Plan

## Context
`implementation_plan.md`, `MVP_Agents_1.jpg`, and `MVP_Architecture.png` describe a 6-agent + HITL-gateway cold-chain routing/carrier-booking system, currently scoped in the exec deck (`generate_deck.py`/`presentation.html`) as a 16-week phased build (Phase 1–4). `mvp_plan.md` separately lays out a 6-week phased MVP sprint plan.

This document answers a narrower, time-boxed question: a **working, demoable MVP deployed by tomorrow morning** to show executives, with the 6 agents deployed on **Google's Agent platform (Vertex AI Agent Runtime / ADK)**. It gives an honest hour-by-hour feasibility timeline for that overnight build, the scope cuts required to hit the deadline, and the concrete Agent Runtime deployment steps per agent — as a fast-path alternative/precursor to the fuller 6-week plan in `mvp_plan.md`.

**Reality check up front:** everything in `MVP_Agents_1.jpg`/`MVP_Architecture.png` at full fidelity (production OR-Tools MC-VRPTW solver, live drag-and-drop 2D trailer physics, Firestore multi-dispatcher optimistic locking, full BI/forecast dashboard, IAP/SSO) is not realistically buildable, tested, and deployed by one team overnight. What **is** achievable overnight is a real, live, end-to-end run of all 6 agents against synthetic data, deployed on GCP, with a UI good enough to walk executives through the story convincingly. The plan below is built around that target, with the corners it cuts called out explicitly so it's a decision made up front, not a surprise at 6am.

---

## Scope for Tonight (in vs. deferred)

| Component | Tonight (MVP demo) | Deferred to Phase 2+ (per existing roadmaps) |
|---|---|---|
| Agents 1–2 (Demand Profiler, Fleet Allocator) | Full logic, real rules, synthetic order/fleet data | BigQuery-backed live data |
| Agent 3 (Route Optimizer) | **Simplified heuristic** (nearest-neighbor + time-window + cube feasibility check), not full OR-Tools MC-VRPTW | Full OR-Tools/Cloud Optimization API MC-VRPTW solver, <300ms live re-solve on drag |
| Agent 4 (Carrier Rate Aggregator) | Simulated parallel quote generator (as designed — MVP table already calls this "simulated") | Real carrier API/EDI integration |
| Agent 5 (Carrier Scoring & Booking) | Full 40/30/20/10 scoring, real math, simulated booking lock | Real EDI 204 transmission |
| Agent 6 (Cold-Chain Monitor) | Simulated timer-triggered alert event (as designed — table already says "Simulated") | Real IoT/telematics feed |
| HITL Gate 1 (Route review) | Real approve/reject buttons wired to backend state machine | Full drag-and-drop stop editor with live recalculation |
| Trailer bulkhead visualizer | Static/semi-interactive 2D colored grid, bulkhead slider recalculates pallet counts on click (not live physics) | Full drag-and-drop, LIFO violation animation |
| Carrier scorecard board | Full ranked cards, real one-click approve | — (in scope as designed) |
| Map | Google Maps JS API polylines if key/billing already provisioned; else Leaflet/OSM fallback | Deck.gl, soft-window violation shading |
| Multi-dispatcher collab (Firestore locking) | Out | Later phase |
| BI/forecast dashboard (2-mo simulation, 3-mo backtest) | Out — replace with 3 static "impact" tiles (miles saved, cube fill 78%→92%, cost delta) computed from the demo run | Later phase |
| Auth/SSO/IAP | Out (open demo URL, or basic password gate) | Later phase |

This is the single biggest lever on whether "tomorrow morning" is achievable — if the full-fidelity solver or drag-and-drop physics must stay in scope, the timeline below does not hold and should be re-cut.

---

## Team Needed

Minimum **2 people** working in parallel tonight (one on agents/backend, one on frontend), ideally **3** (add one on deploy/infra + demo data/script) — using Claude Code / AI-assisted coding throughout is what makes the compressed timeline plausible at all; this is not a realistic timeline for hand-written code at this scope.

---

## Hour-by-Hour Timeline (~12–13 focused hours, elapsed from kickoff)

| Time | Track A: Agents/Backend | Track B: Frontend | Track C: Infra/Deploy |
|---|---|---|---|
| **Hr 0–0.5** | Lock scope (table above), confirm GCP project ID, billing, Maps API key/billing status | — | Confirm GCP project, enable `run.googleapis.com`, `cloudbuild.googleapis.com`, `secretmanager.googleapis.com`, `aiplatform.googleapis.com` |
| **Hr 0.5–1** | `agents-cli scaffold create` — single ADK project, 6 sub-agents + orchestrator, deployment target `agent_runtime` | Scaffold Next.js app, lay out 4 views as static components | Set up Artifact Registry / confirm `agents-cli` auth (`gcloud auth login` / ADC) |
| **Hr 1–2** | Build synthetic data: 40–60 wholesale grocery orders (Frozen/Chill/Ambient/HMBC mix), 3 trailer types (46W/48W/53W), 5 mock carriers — bake in as JSON fixtures | Build order demand cards + fleet pool views against fixture JSON (no backend yet) | Provision Memorystore Redis if used; otherwise skip (in-process cache is fine for a single-instance demo) |
| **Hr 2–4** | Agents 1–2 (profiler, fleet allocator) as ADK sub-agents/tools; Agent 3 heuristic solver (nearest-neighbor + time-window + cube check, NOT full OR-Tools) | Interactive map view wired to mock route output; trailer bulkhead 2D grid (static + slider) | — |
| **Hr 4–6** | Agents 4–6 (simulated carrier quotes, 40/30/20/10 scorer, simulated telemetry timer) + HITL gateway agent (approval state machine) | Carrier scorecard board; HITL approve/override buttons; live "agent activity" log feed (high demo value, cheap to build) | Stand up thin Cloud Run FastAPI+WebSocket gateway (see deployment plan) — deploy skeleton NOW, don't leave first deploy to hour 10 |
| **Hr 6–8** | Wire orchestrator: ingest → profile → allocate → route → **HITL 1** → rate agg → score → **HITL 2** → simulated booking/WMS → telemetry alert | Wire frontend to backend REST/WebSocket; replace all mock JSON with live calls | First real deploy of Agent Runtime app; smoke test `agents-cli run` against it |
| **Hr 8–9.5** | End-to-end run-through, fix state machine edge cases | Wire "impact" tiles (miles saved, cube 78%→92%, cost delta) computed from the actual demo run output, not hardcoded | Deploy Cloud Run gateway + frontend; confirm gateway ↔ Agent Runtime path works end-to-end in the deployed environment (not just localhost) |
| **Hr 9.5–11** | Bug bash on deployed environment (things break differently deployed vs local — budget real time here) | Same | Same — this hour is buffer, expect to need it |
| **Hr 11–12** | Seed final "wow" demo data, rehearse the click-path once end-to-end on the deployed URL | | Record a screen-capture fallback video of one full successful run, in case live demo hits a GCP hiccup in front of executives |
| **Hr 12–13** | Buffer | Buffer | Buffer |

**Biggest risks, called out:**
1. **Agent 3's solver is the single highest-risk item.** A real MC-VRPTW solve is not a few-hour task. Ship the heuristic and be ready to say "the production solver ships in a later phase" if asked.
2. **First-time Agent Runtime deploys take 5–10 min and can hit IAM propagation delays** (a few minutes per grant) — deploy early (hour ~6), not for the first time at hour 11.
3. **Google Maps JS API key/billing** is a classic late-night blocker if not already enabled on the project — confirm in hour 0, have the Leaflet/OSM fallback ready.
4. **Deployed-environment bugs differ from localhost** (auth headers, CORS, WebSocket through Cloud Run's proxy) — the plan reserves ~1.5 hrs for this; don't skip it to "save time" earlier.
5. Have a **recorded fallback** of a clean run — live demos in front of executives are exactly where you don't want to debug a cold start on stage.

---

## GCP Agent Platform Deployment Plan (per agent)

Vertex AI **Agent Runtime** (formerly Agent Engine) is the managed "Agent platform" target — deployed via `agents-cli deploy --deployment-target agent_runtime` (no `gcloud` equivalent exists; it packages the project's Dockerfile and builds server-side, 5–10 min per deploy).

**Tonight's topology (recommended for speed):** the 6 agents run as ADK sub-agents/tools inside **one Agent Runtime deployment** (an orchestrator agent invoking them in-process — sequential for 1→2→3, fan-out for 4, then 5, then 6), fronted by a **thin Cloud Run FastAPI+WebSocket gateway** that the Next.js UI talks to. Agent Runtime doesn't expose arbitrary custom WebSocket routes the way Cloud Run does, which is why the real-time HITL/UI layer needs a Cloud Run BFF in front of it even though the agent logic itself lives on the Agent platform. Splitting all 6 into independently-scaled Agent Runtime deployments tonight would multiply the deploy/IAM/CI surface for no benefit at this scope — that split is the natural production move, mapped out below.

| # | Agent | Tonight's deployment unit | Production path (later) |
|---|---|---|---|
| 1 | Demand & Order Profiler | Sub-agent inside the single Agent Runtime app | Own Agent Runtime deployment, `agents-cli deploy --service-name demand-profiler` |
| 2 | Fleet & Dock Allocator | Same app | Own Agent Runtime deployment |
| 3 | Cold-Chain Route Optimizer | Same app (heuristic solver as a tool) | Cloud Run instead of Agent Runtime — needs VPC-native Memorystore access and sub-300ms latency for live recalculation, which favors Cloud Run's networking control per the deployment decision matrix |
| 4 | Live Carrier Rate Aggregator | Same app | Own Agent Runtime deployment, or Cloud Run if real carrier webhooks need native Pub/Sub/Eventarc triggers |
| 5 | Carrier Decision & Booking | Same app | Own Agent Runtime deployment |
| 6 | Dynamic Cold-Chain Monitor | Same app (simulated via in-process timer tonight) | Event-driven: Cloud Scheduler → Pub/Sub → Agent Runtime `/api` trigger passthrough |
| — | HITL Gateway | **Cloud Run** (FastAPI + WebSocket, calls into the Agent Runtime app) | Same — stays on Cloud Run for networking/WebSocket control |
| — | Next.js Frontend | Cloud Run (or Firebase Hosting) | Same |

**Concrete steps tonight:**
1. `agents-cli scaffold create route-mvp --deployment-target agent_runtime` — one project, orchestrator + 6 sub-agents.
2. Build/test locally (`agents-cli run` or local uvicorn) through hour ~5.
3. `gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com aiplatform.googleapis.com --project=<PROJECT_ID>`.
4. First deploy by hour ~6: `agents-cli deploy --project <PROJECT_ID> --region us-central1 --no-confirm-project` (use `--no-wait` + `--status` to avoid blocking on the 5–10 min build).
5. Deploy the Cloud Run HITL gateway (`gcloud run deploy` or `agents-cli deploy --deployment-target cloud_run` for the gateway service) pointing at the Agent Runtime endpoint.
6. Deploy Next.js frontend to Cloud Run, env-configured to the gateway's URL.
7. Grant the gateway's service account `roles/aiplatform.user` (or the specific Agent Runtime invoker role) so it can call the deployed agent.
8. Re-deploy iteratively through hours 6–11 as bugs surface — expect several redeploys, budget for the 5–10 min Agent Runtime build time each round (this is itself a reason to keep agents consolidated into one deployment tonight rather than 6).

**After the demo**, splitting into 6 independent Agent Runtime deployments (one `agents-cli deploy` per agent, each with its own service account and IAM scoped narrowly) plus moving Agent 3 to Cloud Run is the natural next step and lines up with the fuller roadmap in `mvp_plan.md` / the deck — nothing tonight forecloses that path.

---

## Verification (tonight)
- Local end-to-end run of the full pipeline against fixture data before any deploy (hour ~6).
- Deployed end-to-end run on the actual Cloud Run/Agent Runtime URLs, not just localhost (hour ~9.5–11) — this is where WebSocket/CORS/auth issues actually show up.
- Rehearse the exact click-path (ingest → HITL 1 approve → HITL 2 approve → simulated booking/WMS/telemetry event) at least twice on the deployed URL before presenting.
- Have the recorded fallback video ready as a backup.

## Open items to confirm before starting the clock
- GCP project ID/billing account to deploy into, and whether Google Maps API + billing is already enabled on it.
- Confirm the scope cuts in the table above are acceptable, or flag which ones must stay in scope (this directly changes whether "tomorrow morning" is achievable).
- How many people are actually available tonight (changes whether Track A/B/C run in parallel or serially).
- **Reconcile with `mvp_plan.md`**, which lays out a 6-week phased build for the same MVP scope — worth deciding which document is the one you're actually executing against tonight vs. later.
