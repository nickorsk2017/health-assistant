.PHONY: run-dev run-inspector kill-inspector run-inspector-docker build-docker

run-dev:
	uv run apple-health-mcp-agent

run-inspector:
	make kill-inspector
	CLIENT_PORT=6300 SERVER_PORT=6301 npx @modelcontextprotocol/inspector uv run apple-health-mcp-agent

kill-inspector:
	kill -9 $$(lsof -t -i :6300 -i :6301) 2>/dev/null || true

run-inspector-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env apple-health-mcp-agent

build-docker:
	docker build -t apple-health-mcp-agent .
