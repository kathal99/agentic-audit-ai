# Agentic Audit AI

Local multi-agent security training arena with Ollama, FastAPI, and a Vite React dashboard.

## Setup

1. Create a Python virtual environment in `agentic-audit-ai`:

```bash
cd ~/agentic-audit-ai
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

2. Install the frontend dependencies:

```bash
cd ~/agentic-audit-ai/frontend
npm install
```

3. Run Ollama locally:

```bash
ollama serve
```

4. Run the backend server:

```bash
cd ~/agentic-audit-ai/backend
source ../venv/bin/activate
uvicorn server:app --reload --port 8000
```

5. Run the frontend dashboard:

```bash
cd ~/agentic-audit-ai/frontend
npm run dev
```

## Docker Sandbox Mode

This project now includes a Kinetic Docker sandbox engine that can run real commands in an ephemeral Alpine container seeded with honeypot data.

1. Install Docker on Linux Mint:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker kali
```

2. Restart your session or reboot so the Docker group membership takes effect.

3. Install the backend Docker dependency:

```bash
cd ~/agentic-audit-ai/backend
source ../venv/bin/activate
pip install docker
```

4. Configure optional alerting in `backend/config.py`:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-url"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/webhook/url"
```

### New Files

- `backend/sandbox_engine.py` — creates a locked Alpine container, seeds fake creds and SSNs, executes Tyler's commands, and returns output.
- `backend/alerts.py` — dispatches Discord/Slack breach alerts.
- `backend/config.py` — sandbox settings, canary payloads, webhook config.
- `deploy/agentic-backend.service` and `deploy/agentic-frontend.service` — systemd unit templates for production.

## Deployment and Service Automation

Use the helper scripts in `deploy/`:

```bash
chmod +x deploy/start_services.sh deploy/run_services.sh deploy/init_github.sh
./deploy/start_services.sh
./deploy/run_services.sh
```

## GitHub Setup

```bash
git init
git branch -M main
git add .
git commit -m "feat: init Agentic Audit AI"
git remote add origin git@github.com:kathal99/agentic-audit-ai.git
git push -u origin main
```

Make sure your SSH key is configured for GitHub. If you need HTTPS instead, replace the remote URL with `https://github.com/kathal99/agentic-audit-ai.git`.

## Local Export for Sharing

If you want a local archive of the repo without using GitHub, run the export helper script from the project root:

```bash
chmod +x deploy/export_repo.sh
./deploy/export_repo.sh
```

This generates a ZIP archive in the project root like `agentic-audit-ai-export-YYYYMMDD-HHMMSS.zip`, excluding `.git`, `node_modules`, and `venv`.

## One-Step Local View

To install dependencies, start the backend and frontend, and open the dashboard in one step, run:

```bash
chmod +x deploy/view.sh
./deploy/view.sh
```

Then open your browser to:

```bash
http://127.0.0.1:5173
```

If your environment supports it, the script will also attempt to open the browser automatically.
