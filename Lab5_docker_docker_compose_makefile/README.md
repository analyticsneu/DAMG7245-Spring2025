# Lab 5: Docker, Docker Compose, and Makefile

## Introduction
This lab introduces three essential DevOps tools:
- **Docker**: For containerizing applications
- **Docker Compose**: For managing multi-container applications
- **Make**: For automating build and deployment processes

### Installation Steps
1. **Docker & Docker Compose**
   - Windows: Install WSL2 + Docker Desktop
   - macOS: Install Docker Desktop
   - Linux: Follow [official installation guide](https://docs.docker.com/get-started/get-docker/)

2. **Verify Installation**
```bash
docker --version
docker-compose --version
make --version
```

## Core Concepts

### Docker Fundamentals
- **Image**: A lightweight, standalone package containing everything needed to run an application.
  ```bash
  # Build an image
  docker build -t myapp:1.0 .
  
  # List images
  docker images
  ```

- **Container**: A running instance of an image with its own isolated environment.
  ```bash
  # Run a container
  docker run -d -p 8080:80 myapp:1.0
  
  # List running containers
  docker ps
  ```

- **Dockerfile**: Instructions for building an image. Each instruction creates a layer.
  ```dockerfile
  # Simple Example
  FROM python:3.9-slim
  WORKDIR /app
  COPY . .
  CMD ["python", "app.py"]
  ```

- **Registry**: Repository for storing and sharing Docker images.
  ```bash
  # Push to Docker Hub
  docker tag myapp:1.0 username/myapp:1.0
  docker push username/myapp:1.0
  
  # Pull from Docker Hub
  docker pull username/myapp:1.0
  ```

### Docker Compose Essentials
- **Services**: Definition of container configurations and their relationships.
  ```yaml
  services:
    webapp:
      build: ./webapp
      ports:
        - "8080:80"
      depends_on:
        - db
  ```

- **Networks**: Enables communication between containers.
  ```yaml
  services:
    webapp:
      networks:
        - frontend
        - backend
  networks:
    frontend:
    backend:
  ```

- **Volumes**: Persistent data storage and sharing between containers.
  ```yaml
  services:
    db:
      volumes:
        - db-data:/var/lib/mysql
  volumes:
    db-data:
  ```

### Makefile Basics
- **Purpose**: Automates common development tasks and builds processes.

- **Structure**: 
  ```makefile
  # Variables for reuse
  DOCKER_COMPOSE = docker-compose
  
  # Target with dependency
  build: check-env
      $(DOCKER_COMPOSE) build
  
  # .PHONY tells Make these aren't files
  .PHONY: build clean
  ```

- **.PHONY**: Special directive to:
  - Prevent conflicts with same-named files
  - Ensure commands always run
  - Improve Make's performance
  ```makefile
  .PHONY: clean
  clean:
      docker-compose down --rmi all
  ```

## Lab Overview

### Project Structure
```
project/
├── frontend/              # Streamlit app
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── backend/              # FastAPI service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── airflow/              # Airflow setup
│   └── dags/
├── docker-compose.yml    # Services configuration
├── Makefile             # Automation commands
└── .env                 # Environment variables
```

### Components
1. **Frontend**: Streamlit dashboard
2. **Backend**: FastAPI service
3. **Airflow**: Workflow management
4. **Docker Compose**: Service orchestration
5. **Makefile**: Build automation

## Step-by-Step Guide

### 1. Basic Docker Operations
```bash
# Basic container operations
docker pull python:3.9-slim
docker run -it python:3.9-slim
docker ps
docker stop <container_id>
```

### 2. Docker Hub Operations
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag myapp:1.0 username/myapp:1.0
docker tag myapp:1.0 username/myapp:latest

# Push images
docker push username/myapp:1.0
docker push username/myapp:latest

# Pull image
docker pull username/myapp:1.0
```

### 3. Project Setup
```bash
# Initialize environment
make env

# Build and start services
make build
make up

# Verify services
make ps
```

### 4. Development Workflow
- Code modification and auto-reload
- Container logs and debugging
- Environment variable management
- Service interaction

### 5. Airflow Integration
- DAG development
- Workflow scheduling
- Monitoring and management

## Best Practices

### Docker
1. **Use Multi-Stage Builds**
   ```dockerfile
   # Build stage
   FROM python:3.9 AS builder
   WORKDIR /build
   COPY requirements.txt .
   RUN pip install --user -r requirements.txt

   # Runtime stage
   FROM python:3.9-slim
   WORKDIR /app
   COPY --from=builder /root/.local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
   COPY . .
   CMD ["python", "app.py"]
   ```

2. **Optimize Image Size**
   - Use slim/alpine base images
   - Combine RUN commands
   - Clean up in the same layer
   ```dockerfile
   RUN apt-get update && \
       apt-get install -y package && \
       rm -rf /var/lib/apt/lists/*
   ```

3. **Implement Health Checks**
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=10s \
     CMD curl -f http://localhost/ || exit 1
   ```

4. **Use .dockerignore**
   ```
   .git
   __pycache__
   *.pyc
   venv
   ```

### Environment Variables
1. Never commit .env files
2. Use .env.example templates
3. Document all variables
4. Implement validation

### Makefile
1. Document all targets
2. Use phony targets for non-file commands
3. Implement dependency checks
4. Keep commands idempotent

## Troubleshooting

### Common Issues
1. **Port Conflicts**
```bash
# Check port usage
sudo lsof -i :8501
sudo lsof -i :8000
```

2. **Container Problems**
```bash
# Access container
docker exec -it <container_id> bash

# View logs
docker logs <container_id>
```

3. **Network Issues**
```bash
# Network inspection
docker network ls
docker network inspect <network_name>
```

## Additional Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)