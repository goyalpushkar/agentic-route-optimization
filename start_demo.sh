#!/bin/bash
# Autonomous Multi-Agent Cold-Chain Engine Quick-Start Demo Launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================================================"
echo "  LAUNCHING AUTONOMOUS MULTI-AGENT COLD-CHAIN ENGINE (EXECUTIVE MVP) "
echo "================================================================================"

# 1. Open Interactive Cockpit in default browser
echo ">>> Opening Interactive Web Cockpit in your browser..."
open "${SCRIPT_DIR}/mvp_cockpit.html"

# 2. Run Python Multi-Agent CLI
echo ">>> Executing Python Multi-Agent Swarm CLI..."
python3 "${SCRIPT_DIR}/run_agents.py"

echo "================================================================================"
echo "  Demo Ready! Refer to DEMO_WALKTHROUGH.md for the 5-minute presentation script."
echo "================================================================================"
