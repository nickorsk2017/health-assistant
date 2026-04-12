.PHONY: install build inspect inspect-docker kill-inspector

dev:
	uv run medical_consilium_agent

build:
	docker build -t medical_consilium_agent .

inspect:
	make kill-inspector
	CLIENT_PORT=6304 SERVER_PORT=6305 npx @modelcontextprotocol/inspector uv run medical_consilium_agent

inspect-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env medical_consilium_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6304 -i :6305) 2>/dev/null || true
