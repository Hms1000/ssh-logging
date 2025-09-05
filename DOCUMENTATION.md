# SSH Logging Tool Documentation

## Table of Contents
- [Project Overview](#project-overview)
- [Setup and Requirements](#setup-and-requirements)
- [Directory Structure](#directory-structure)
- [CI/CD Workflow](#cicd-workflow)
- [Security Notes](#security-notes)
- [NGINX Integration](#nginx-integration)
- [Issues, Warnings and Areas of Improvement](#issues-warnings-and-future-of-improvement)

## Project Overview

**Purpose**  
The SSH logging tool is a backend Python application I designed for IT and Cybersecurity professional to log in securely into remote servers. I created this tool so as to try to save time, automate and simplify auditing, debugging and tracking commands for IT personnel. 

**Key Features** 
- For Secure SSH login I used a Python library `paramiko`, which was key and other libraries in the script.  
- Because I wanted to track the tool, particularly if any errors occur, I used the `logging` library for tracking.  
- I wanted the tool to be command line portable, that's why I imported the `argparse` library.  
- The `pathlib` library was my choice for file reading because it's more Pythonic in this case due to its abilities to make data reading easy.  
- The tool's ability to execute command execution on remote servers was also automated.  
- Log generation (`secure_ssh.log`), which is key in understanding what happened between the client and the server for effective debugging, was integrated.  
- In line with modern Development and Operations practices, I decided to use Docker to containerise the tool for easy deployment; this way the tool can be lightweight, fast and deployable on any environment.  

## Setup and Requirements
- Python 3.12 must be installed locally.  
- Docker and Docker Compose must be installed also.  
- A command line interface is required for running scripts.  
- Secrets stored in `secrets/` folder for database credentials (this requirement might be adjusted in future in line with cloud requirements). When using the tool in the cloud, a keyvault is used to store secrets, so it will not be a requirement to have a `secrets/` folder.  

## Directory Structure
```bash
.
├── DOCUMENTATION.md
├── Dockerfile
├── README.md
├── docker-compose.yml
├── nginx
│   └── default.conf
├── requirements.txt
├── secrets
│   ├── postgres_db.txt
│   ├── postgres_password.txt
│   └── postgres_user.txt
└── src
    ├── secure_ssh.log
    └── ssh-logging.py
```

## CI/CD Workflow

It’s essential to create a CI/CD pipeline for the tool, for easy deployment and integration with other tools.
I used GitHub Actions Workflow to handle:
- Checkout code
- Docker login using secrets
- Build Docker image
- Tagging image with latest and Git commit SHA (this is a way to know which image a user might be using; also great for tracking versioning)
- Pushing images to Docker Hub
- Only the ssh-logging container is built and pushed; NGINX and PostgreSQL are pulled from official images.

## NGINX Integration
```
default.conf: 

server { 
    listen 80; 

    location / { 
        proxy_pass http://ssh-logging; 
        proxy_set_header Host $host; 
        proxy_set_header X-Real-IP $remote_addr; 
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
        proxy_set_header X-Forwarded-Proto $scheme; 
    } 
} 
```
**Explanation:**
- All incoming traffic on port 80 is forwarded to ssh-logging. Only NGINX is exposed to the internet, reducing attack surface.
- NGINX is the reverse-proxy, forwarding client requests securely to ssh-logging. I chose nginx because it's lightweight, easy to use, and supports load balancing in future.
- The ssh-logging tool is currently CLI only; future integration with FastAPI is planned.

## Security Notes
- I decide to manage secrets via Docker secrets (/run/secrets/...) which are read in the script using pathlib.This therefore, assist in avoiding hardcoded credentials, which can be target by malicious actors.
- PostgreSQL credentials are not exposed in the docker-compose file.
- PostgreSQL port 5432 is internal only and is not mapped to host, ensuring our database is not exposed to the internet. This is a measure that restrict user information such as PII to be stolen.
- I ensured logs are stored in volumes, not inside container filesystem.

## Issues, Warnings and Future Improvements
**Pip Warning**
Installing pip as root inside the container.
*Lesson learnt*: Use a virtual environment or non-root user.

**Database URL/Secrets**
Adding DATABASE_URL directly in docker-compose and hardcoding credentials.
*Lesson learnt*: Use Docker secrets instead as this is a more secure method.

**Improvements**
- I plan to Integrate FastAPI for HTTP-based command execution
- I am also going to improve PostgreSQL integration directly in the ssh-logging script, this ensures database secrets are never exposed
- CI/CD enhancements for multi service deployment
- Deploy the ssh-logging tool in the cloud (Azure/AWS/GCP)

### Final Touch
I made some comments and forgot to commit them:
>I should make sure to review every change carefully and commit consistently to avoid losing important history in the future.
