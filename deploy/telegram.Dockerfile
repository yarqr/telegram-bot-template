FROM python:3.11-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==1.8
RUN poetry install --with=infra,telegram --no-cache

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/app/.venv/bin:$PATH"

COPY --from=base /app/.venv .venv/

COPY .env .
COPY config config/
COPY src src/

ENTRYPOINT ["python", "-m", "src.presentation.telegram"]
