.PHONY: install dev build start docker-build docker-run docker

install:
	npm install

dev:
	npm run dev

build:
	npm run build

start:
	npm start

docker-build:
	docker build -t health-assistant-frontend .

docker-run:
	docker run -p 3000:3000 health-assistant-frontend

docker:
	docker compose --env-file ../_common/.env -f ../docker-compose.yml up --build -d frontend
