ENV=poetry run

install:
	poetry install

lint:
	$(ENV) flake8

dev:
	$(ENV) uvicorn main:app --reload