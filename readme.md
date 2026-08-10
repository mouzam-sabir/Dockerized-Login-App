# Dockerized Login Application

A multi-container Login and Registration Web Application built with Flask, MySQL, Nginx, Ubuntu, Docker, and Docker Compose.

## Project Overview

This project demonstrates practical Docker and DevOps concepts by running a web application as multiple interconnected containers.

### Features

- User registration
- User login
- Dashboard
- Logout
- MySQL database
- Password hashing
- Custom Docker images
- Dockerfiles
- Docker Compose
- Docker networking
- Persistent Docker volume
- Ubuntu container for network testing
- Nginx web server

## Architecture

    User
      |
      v
    Nginx
      |
      v
    Flask Application
      |
      v
    MySQL Database
      |
      v
    Docker Volume

All containers communicate through the custom Docker network:

    devops-net

## Services

### Flask Application

The Flask container runs the backend application and handles authentication and database communication.

- Image: `flask-login-app:latest`
- Container: `flask-app`
- Port: `5000`
- Base image: `python:3.12-slim`

Application:

    http://localhost:5000

### MySQL Database

MySQL stores the registered user data.

- Image: `mysql:latest`
- Container: `mysql-db`
- Database: `docker_login`

Persistent storage:

    mysql-data:/var/lib/mysql

### Nginx

Nginx is used as the web server for the frontend.

- Image: `custom-nginx:latest`
- Container: `custom-nginx`
- Container port: `80`
- Host port: `8080`

Application:

    http://localhost:8080

### Ubuntu Client

The Ubuntu container is used for practicing and testing Docker networking.

- Image: `ubuntu:latest`
- Container: `ubuntu`
- Tool: `iputils-ping`

Example:

    docker exec -it ubuntu bash
    ping db

## Docker Network

The containers communicate through:

    devops-net

The Flask application connects to MySQL using the Docker Compose service name:

    db

It does not use `localhost` because `localhost` inside a container refers to that same container.

Docker provides internal DNS so services can communicate using their service names.

Example:

    Flask Container
          |
          | db
          v
    MySQL Container

## Database Storage

MySQL uses a named Docker volume:

    mysql-data

The volume is mounted inside the MySQL container at:

    /var/lib/mysql

Storage flow:

    Flask
      |
      v
    MySQL Container
      |
      v
    docker_login Database
      |
      v
    mysql-data Volume

The volume keeps database data persistent when the MySQL container is recreated.

## Password Security

Passwords are not stored as plain text.

The Flask application uses Werkzeug password hashing.

During registration:

    generate_password_hash(password)

During login:

    check_password_hash()

Authentication flow:

    User Password
          |
          v
    generate_password_hash()
          |
          v
    Password Hash
          |
          v
    MySQL

During login, the entered password is compared with the stored hash.

## Project Structure

    Docker-Login-App/
    |
    +-- app/
    |   +-- app.py
    |   +-- dockerfile
    |   +-- requirements.txt
    |   +-- static/
    |   |   +-- style.css
    |   +-- templates/
    |       +-- login.html
    |       +-- register.html
    |       +-- dashboard.html
    |
    +-- nginx/
    |   +-- dockerfile
    |   +-- index.html
    |   +-- style.css
    |
    +-- ubuntu/
    |   +-- dockerfile
    |
    +-- docker-compose.yml
    +-- README.md

## Flask Dockerfile

    FROM python:3.12-slim

    WORKDIR /app

    COPY requirements.txt .

    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 5000

    CMD ["python", "app.py"]

## Nginx Dockerfile

    FROM nginx:stable-alpine3.24-perl

    WORKDIR /usr/share/nginx/html

    COPY index.html .
    COPY style.css .

    EXPOSE 80

## Ubuntu Dockerfile

    FROM ubuntu:latest

    RUN apt-get update && apt-get install -y iputils-ping

    CMD ["bash"]

## Docker Compose

Docker Compose manages all application services from a single `docker-compose.yml` file.

### Build and Start

    docker compose up -d --build

### Check Services

    docker compose ps

### View Logs

    docker compose logs

### Follow Logs

    docker compose logs -f

### Stop Services

    docker compose stop

### Start Services

    docker compose start

### Restart Services

    docker compose restart

### Remove Containers and Network

    docker compose down

### Remove Containers and Volumes

    docker compose down -v

> Be careful with `docker compose down -v` because it removes the MySQL volume and its stored database data.

## Useful Docker Commands

### Images

List images:

    docker images

Pull an image:

    docker pull mysql:latest

Build an image:

    docker build -t my-python-app .

Tag an image:

    docker tag my-python-app username/my-python-app:v1

Remove an image:

    docker rmi IMAGE_ID

Inspect an image:

    docker image inspect IMAGE_NAME

### Containers

List running containers:

    docker ps

List all containers:

    docker ps -a

Run a container:

    docker run nginx

Run in detached mode:

    docker run -d nginx

Stop a container:

    docker stop CONTAINER_NAME

Start a container:

    docker start CONTAINER_NAME

Restart a container:

    docker restart CONTAINER_NAME

Remove a container:

    docker rm CONTAINER_NAME

View container logs:

    docker logs CONTAINER_NAME

Access a running container:

    docker exec -it CONTAINER_NAME bash

### Volumes

List volumes:

    docker volume ls

Create a volume:

    docker volume create my-volume

Inspect a volume:

    docker volume inspect mysql-data

Remove a volume:

    docker volume rm my-volume

### Networks

List networks:

    docker network ls

Inspect a network:

    docker network inspect devops-net

Create a network:

    docker network create my-network

Connect a container:

    docker network connect my-network CONTAINER_NAME

Disconnect a container:

    docker network disconnect my-network CONTAINER_NAME

## How to Run the Project

### Prerequisites

Install:

- Docker Desktop
- Docker Compose
- Git

Verify Docker:

    docker --version

Verify Docker Compose:

    docker compose version

Verify Git:

    git --version

### Clone Repository

    git clone <your-repository-url>

Enter the project directory:

    cd Docker-Login-App

### Build and Start

    docker compose up -d --build

Check the running services:

    docker compose ps

## Access the Application

Flask:

    http://localhost:5000

Nginx:

    http://localhost:8080

## Test Container Networking

Enter the Ubuntu container:

    docker exec -it ubuntu bash

Test MySQL connectivity:

    ping db

Test Flask connectivity:

    ping app

This demonstrates container-to-container communication through the Docker network.

## Technologies Used

- Python
- Flask
- MySQL
- Nginx
- Ubuntu
- Docker
- Docker Compose
- Docker Networking
- Docker Volumes
- Werkzeug Password Hashing

## DevOps Concepts Demonstrated

- Containerization
- Docker Images
- Docker Containers
- Dockerfiles
- Docker Compose
- Multi-container applications
- Custom Docker images
- Docker networking
- Docker volumes
- Persistent database storage
- Environment variables
- Service dependencies
- Container-to-container communication
- Application-to-database communication
- Password hashing
- Docker CLI
- Container troubleshooting

## Future Improvements

- GitLab CI/CD
- GitLab Runner
- Automated testing
- SAST
- DAST
- SCA
- Secret Detection
- Container Scanning
- Nginx reverse proxy
- Gunicorn
- HTTPS/SSL
- Docker Hub image publishing
- GitLab Container Registry
- Cloud deployment
- Kubernetes
- Monitoring and logging

## Author

**Muhammad Mouzam Sabir**

DevOps / DevSecOps

## Project Goal

The goal of this project is to understand how a real-world web application can be containerized as multiple interconnected Docker services while maintaining persistent database storage, container networking, and secure password handling.
