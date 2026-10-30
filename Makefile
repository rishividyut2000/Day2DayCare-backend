.PHONY: up down migrate tenant test lint fmt prod-up prod-down prod-logs

up:        ; docker compose up -d
down:      ; docker compose down

prod-up:   ; docker compose -f docker-compose.prod.yml up -d --build
prod-down: ; docker compose -f docker-compose.prod.yml down
prod-logs: ; docker compose -f docker-compose.prod.yml logs -f
migrate:   ; python manage.py migrate_schemas --shared && python manage.py migrate_schemas
tenant:    ; python manage.py provision_tenant --code $(CODE) --name "$(NAME)" --email $(EMAIL)
test:      ; pytest
lint:      ; ruff check . && mypy .
fmt:       ; ruff format . && ruff check --fix .
