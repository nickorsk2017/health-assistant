# oura-ring-mcp-agent

An MCP agent that exposes Oura Ring biometric data via the `get_daily_oura_biometrics` tool.
Biometric records are generated synthetically by an LLM, simulating realistic day-to-day Oura Ring output.

## Tool

### `get_daily_oura_biometrics`

| Argument  | Type   | Description                            |
|-----------|--------|----------------------------------------|
| `date`    | string | ISO 8601 start date (`YYYY-MM-DD`)     |
| `user_id` | string | Identifier of the user                 |

Returns a list of `DailyBiometrics` objects covering every day from `date` to today, each containing:
- **sleep** — score, total/REM/deep hours, efficiency
- **movement** — steps, distance, active calories, activity score
- **recovery** — readiness score, HRV (ms), resting HR, temperature deviation, stress score

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
# or directly:
docker build -t oura-ring-mcp-agent .
```

### Run (stdio transport)

```bash
docker run -i --rm --env-file .env oura-ring-mcp-agent
```

The container runs the agent over **stdio**, which is the standard transport for MCP clients (e.g. Claude Desktop, Cursor).

### MCP Inspector (Docker)

```bash
make run-inspector-docker
```

## Claude Desktop integration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "oura-ring": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--env-file", "/absolute/path/to/.env", "oura-ring-mcp-agent"]
    }
  }
}
```
