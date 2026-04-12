FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock* .

RUN uv pip install --system --no-cache -e .

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
