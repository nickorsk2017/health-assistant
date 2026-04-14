.PHONY: install run build

install:
	uv sync

dev:
	make kill-port
	uv run user_microservice

build:
	docker build -t health-user-microservice .

kill-port:
	kill -9 $$(lsof -t -i :8001) 2>/dev/null || true