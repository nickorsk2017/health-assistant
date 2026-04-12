.PHONY: run-dev run-inspector kill-inspector run-inspector-docker build-docker

run-dev:
	uv run oura-ring-mcp-agent

run-inspector:
	make kill-inspector
	npx @modelcontextprotocol/inspector uv run oura-ring-mcp-agent

kill-inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

run-inspector-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env oura-ring-mcp-agent

build-docker:
	docker build -t oura-ring-mcp-agent .
