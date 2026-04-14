.PHONY: install build inspect inspect-docker kill-inspector

dev:
	make kill-port
	uv run client_history_agent

add-mockup-history:
	uv run seed_clinical_history

build:
	docker build -t client_history_agent .

inspect:
	make kill-inspector
	CLIENT_PORT=6302 SERVER_PORT=6303 npx @modelcontextprotocol/inspector uv run inspector

inspect-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env client_history_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6302 -i :6303) 2>/dev/null || true

kill-port:
	kill -9 $$(lsof -t -i :6332) 2>/dev/null || true
