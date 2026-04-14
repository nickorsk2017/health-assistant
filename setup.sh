#!/usr/bin/env bash
set -euo pipefail

if [ ! -f _common/.env ]; then
  echo "ERROR: _common/.env not found. Create it from the example:"
  echo "  cp _common/.env.example _common/.env"
  echo "  # then fill in OPENAI_API_KEY and POSTGRES_PASSWORD"
  exit 1
fi

docker compose up --build -d

echo ""
echo "Stack is starting. Monitor with: docker compose logs -f"
echo "  Frontend  → http://localhost:3000"
echo "  Gateway   → http://localhost:8000/docs"
