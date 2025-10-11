dev:
	poetry run uvicorn src.vulnrisk.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest src/tests

lint:
	poetry run black src && poetry run flake8 src && poetry run mypy src

build:
	docker build -t vulnrisk-backend .

deploy-staging:
	echo "Deploy to staging not yet implemented." 