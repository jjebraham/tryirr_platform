# Makefile for tryirr_platform

# Build images
.PHONY: build
build:
	docker-compose build

# Start everything (with auto-migrations & collectstatic via entrypoint)
.PHONY: up
up:
	docker-compose up -d

# Tear down
.PHONY: down
down:
	docker-compose down

# Tail the web logs
.PHONY: logs
logs:
	docker-compose logs -f web

# Run Django migrations
.PHONY: migrate
migrate:
	docker-compose exec web python manage.py migrate --noinput

# Create new migrations for 'core'
.PHONY: makemigrations-core
makemigrations-core:
	docker-compose exec web python manage.py makemigrations core

# Get a shell inside the web container
.PHONY: shell
shell:
	docker-compose exec web sh

# Show running containers
.PHONY: ps
ps:
	docker-compose ps

