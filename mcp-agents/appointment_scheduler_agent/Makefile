.PHONY: dev inspector kill-inspector inspector-docker build-docker

dev:
	make kill-port
	uv run appointment-scheduler-agent

inspector:
	make kill-inspector
	npx @modelcontextprotocol/inspector uv run appointment-scheduler-agent

kill-inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

inspector-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env appointment-scheduler-agent

build-docker:
	docker build -t appointment-scheduler-agent .

kill-port:
	kill -9 $$(lsof -t -i :6342) 2>/dev/null || true
