# Makefile for Docker operations

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER = docker
ENV_FILE = .env

# Check if .env file exists, if not create from example
check-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example $(ENV_FILE); \
	fi

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "  make build      - Build all Docker images"
	@echo "  make up         - Start all containers"
	@echo "  make down       - Stop and remove all containers"
	@echo "  make restart    - Restart all containers"
	@echo "  make logs       - View container logs"
	@echo "  make clean      - Remove all containers and images"
	@echo "  make ps         - List running containers"
	@echo "  make env        - Create .env file from example if it doesn't exist"

# Build images
build: check-env
	$(DOCKER_COMPOSE) build

# Start containers
up: check-env
	$(DOCKER_COMPOSE) up -d

# Stop containers
down:
	$(DOCKER_COMPOSE) down

# Restart containers
restart: down up

# View logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Clean up
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

# Show running containers
ps:
	$(DOCKER_COMPOSE) ps

# Individual service commands
frontend-logs:
	$(DOCKER_COMPOSE) logs -f frontend

backend-logs:
	$(DOCKER_COMPOSE) logs -f backend

# Development commands
dev-build: check-env
	$(DOCKER_COMPOSE) -f docker-compose.yml build

dev-up: check-env
	$(DOCKER_COMPOSE) -f docker-compose.yml up -d

dev-down:
	$(DOCKER_COMPOSE) -f docker-compose.yml down

# Environment file commands
env: check-env

# Prevent command names from being interpreted as files
.PHONY: help build up down restart logs clean ps frontend-logs backend-logs dev-build dev-up dev-down check-env env