# Image Classification FastAPI App

A full-stack machine learning application for classifying images using a pre-trained convolutional neural network (CNN). The system consists of a FastAPI backend, Streamlit frontend, and Docker-based deployment.

##  Business Use Case

A company with a large catalog of images needs to automate classification into over 1,000 categories. Manual classification is slow and error-prone.

This app provides:
- An intuitive web interface for users to upload images
- A FastAPI backend that preprocesses the image and runs predictions
- Real-time results with support for user feedback and error handling

##  System Architecture

- **Frontend**: Streamlit app for user interaction
- **Backend API**: FastAPI service hosting the CNN model
- **Model**: Pre-trained TensorFlow CNN
- **Message Broker**: Redis (optional for async tasks)
- **Docker**: Multi-service deployment using Docker Compose

##  Tech Stack

- **Python**
- **FastAPI** – REST API for model inference
- **TensorFlow** – CNN image classifier (pre-trained)
- **Streamlit** – Web UI
- **Redis** – Service communication
- **Docker / Docker Compose** – Container orchestration
- **Pytest** – Unit and integration testing
- **Black / isort** – Code formatting

##  Features

- Upload image → Get predicted class (JSON)
- Responsive web UI for interaction
- End-to-end containerized deployment
- Integration and unit tests with Docker
- API docs via FastAPI (Swagger UI)

##  Project Structure

.
├── api/ # FastAPI app
├── model/ # TensorFlow model wrapper
├── ui/ # Streamlit frontend
├── tests/ # Unit & integration tests
├── docker-compose.yml
├── .env / .env.original
└── README.md

bash
Copiar
Editar

##  Installation & Setup

1. Clone repo and copy env file
```bash
git clone https://github.com/ArocenaAlfredo/image-classification-fastapi-app.git
cd image-classification-fastapi-app
cp .env.original .env
Create network and build services

bash
Copiar
Editar
docker network create shared_network
docker-compose up --build -d
Access the services:

 FastAPI Docs: http://localhost:8000/docs

 Web UI (Streamlit): http://localhost:9090

Login credentials:

pgsql
Copiar
Editar
user: admin@example.com
pass: admin
 Run Tests
Unit Tests inside Docker:
bash
Copiar
Editar
cd api/
docker build -t fastapi_test --target test .
Do the same in model/ and ui/ folders for respective services.

Integration Test:
bash
Copiar
Editar
pip install -r tests/requirements.txt
python tests/test_integration.py
Expected output:

nginx
Copiar
Editar
Ran 2 tests in 0.299s
OK
 Code Formatting
bash
Copiar
Editar
isort --profile=black .
black --line-length=88 .
This project demonstrates the deployment of a scalable, containerized ML system with a modern Python backend and a user-friendly interface.
