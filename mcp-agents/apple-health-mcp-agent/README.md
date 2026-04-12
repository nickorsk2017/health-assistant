# apple-health-mcp-agent

An MCP agent that exposes Apple HealthKit daily metrics via the `get_apple_health_metrics` tool.
Data is generated synthetically by an LLM, simulating the high-frequency tracking output of an Apple Watch.

## Tool

### `get_apple_health_metrics`

| Argument  | Type   | Description                        |
|-----------|--------|------------------------------------|
| `date`    | string | ISO 8601 start date (`YYYY-MM-DD`) |
| `user_id` | string | Identifier of the user             |

Returns a list of `DailyHealthMetrics` objects from `date` to today, each containing:
- **sleep** — total, deep (N3), core (N1+N2), REM, awake, efficiency, time in bed
- **movement** — steps, active energy (kcal), resting energy, exercise minutes, stand hours, distance, flights climbed
- **stress** — HRV SDNN (ms), resting HR, walking HR average, respiratory rate
- **recovery** — derived score, VO2 max, body battery

## Setup

### 1. Environment variables

```bash
cp example.env .env
# Edit .env and set OPENAI_API_KEY
```

### 2. Local development

Requires [uv](https://github.com/astral-sh/uv).

```bash
uv pip install -e .
make run-dev
```

### 3. MCP Inspector (local)

```bash
make run-inspector
```

Opens the MCP Inspector UI at `http://localhost:6274`.

## Docker

### Build

```bash
make build-docker
```

### Run (stdio transport)

```bash
docker run -i --rm --env-file .env apple-health-mcp-agent
```

### MCP Inspector (Docker)

```bash
make run-inspector-docker
```

## Claude Desktop integration

```json
{
  "mcpServers": {
    "apple-health": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--env-file", "/absolute/path/to/.env", "apple-health-mcp-agent"]
    }
  }
}
```
