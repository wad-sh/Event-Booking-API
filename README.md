# Event Booking API

A backend REST API for managing events and reservations.
The project provides user authentication, role-based authorization, event management, and reservation handling with PostgreSQL database integration.

## Features

* User registration and authentication using JWT.
* Secure password hashing.
* Role-based authorization (User / Admin).
* Admin event management:

  * Create events.
  * Update events.
  * Delete events.
* Browse upcoming events.
* User event reservations.
* Prevent duplicate reservations.
* Event capacity management.
* Database migrations using Alembic.
* PostgreSQL integration using SQLAlchemy ORM.

---

## Technologies

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* JWT Authentication
* Uvicorn

---

## Backend Engineering Concepts Implemented

- JWT-based authentication and authorization.
- Role-based access control (Admin/User).
- FastAPI dependency injection using `Depends`.
- SQLAlchemy ORM with PostgreSQL.
- Database schema management using Alembic migrations.
- Transaction management with rollback handling.
- Pessimistic row-level locking using `SELECT FOR UPDATE` for reservation concurrency handling.
- Race condition prevention during event reservations.
- Database constraints for data integrity (unique constraints and foreign keys).
- Layered architecture (routers, services, models, schemas).
- Request validation using Pydantic schemas.

## Project Structure

```
EventBookingAPI/
│
├── app/
│   ├── auth/
│   ├── database/
│   ├── enums/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── migrations/
│   └── main.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone <https://github.com/wad-sh/Event-Booking-API>
```

Navigate into the project:

```bash
cd EventBookingAPI
```

---

## 2. Create virtual environment

```bash
py -m venv venv
```

Activate it:

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
py -m pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/event_booking

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```
---
## Creating the First Admin User

The project includes an admin creation script to initialize the first administrator account.

Run:

```bash
py -m scripts.create_admin
```
The script will:

Ask for admin username, email, and password.
Hash the password securely.
Create a user with Admin role.
Store the admin account in the PostgreSQL database.

This avoids manually modifying the database when setting up the first administrator.


---

## Database Setup

This project uses PostgreSQL.

Make sure PostgreSQL is installed and create a database.

Example:

```sql
CREATE DATABASE event_booking;
```

---

## Run Database Migrations

Apply migrations using Alembic:

```bash
py -m alembic upgrade head
```

To create a new migration after changing models:

```bash
py -m alembic revision --autogenerate -m "describe change"
```

Then apply it:

```bash
py -m alembic upgrade head
```

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

# API Overview

## Authentication

### Register

```
POST /users/register
```

Creates a new user.

---

### Login

```
POST /users/login
```

Returns a JWT access token.

---

## Events

### Get upcoming events

```
GET /events
```

Available for public users.

---

### Create event

```
POST /events
```

Admin only.

---

### Update event

```
PUT /events/{id}
```

Admin only.

---

### Delete event

```
DELETE /events/{id}
```

Admin only.

---

## Reservations

### Reserve an event

```
POST /events/{event_id}/reserve
```

Authenticated users only.

---

### Cancel reservation

```
DELETE /events/{event_id}/reserve
```

Authenticated users only.

---

# Database Design

Main entities:

## User

Stores user information and roles.

## Event

Stores event details:

* Title
* Description
* Date
* Capacity
* Creator

## Reservation

Connects users with events and prevents duplicate reservations.

---

# Security

Implemented:

* JWT authentication.
* Password hashing.
* Protected admin routes.
* Token validation.
* Role-based access control.

---

# Database Management

Alembic is used for tracking database schema changes.

The project avoids direct table creation in production and uses migrations instead.

---

# Future Improvements

Possible improvements:

* Add automated tests.
* Add Docker support.
* Add pagination for events.
* Add email notifications.
* Deploy using cloud services.
* Add CI/CD pipeline.

---

# Author

Wadee'

Backend Developer | Python | FastAPI
