POETRY?=poetry
COMPOSE=docker compose

.PHONY: up down seed demo lint test install

up:
$(COMPOSE) --env-file .env up -d --build

up-ui:
cd ui-admin && npm install && npm run start

down:
$(COMPOSE) --env-file .env down

seed:
bash scripts/seed.sh

demo:
bash demo.sh

install:
for svc in services/*; do \
if [ -f $$svc/pyproject.toml ]; then \
cd $$svc && $(POETRY) install && cd - >/dev/null; \
fi; \
done

test:
for svc in services/*; do \
if [ -f $$svc/pyproject.toml ]; then \
cd $$svc && $(POETRY) run pytest && cd - >/dev/null || exit 1; \
fi; \
done

lint:
for svc in services/*; do \
if [ -f $$svc/pyproject.toml ]; then \
cd $$svc && $(POETRY) run ruff check . && cd - >/dev/null || exit 1; \
fi; \
done
