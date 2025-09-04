
# fastapi_todo_test

## REST API to Manage Tasks (TODOs)
This is a **API REST** built with **FastAPI**, **PostgreSQL** and **SQLAlchemy** to manage tasks with JWT authentication.

### Functional requirements
1. Create, read, update and delete tasks
2. Secure JWT Authentication
3. PostgreSQL Database with SQLAlchemy ORM
4. Data validation with Pydantic v2
5. Error handling and security
6. Integrated logging

# Install requirements
pip install -r requirements.txt

# Run app
uvicorn main:app --reload

# Documentation
- (Swagger) http://localhost:8000/docs
- (Redoc) http://localhost:8000/redoc

## Endpoints (http)
### Register user

POST - http://localhost:8000/api/oauth/register

Content-Type: application/json

{
  "username": "juan",
  "password": "juan123"
}

### Login:

POST - http://localhost:8000/api/oauth/login

Content-Type: application/json

{
  "username": "juan",
  "password": "juan123"
}

### Create a new task

POST - http://localhost:8000/api/tasks

Authorization: Bearer <your_token>

Content-Type: application/json

{
  "title": "Buy milk",
  "description": "Go to supermarket",
  "state": "pending"
}

### List all tasks of the authenticated user

GET - http://localhost:8000/api/tasks

Authorization: Bearer <your_token>

### Get details of a task

GET - http://localhost:8000/api/tasks/1

Authorization: Bearer <your_token>

### Update a task

PUT - http://localhost:8000/api/tasks/1

Authorization: Bearer <your_token>

Content-Type: application/json

{
  "title": "Buy milk",
  "description": "Go to supermarket",
  "state": "completed"
}

### Delete a task

DELETE - http://localhost:8000/api/tasks/1

Authorization: Bearer <your_token>

# Test
pytest test/test.py -v
