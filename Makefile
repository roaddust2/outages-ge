ENV=poetry run


# Main commands

install:
	poetry install

lint:
	$(ENV) flake8

dev:
	$(ENV) uvicorn main:app --reload

setup:
	$(ENV) python3 ./app/cli.py setup_cities
	$(ENV) python3 ./app/cli.py setup_districts

update-streets:
	$(ENV) python3 ./app/cli.py update_streets


# Alembic migrations

alembic-revision:
	$(ENV) alembic revision --autogenerate -m '$(msg)'

alembic-upgrade:
	$(ENV) alembic upgrade head