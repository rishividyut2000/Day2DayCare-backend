.PHONY: up down migrate tenant test lint fmt

up:        ; docker compose up -d
down:      ; docker compose down
migrate:   ; python manage.py migrate_schemas --shared && python manage.py migrate_schemas
tenant:    ; python manage.py provision_tenant --code $(CODE) --name "$(NAME)" --email $(EMAIL)
test:      ; pytest
lint:      ; ruff check . && mypy .
fmt:       ; ruff format . && ruff check --fix .
