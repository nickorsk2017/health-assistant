.PHONY: install build inspect inspect-docker kill-inspector

dev:
	make kill-port
	uv run gp_synthesis_agent

install:
	uv sync

build:
	docker build -t gp_synthesis_agent .

inspect:
	make kill-inspector
	CLIENT_PORT=6306 SERVER_PORT=6307 npx @modelcontextprotocol/inspector uv run inspector

inspect-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env gp_synthesis_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6306 -i :6307) 2>/dev/null || true

kill-port:
	kill -9 $$(lsof -t -i :6334) 2>/dev/null || true