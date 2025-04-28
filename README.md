# Goods Vault backend

## Requirements

* [Python](https://www.python.org/downloads/) (3.12+)
* [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Run

1. Install dependencies via `uv sync`
2. Spin up the database via `docker-compose up -d`
3. Copy `.env.example` to `.env` and fill in the values
4. Apply migrations via `uv run alembic upgrade head`
5. Parse categories via `uv run src/cli.py`
6. Run the server via `uv run src/main.py`
