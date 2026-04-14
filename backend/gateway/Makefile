.PHONY: install run build

install:
	uv sync

dev:
	make kill-port
	uv run gateway

build:
	docker build -t health-gateway .

kill-port:
	kill -9 $$(lsof -t -i :8000) 2>/dev/null || true