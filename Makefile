.PHONY: help install sync run makemigrations migrate createsuperuser shell test check collectstatic

PYTHON = uv run python
MANAGE = $(PYTHON) manage.py

help:
	@echo "Available commands:"
	@echo "  make install          Install/sync project dependencies"
	@echo "  make sync             Sync dependencies with uv.lock"
	@echo "  make run              Start Django development server"
	@echo "  make makemigrations   Create Django migrations"
	@echo "  make migrate          Apply Django migrations"
	@echo "  make createsuperuser  Create Django superuser"
	@echo "  make shell            Open Django shell"
	@echo "  make test             Run Django tests"
	@echo "  make check            Run Django system checks"
	@echo "  make collectstatic    Collect static files"

install:
	uv sync

sync:
	uv sync

run:
	$(MANAGE) runserver

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

test:
	$(MANAGE) test

check:
	$(MANAGE) check

collectstatic:
	$(MANAGE) collectstatic --noinput