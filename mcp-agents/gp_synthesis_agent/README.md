# gp-synthesis-agent

The final orchestrator in the health assistant pipeline. Acts as the **Head of the Medical Board** — calls `medical-consilium-agent`, synthesizes all specialist findings through a GPT-4o GP synthesis LLM, and returns a unified clinical consultation.

## Pipeline position

```
visit_doctor_agent          (stores SOAP notes in PostgreSQL)
        ↓
medical_consilium_agent     (9 specialist LLMs in parallel)
        ↓
gp-synthesis-agent          (final GP synthesis — this agent)
```

## Tool

### `get_final_gp_consultation`

| Argument                    | Type   | Description                                         |
|-----------------------------|--------|-----------------------------------------------------|
| `user_id`                   | string | Patient identifier                                  |
| `start_date_clinic_history` | string | ISO 8601 start date for history retrieval (`YYYY-MM-DD`) |

Returns a single `GPConsultation` object:

```json
{
  "diagnosis": "Primary Hyperparathyroidism (E21.0) ...",
  "treatment": "1. [URGENT] Parathyroidectomy referral ...\n2. ...",
  "prognosis": "With successful parathyroidectomy ...",
  "summary": "Over the past several months, you visited ..."
}
```

## Setup

### 1. Start upstream agents

```bash
# Terminal 1 — visit_doctor_agent (PostgreSQL + HTTP)
cd mcp-agents/visit_doctor_agent
uv run visit_doctor_agent   # starts on MCP_HOST:MCP_PORT (default 0.0.0.0:6332)

# Terminal 2 — medical_consilium_agent (HTTP)
cd mcp-agents/medical_consilium_agent
uv run medical_consilium_agent   # starts on port 6305 by default
```

### 2. Configure environment

```bash
cp example.env .env
# Edit CONSILIUM_AGENT_URL to match the running consilium agent
# Edit OPENAI_API_KEY
```

### 3. Local development

```bash
make install
make inspect   # opens MCP Inspector at http://localhost:6306
```

## Docker

```bash
make build
docker run -i --rm --env-file .env gp-synthesis-agent
```

## GP Synthesis Prompt

The system prompt (`prompts/gp_synthesis.md`) instructs the LLM to:
1. Identify a **unifying root diagnosis** across all specialist reports
2. **Resolve treatment conflicts** (e.g., a drug recommended by one specialist and contraindicated by another)
3. Produce a **patient-friendly narrative** — no unexplained jargon
4. Return a structured 4-field output: `diagnosis`, `treatment`, `prognosis`, `summary`
