.PHONY: dev build inspect inspect-docker kill-inspector kill-port

dev:
	make kill-port
	uv run labs_agent

build:
	docker build -t labs_agent .

inspect:
	make kill-inspector
	CLIENT_PORT=6304 SERVER_PORT=6305 npx @modelcontextprotocol/inspector uv run inspector

inspect-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env labs_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6304 -i :6305) 2>/dev/null || true

kill-port:
	kill -9 $$(lsof -t -i :6444) 2>/dev/null || true
