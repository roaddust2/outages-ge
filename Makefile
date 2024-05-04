ENV=poetry run


# Main commands

install:
	poetry install

lint:
	$(ENV) flake8

dev:
	$(ENV) uvicorn main:app --reload


# Alembic migrations

alembic-revision:
	$(ENV) alembic revision --autogenerate -m '$(msg)'

alembic-upgrade:
	$(ENV) alembic upgrade head