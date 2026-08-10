\# Dockerized Login Application



A containerized login and registration application built with \*\*Flask, MySQL, Nginx, Ubuntu, and Docker Compose\*\*.



The project demonstrates how multiple Docker containers can communicate through a custom Docker network while persistent MySQL storage is maintained through a Docker volume.



\## Project Overview



This project contains:



\* Flask web application for Login, Registration, Dashboard, and Logout

\* MySQL database for storing user accounts

\* Nginx web server

\* Ubuntu client container for network testing

\* Dockerfiles for custom Flask, Nginx, and Ubuntu images

\* Docker Compose for managing all services

\* Custom Docker network for container-to-container communication

\* Persistent MySQL storage using Docker volumes

\* Password hashing using Werkzeug



\## Architecture



```text

&#x20;                   Docker Compose

&#x20;                        |

&#x20;       +----------------+----------------+

&#x20;       |                |                |

&#x20;       v                v                v

&#x20;    Nginx             Flask            MySQL

&#x20;  Container          Container         Container

&#x20;     :80               :5000              |

&#x20;       |                 |                |

&#x20;       |                 +----------------+

&#x20;       |                         |

&#x20;       |                    docker\_login

&#x20;       |                     database

&#x20;       |

&#x20;       v

&#x20;  Host Port 8080



&#x20;                Ubuntu Client

&#x20;                      |

&#x20;                devops-net

```



\## Services



\### 1. Nginx



Nginx serves the frontend page.



\* Image: `custom-nginx:latest`

\* Base image: `nginx:stable-alpine3.24-perl`

\* Container: `custom-nginx`

\* Container port: `80`

\* Host port: `8080`



Access:



```text

http://localhost:8080

```



\### 2. Flask Application



The Flask application handles:



\* User registration



\* User login



\* Dashboard



\* Logout



\* MySQL database communication



\* Image: `flask-login-app:latest`



\* Base image: `python:3.12-slim`



\* Container: `flask-app`



\* Container port: `5000`



\* Host port: `5000`



Access:



```text

http://localhost:5000

```



\### 3. MySQL



MySQL stores registered users.



\* Image: `mysql:latest`

\* Container: `mysql-db`

\* Database: `docker\_login`

\* Username: `root`

\* Password: `root123`



MySQL data is persisted using:



```text

mysql-data:/var/lib/mysql

```



This means deleting the MySQL container does not automatically delete the stored database data as long as the Docker volume remains.



\### 4. Ubuntu Client



An Ubuntu container is included for practicing Docker networking and testing communication between containers.



\* Image: `ubuntu:latest`

\* Container: `ubuntu`

\* Additional package: `iputils-ping`



\## Docker Network



All services are connected to a custom Docker network:



```text

devops-net

```



This allows containers to communicate with each other using their service/container names.



For example, the Flask application connects to MySQL using:



```text

host = db

```



Instead of using:



```text

localhost

```



Inside the Docker network, `db` resolves to the MySQL service.



\## Data Storage



MySQL uses a named Docker volume:



```yaml

volumes:

&#x20; mysql-data:

```



The volume is mounted at:



```text

/var/lib/mysql

```



Architecture:



```text

Flask

&#x20; |

&#x20; v

MySQL Container

&#x20; |

&#x20; v

docker\_login database

&#x20; |

&#x20; v

mysql-data Docker Volume

```



\## Password Security



User passwords are \*\*not stored as plain text\*\*.



The Flask application uses Werkzeug password hashing:



```python

generate\_password\_hash(password)

```



During login, the submitted password is verified against the stored hash using:



```python

check\_password\_hash()

```



Flow:



```text

User Password

&#x20;     |

&#x20;     v

generate\_password\_hash()

&#x20;     |

&#x20;     v

Password Hash

&#x20;     |

&#x20;     v

MySQL

```



During login:



```text

Entered Password

&#x20;     |

&#x20;     v

check\_password\_hash()

&#x20;     |

&#x20;     v

Match / Reject

```



\## Project Structure



```text

Docker-Login-App/

│

├── app/

│   ├── app.py

│   ├── dockerfile

│   ├── requirements.txt

│   │

│   ├── static/

│   │   └── style.css

│   │

│   └── templates/

│       ├── login.html

│       ├── register.html

│       └── dashboard.html

│

├── nginx/

│   ├── dockerfile

│   ├── index.html

│   └── style.css

│

├── ubuntu/

│   └── dockerfile

│

├── docker-compose.yml

└── readme.md

```



\## Dockerfile – Flask



The Flask Dockerfile:



```dockerfile

FROM python:3.12-slim



WORKDIR /app



COPY requirements.txt .



RUN pip install --no-cache-dir -r requirements.txt



COPY . .



EXPOSE 5000



CMD \["python", "app.py"]

```



\## Dockerfile – Nginx



```dockerfile

FROM nginx:stable-alpine3.24-perl



WORKDIR /usr/share/nginx/html



COPY index.html .

COPY style.css .



EXPOSE 80

```



\## Dockerfile – Ubuntu



```dockerfile

FROM ubuntu:latest



RUN apt-get update \&\& apt-get install -y iputils-ping



CMD \["bash"]

```



\## Docker Compose



All services are managed through:



```text

docker-compose.yml

```



Start the complete application with:



```bash

docker compose up -d

```



Check running containers:



```bash

docker compose ps

```



View logs:



```bash

docker compose logs

```



View logs for a specific service:



```bash

docker compose logs app

```



Stop the project:



```bash

docker compose stop

```



Restart the project:



```bash

docker compose restart

```



Stop and remove containers and network:



```bash

docker compose down

```



\## Useful Docker Commands



List containers:



```bash

docker ps

```



List all containers:



```bash

docker ps -a

```



List images:



```bash

docker images

```



List networks:



```bash

docker network ls

```



Inspect the Docker network:



```bash

docker network inspect devops-net

```



List volumes:



```bash

docker volume ls

```



Inspect the MySQL volume:



```bash

docker volume inspect mysql-data

```



Access the Flask container:



```bash

docker exec -it flask-app bash

```



Access the Ubuntu container:



```bash

docker exec -it ubuntu bash

```



\## How to Run



\### Prerequisites



Install:



\* Docker Desktop

\* Docker Compose



Verify Docker:



```bash

docker --version

```



Verify Docker Compose:



```bash

docker compose version

```



\### Start Application



Clone the repository:



```bash

git clone <your-repository-url>

```



Move into the project directory:



```bash

cd Docker-Login-App

```



Start all containers:



```bash

docker compose up -d

```



Check the services:



```bash

docker compose ps

```



Open:



```text

http://localhost:8080

```



or:



```text

http://localhost:5000

```



\## Container Communication



The application demonstrates Docker container networking:



```text

Flask Container

&#x20;     |

&#x20;     | MySQL connection

&#x20;     v

MySQL Container

```



The Flask application connects using the Compose service name:



```text

db

```



All containers share:



```text

devops-net

```



\## Technologies Used



\* Python

\* Flask

\* MySQL

\* Nginx

\* Ubuntu

\* Docker

\* Docker Compose

\* Docker Networking

\* Docker Volumes

\* Werkzeug Password Hashing



\## DevOps Concepts Demonstrated



This project provides practical experience with:



\* Containerization

\* Docker Images

\* Docker Containers

\* Dockerfiles

\* Docker Compose

\* Multi-container applications

\* Container Networking

\* Docker Volumes

\* Persistent Database Storage

\* Custom Images

\* Environment Variables

\* Service Dependencies

\* Application-to-Database Communication

\* Password Hashing



\## Future Improvements



Possible improvements for a production-ready version:



\* Move database credentials to environment variables or Docker secrets

\* Use a production WSGI server such as Gunicorn

\* Configure Nginx as a reverse proxy

\* Remove Flask debug mode

\* Add health checks

\* Add CI/CD using GitLab

\* Add SAST, SCA, and DAST security scanning

\* Push application images to Docker Hub or GitLab Container Registry

\* Deploy the application to a cloud server

\* Add HTTPS with SSL/TLS



\## Author



\*\*Muhammad Mouzam Sabir\*\*



DevOps Enthusiast 





