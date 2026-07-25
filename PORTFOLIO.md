# Agentic Audit AI — Portfolio Showcase

## Project Overview

Agentic Audit AI is a local, air-gapped adversarial security simulator that blends multi-agent red-team/blue-team dynamics with real sandbox execution and a cyberpunk React dashboard.

The project demonstrates:

- FastAPI backend orchestration for agent-based security reasoning
- Local Ollama model integration for adversarial simulation
- Dynamic RAG policy patching and compliance-driven mitigation
- Docker sandbox execution with honeypot data and breach detection
- WebSocket-powered live dashboard telemetry and threat scoring
- Portfolio-ready documentation and export automation

## Key Features

- **Adversarial agent fight club**: Chaos and rulemaker agents battle to identify and patch policy weaknesses.
- **Sandboxed real command execution**: Ephemeral Alpine containers run suspicious activity against a seeded honeypot.
- **Live threat dashboard**: React/Vite dashboard shows live messages, score rings, patch feed, and threat meter.
- **Compliance and PII firewall**: Built-in detectors guard against data exfiltration and personal information leakage.
- **Export helper**: `deploy/export_repo.sh` packages the repo for sharing without GitHub.

## Tech Stack

- Python 3
- FastAPI + Uvicorn
- React + Vite
- Docker (sandbox engine)
- Ollama (local LLM serving)
- ChromaDB-style compliance engine
- WebSockets for real-time UI updates

## Demo / Portfolio Story

1. Start the local Ollama model server.
2. Launch the FastAPI backend on `localhost:8000`.
3. Run the React dashboard and open the UI in the browser.
4. Press `INITIALIZE ADVERSARIAL FIGHT CLUB` to begin the simulation.
5. Watch the live feed, threat-level meter, and dynamic RAG patch updates.
6. Export the audit report as Markdown or PDF to capture findings.

## Presentation Notes

- Emphasize how this is a **local, secure red-team simulator** rather than a public cloud service.
- Mention the **air-gapped** and **self-hosted** design, which is ideal for sensitive security demonstrations.
- Highlight the **portfolio value** of blending AI, security, compliance, and real execution sandboxing.

## How to Share

Use the included export script to package the repository for offline sharing:

```bash
cd ~/agentic-audit-ai
chmod +x deploy/export_repo.sh
./deploy/export_repo.sh
```

The generated ZIP file can be attached to your portfolio or shared directly with reviewers.

## Optional Portfolio Assets

- Screenshots of the dashboard live feed and threat meter
- A short demo video walking through the attack simulation
- A screenshot of the generated audit report
- A summary sentence like:

> "Agentic Audit AI is a self-hosted adversarial training platform that fuses local LLM-driven red teaming with sandboxed execution and compliance audit automation."
