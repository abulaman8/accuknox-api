# Social media API

## Overview

This is a Django application configured to run within a Docker container. The application uses Docker Compose for easy management of development, testing, and production environments.

[Postman Collection](https://paradox-webops.postman.co/workspace/Paradox-Workspace~f8042fd3-e323-447e-a1f5-7e74c14d48f7/collection/19575325-3e41cee6-9900-41ff-b596-a41e147cf4cf?action=share&creator=19575325)


## Non Docker run instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/abulaman8/accuknox-api.git
cd accuknox-api
```
### 2. Install Dependencies and Run

Install the dependencies and run the application:

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Docker run instructions

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)



### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/abulaman8/accuknox-api.git
cd accuknox-api
```

### 2. Run Docker Compose

```bash
docker compose up
```

### 3. Access the API
To access the API, go to http://127.0.0.1:8000/


