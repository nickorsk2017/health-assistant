.PHONY: dev inspector kill-inspector inspector-docker build-docker

dev:
	uv run pubmed_validator_agent

inspector:
	make kill-inspector
	npx @modelcontextprotocol/inspector uv run pubmed_validator_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

inspector-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env pubmed-validator-agent

build-docker:
	docker build -t pubmed-validator-agent .
