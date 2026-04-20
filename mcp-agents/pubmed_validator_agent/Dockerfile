FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY _common/ _common/
COPY mcp-agents/pubmed_validator_agent/ .

RUN uv pip install --system --no-cache .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["python", "main.py"]
