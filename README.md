
# Django Authentication Service

A **Django-based authentication system** with JWT support, PostgreSQL, Redis caching, email-based password reset, and built-in rate limiting on authentication endpoints. This project is deployed on **Render** with integrated API documentation (Swagger, ReDoc, and Postman).  

---

## Features
- User registration with unique email-based login
- JWT authentication (`access` + `refresh` tokens)
- Password reset via email (with Redis token storage)
- Role-based permissions (`AllowAny`, `IsAuthenticated`, `IsAdminUser`)
- User detail management (view/update/delete)
- Rate limiting on login & password reset endpoints
- API documentation with **Swagger**, **ReDoc**, and **Postman**
- CI/CD integration with GitHub Actions

---

## Tech Stack
- **Backend**: Django, Django REST Framework (DRF)
- **Auth**: JWT (SimpleJWT)
- **Database**: PostgreSQL
- **Cache & Tokens**: Redis
- **Email**: SMTP (Gmail configured)
- **Deployment**: Render
- **Docs**: Swagger, ReDoc, Postman

---

## API Documentation
- **ReDoc**: [ReDoc](https://auth-service-zfrd.onrender.com/api/schema/redoc/)  
- **Swagger/OpenAPI**: [Swagger](https://auth-service-zfrd.onrender.com/api/schema/swagger-ui/)  
- **Postman Collection**: [Postman](https://documenter.getpostman.com/view/45172601/2sB3Hhthop)  

---

## Setup Instructions

### Clone the repo
```bash
git clone https://github.com/ugberaeseac/auth_service.git
cd auth-service
```

### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment variables
Copy `.env.sample` to `.env` and fill in your secrets.

```bash
cp .env.sample .env
```

### Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Redis (if running locally or with Docker)
```bash
sudo service redis-server start
```

```bash
docker run -d --name redis -p 6379:6379 redis
```

### Run the development server
```bash
python manage.py runserver
```

---

## API Endpoints

### Authentication
#### Register
`POST /api/auth/register/`

**Request:**
```json
{
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "email": "testuser@demo.com",
  "password": "StrongPass123"
}
```

**Response:**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "email": "testuser@demo.com",
  "created_at": "2025-08-30T10:00:00Z"
}
```

#### Login
`POST /api/auth/login/`

**Request:**
```json
{
  "email": "testuser@demo.com",
  "password": "StrongPass123"
}
```

**Response:**
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

#### Refresh Token
`POST /api/auth/token/refresh/`

**Request:**
```json
{
  "refresh": "jwt_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_jwt_access_token"
}
```

### Password Management

#### Forgot Password
`POST /api/auth/password/forgot/`

**Request:**
```json
{
  "email": "testuser@demo.com"
}
```

**Response:**
```json
{
  "detail": "If the email exists, a reset link has been sent"
}
```

#### Reset Password
`POST /api/auth/password/reset/`

**Request:**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "token": "a_secureRandomToken123",
  "new_password": "NewStrongPass123"
}
```

**Response:**
```json
{
  "detail": "Your password has been reset"
}
```

### Users

#### Get All Users (Admin only)
`GET /api/users/`

#### Get Single User
`GET /api/users/<user_id>/`

#### Update User
`PUT /api/users/<user_id>/`

#### Delete User
`DELETE /api/users/<user_id>/`

---

## Running Tests
```bash
python manage.py test
```

---

## Rate Limiting
The following endpoints are rate-limited:
- `login`: **5 requests/min**
- `forgot_pass`: **3 requests/min**
- `reset_pass`: **5 requests/min**

---

## Deployment (Render)
- Backend: Django + PostgreSQL + Redis services connected on Render  
- CI/CD: GitHub Actions runs tests on pull requests & merges