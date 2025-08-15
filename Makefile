.PHONY: up down etl api dbsh test

up:
	 docker compose up -d --build

down:
	 docker compose down -v

etl:
	 docker compose run --rm flow python etl/flow.py

api:
	 open http://localhost:8000/docs || true

dbsh:
	 docker compose exec db psql -U postgres -d quakewatch

test:
	 docker compose run --rm api pytest -q
