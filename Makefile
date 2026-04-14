.PHONY: up down build build-nc dev logs ps restart clean prune nuke

export NEXT_PUBLIC_API_URL = $(shell grep '^NEXT_PUBLIC_API_URL=' _common/.env | cut -d= -f2-)

COMPOSE = docker compose --env-file _common/.env

# Start all services in background
up:
	$(COMPOSE) up -d

# Build images without starting containers
build:
	$(COMPOSE) build

# Build images from scratch ignoring the cache
build-nc:
	$(COMPOSE) build --no-cache

# Build and start services in background (Development mode)
dev:
	$(COMPOSE) up --build -d

# Stop and remove containers and networks
down:
	$(COMPOSE) down

# Follow log output from services
logs:
	$(COMPOSE) logs -f

# List containers and their status
ps:
	$(COMPOSE) ps

# Restart all services (Full cycle)
restart:
	$(COMPOSE) down && $(COMPOSE) up -d

# Remove unused Docker build cache layers
prune:
	docker builder prune -f

# Stop services and remove volumes, orphans, and local images
clean:
	$(COMPOSE) down --volumes --remove-orphans --rmi local

# Wipe everything: all images, volumes, and deep build cache
nuke:
	$(COMPOSE) down --volumes --remove-orphans --rmi all
	docker system prune --volumes --all -f
	docker builder prune -a -f