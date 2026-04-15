# AI Health Assistant

An AI-powered clinical decision support system that performs multidisciplinary patient evaluations using a coordinated network of specialist language model agents. The system aggregates patient history, laboratory results, wearable device data, and complaints, runs them through a 9-specialist AI consilium, and synthesizes a unified GP consultation with diagnosis, treatment plan, and prognosis.

---

## What It Does

A patient (or doctor on their behalf) submits a request for a health evaluation. The system automatically:

1. Retrieves the patient's SOAP history, lab results, device readings, and active complaints in parallel
2. Passes all data through a **Medical Consilium** — 9 specialist LLM agents (cardiology, oncology, gastroenterology, hematology, nephrology, nutrition, endocrinology, mental health, pulmonology) running concurrently
3. A **GP Synthesis Agent** reads all specialist findings and produces a single, unified consultation: diagnosis, treatment plan, prognosis, and a patient-facing health summary
4. Results are displayed in the frontend for the doctor or the patient, depending on the active role

The system also supports appointment scheduling, complaint management, and integration with wearable devices (Oura Ring, Apple Health).

---

## Architecture

```
Browser
  └── Next.js Frontend (port 3000)
        └── FastAPI Gateway (port 8000)
              ├── user_microservice          — patient registry, auth
              ├── master_orchestrator_agent  — coordinates full evaluation pipeline
              │     ├── client_history_agent — SOAP visit history (Postgres)
              │     ├── labs_agent           — laboratory results (Postgres)
              │     ├── doctors_agent        — 9-specialist MDT consilium (LLM)
              │     ├── gp_synthesis_agent   — final GP consultation (LLM)
              │     ├── devices_agent        — wearable aggregator
              │     │     ├── oura_ring_agent
              │     │     └── apple_health_agent
              │     └── complaint_manager_agent
              └── appointment_scheduler_agent
```

**Stack**

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, Zustand |
| Gateway | Python 3.12, FastAPI, Uvicorn |
| Agents | Python 3.12, FastMCP, LangChain, OpenAI |
| Database | PostgreSQL 16 |
| Infra | Docker, Docker Compose |

All agents communicate with the gateway via HTTP using the MCP (Model Context Protocol) over `streamable-http` transport. The frontend communicates with the gateway via REST only.

---

## Quick Start

### Prerequisites

- Docker and Docker Compose v2
- An OpenAI API key

### Install Docker

**macOS**

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Open the `.dmg` and drag Docker to Applications
3. Launch Docker Desktop and wait for the whale icon in the menu bar to stop animating

**Windows**

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer (requires WSL 2 — the installer will prompt you to enable it)
3. Restart your machine if asked, then launch Docker Desktop

**Linux (Ubuntu / Debian)**

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER   # lets you run docker without sudo (re-login to apply)
```

Verify the installation:

```bash
docker --version        # Docker version 26.x or higher
docker compose version  # Docker Compose version v2.x or higher
```

### 1. Clone the repository

```bash
git clone <repo-url>
cd health-assistant
```

### 2. Create your environment file

```bash
cp _common/.env.example _common/.env
```

Open `_common/.env` and fill in the two required values:

```env
OPENAI_API_KEY=sk-...          # your OpenAI key
POSTGRES_PASSWORD=your_secret  # choose any strong password
```

Everything else can be left at its default. See [Environment Variables](#environment-variables) for the full reference.

### 3. Start the stack

```bash
make dev
```

This builds all Docker images and starts every service in the background. On first run it will take a few minutes to download base images and install dependencies.

Wait until the gateway is healthy, then open:

After run http://localhost:3000 on your browser


## Makefile Reference

Run all commands from the **project root**.

| Command | Description |
|---|---|
| `make dev` | Build images and start all services (development) |
| `make up` | Start already-built services |
| `make down` | Stop and remove containers |
| `make build` | Build images without starting |
| `make build-nc` | Force full rebuild (no Docker layer cache) |
| `make restart` | Full stop → start cycle |
| `make logs` | Tail logs from all services |
| `make ps` | Show container status |
| `make clean` | Stop, remove volumes and local images |
| `make prune` | Remove unused Docker build cache |
| `make nuke` | Wipe everything — all images, volumes, build cache |

---

## Environment Variables

A single file, `_common/.env`, is the source of truth for the entire stack. Every service reads from it at container startup.

### LLM

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | **Yes** | OpenAI API key used by all LLM agents |
| `OPENAI_MODEL` | No | Model name (default: `gpt-5-mini`) |

### Database

| Variable | Required | Default | Description |
|---|---|---|---|
| `POSTGRES_USER` | No | `postgres` | PostgreSQL username |
| `POSTGRES_PASSWORD` | **Yes** | — | PostgreSQL password |
| `POSTGRES_DB` | No | `health_assistant` | Database name |
| `POSTGRES_HOST` | No | `postgres` | Hostname — must match the service name in `docker-compose.yml` |
| `POSTGRES_PORT` | No | `5432` | Port |
| `DATABASE_URL` | Auto | — | Assembled from the fields above; do not set manually |

### Internal Agent URLs

These are Docker internal hostnames. **Do not change** unless you rename services in `docker-compose.yml`.

| Variable | Default |
|---|---|
| `CLIENT_HISTORY_AGENT_URL` | `http://client_history_agent:6332/mcp` |
| `LABS_AGENT_URL` | `http://labs_agent:6444/mcp` |
| `DOCTORS_AGENT_URL` | `http://doctors_agent:6333/mcp` |
| `GP_SYNTHESIS_AGENT_URL` | `http://gp_synthesis_agent:6334/mcp` |
| `DEVICE_ORCHESTRATOR_AGENT_URL` | `http://devices_agent:6340/mcp` |
| `COMPLAINT_MANAGER_AGENT_URL` | `http://complaint_manager_agent:6341/mcp` |
| `APPOINTMENT_SCHEDULER_AGENT_URL` | `http://appointment_scheduler_agent:6342/mcp` |
| `MASTER_ORCHESTRATOR_AGENT_URL` | `http://master_orchestrator_agent:6350/mcp` |
| `OURA_RING_AGENT_URL` | `http://oura_ring_agent:6330/mcp` |
| `APPLE_HEALTH_AGENT_URL` | `http://apple_health_agent:6331/mcp` |
| `USER_SERVICE_URL` | `http://user_microservice:8001` |

### Gateway

| Variable | Default | Description |
|---|---|---|
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins for the gateway |

### Frontend

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api/v1` | Gateway URL as seen by the **browser**. Use `localhost` (not the internal Docker hostname) because this is called from the user's machine. Change this if you deploy the gateway to a remote host. |

> **Note:** `NEXT_PUBLIC_API_URL` is baked into the Next.js bundle at Docker build time. If you change it, run `make build-nc` to force a full rebuild of the frontend image.

---

## How It Works — Data Flow

### GP Diagnosis (full evaluation)

```
GET /api/v1/diagnosis/{user_id}?start_date=YYYY-MM-DD
  └── gateway → master_orchestrator_agent
        │
        ├── [parallel fetch]
        │     ├── client_history_agent  → SOAP visit records from Postgres
        │     ├── labs_agent            → lab results from Postgres
        │     ├── devices_agent         → wearable data (Oura, Apple Health)
        │     └── complaint_manager_agent → active complaints from Postgres
        │
        ├── doctors_agent (consilium)
        │     └── 9 specialist LLMs run in parallel, each producing findings
        │
        └── gp_synthesis_agent
              └── reads all findings → produces unified consultation
                    {diagnosis, treatment, prognosis, summary}
```

### MDT Consilium only

```
GET /api/v1/consilium/{user_id}?start_date=YYYY-MM-DD
  └── gateway → master_orchestrator_agent
        ├── fetch history + labs in parallel
        └── doctors_agent → 9 specialist findings
```

### Other endpoints

| Endpoint prefix | Agent / Service | Storage |
|---|---|---|
| `/api/v1/patients` | user_microservice | Postgres |
| `/api/v1/patient-history` | client_history_agent | Postgres |
| `/api/v1/analyses` | labs_agent | Postgres |
| `/api/v1/complaints` | complaint_manager_agent | Postgres |
| `/api/v1/appointments` | appointment_scheduler_agent | Postgres |
| `/api/v1/devices` | devices_agent | (wearable APIs) |

---

## User Roles

The frontend supports two roles selectable on first load:

- **Doctor** — can view all patients, trigger evaluations, edit records
- **Patient** — sees only their own data

The role is stored in `localStorage` and enforced in the UI. There is no server-side authentication in the current version.

---

## Project Structure

```
/
├── _common/
│   └── .env                  # Single env file for the full stack
├── frontend/                 # Next.js application
│   ├── app/                  # Routes (App Router)
│   ├── components/           # UI components
│   ├── services/             # REST API clients
│   ├── stores/               # Zustand state
│   └── types/                # TypeScript types
├── backend/
│   ├── gateway/              # FastAPI gateway — all REST endpoints
│   └── user_microservice/    # Patient registry
├── mcp-agents/
│   ├── master_orchestrator_agent/
│   ├── doctors_agent/        # 9-specialist MDT consilium
│   ├── gp_synthesis_agent/   # Final GP consultation
│   ├── client_history_agent/ # SOAP history
│   ├── labs_agent/           # Lab results
│   ├── complaint_manager_agent/
│   ├── appointment_scheduler_agent/
│   ├── devices_agent/        # Wearable aggregator
│   ├── oura_ring_agent/
│   └── apple_health_agent/
├── docker-compose.yml
├── Makefile
└── setup.sh
```
