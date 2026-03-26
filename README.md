# 📋 Task Management API

A REST API for managing tasks, projects, and team collaboration — built with **FastAPI** and **PostgreSQL**.

---

## 🚀 Features

- 🔐 **JWT Authentication** — Register, login, and secure every endpoint with Bearer tokens
- 👥 **User Roles** — Admin, Manager, and Member roles defined (enforcement on routes planned)
- 📁 **Project Management** — Create and manage projects with full CRUD operations
- ✅ **Task Management** — Create, assign, filter, and track tasks with status and priority
- 💬 **Comments** — Add comments to tasks for team collaboration
- 📎 **Attachments** — Upload and manage file attachments on tasks
- 🔔 **Reminders** — Store reminder timestamps for tasks
- 📜 **Activity Logs** — Model defined (Automatic tracking planned)


---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| **FastAPI** | Web framework — routing, request/response handling |
| **PostgreSQL** (Supabase) | Relational database |
| **SQLAlchemy** | ORM — Python classes mapped to DB tables |
| **Alembic** | Database migrations |
| **Pydantic** | Data validation and serialization |
| **python-jose** | JWT token creation and verification |
| **passlib + bcrypt** | Password hashing |
| **uvicorn** | ASGI server |

---

## 📁 Project Structure

```
task_manager/
  ├── app/
  │   ├── main.py              # FastAPI app entry point
  │   ├── database.py          # SQLAlchemy engine + session
  │   ├── core/
  │   │   ├── config.py        # Environment variable settings
  │   │   ├── security.py      # JWT + password hashing
  │   │   └── dependencies.py  # Auth dependencies + role checks
  │   ├── models/              # SQLAlchemy ORM models
  │   │   ├── user.py
  │   │   ├── project.py
  │   │   ├── task.py
  │   │   ├── comment.py
  │   │   ├── activity_log.py
  │   │   ├── attachment.py
  │   │   └── reminder.py
  │   ├── schemas/             # Pydantic request/response schemas
  │   │   ├── user.py
  │   │   ├── project.py
  │   │   ├── task.py
  │   │   └── attachment.py
  │   ├── routers/             # API route handlers
  │   │   ├── auth.py
  │   │   ├── projects.py
  │   │   ├── tasks.py
  │   │   ├── comments.py
  │   │   └── attachments.py
  │   └── tasks/               # placeholder for future background tasks
  │       └── reminders.py
  ├── tests/                   # placeholder — tests not yet implemented
  ├── alembic/                 # placeholder — migrations not yet configured
  ├── .env                     # Environment variables (not committed)
  ├── requirements.txt
  └── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (or Supabase account)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```env
DATABASE_URL=postgresql://your-db-url
SECRET_KEY=your-secret-key
```

> Generate a secret key:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 5. Run the application
```bash
uvicorn app.main:app --reload
```

### 6. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "abc",
  "email": "abc@gmail.com",
  "password": "password123",
  "role": "member"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "abc@gmail.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user profile |

### Projects
| Method | Endpoint | Description |
|---|---|---|
| POST | `/projects/` | Create a new project |
| GET | `/projects/` | List all your projects |
| GET | `/projects/{id}` | Get a single project |
| PUT | `/projects/{id}` | Update a project |
| DELETE | `/projects/{id}` | Delete a project |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | List all tasks (filterable) |
| GET | `/tasks/{id}` | Get a single task |
| PATCH | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

### Comments
| Method | Endpoint | Description |
|---|---|---|
| POST | `/comments/` | Add a comment |
| GET | `/comments/task/{task_id}` | List comments |
| DELETE | `/comments/{comment_id}` | Delete comment |

### Attachments
| Method | Endpoint | Description |
|---|---|---|
| POST | `/attachments/` | Manage file attachment metadata (URL-based)|
| GET | `/attachments/{id}` | Get attachment details |
| DELETE | `/attachments/{id}` | Delete attachment |

### Reminders
| Method | Endpoint | Description |
|---|---|---|
| POST | `/reminders/` | Create a reminder |

---

## 🗄️ Database Schema

The system uses **7 PostgreSQL tables:**

```
users          — stores user accounts with roles
projects       — projects owned by users
tasks          — tasks linked to projects and users
comments       — comments on tasks
activity_logs  — automatic change history (JSONB metadata)
attachments    — file metadata linked to tasks
reminders      — scheduled reminders for tasks
```

---

## 👥 User Roles

Three roles are defined in the system: **admin**, **manager**, and **member**.

| Role | Intended Permissions |
|---|---|
| **member** | View and update assigned tasks |
| **manager** | Create projects, assign tasks |
| **admin** | Full access — manage users, delete anything |

> **Note:** The `role` field is stored on the user and role-checking dependencies (`require_admin`, `require_manager`) are implemented in `core/dependencies.py`. However, role enforcement is not yet applied to routes — all authenticated users currently have equal access. This will be enforced in a future update.

---

## 🧪 Tests

Tests have not been implemented yet. This is planned for a future stage using **pytest** and **httpx**.

```
tests/    ← currently empty, to be implemented
```

---

## 📝 Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret key |

---

## 🔒 Security Features

- Passwords hashed with **bcrypt** — never stored in plain text
- JWT tokens expire after **30 minutes**
- Refresh tokens valid for **7 days**
- Role-based access control (to be implemented)
- Sensitive fields (password_hash) never exposed in API responses

---

## 📌 Notes

- API documentation available at `/docs` (Swagger UI) and `/redoc`
- Database tables are auto-created on startup via `Base.metadata.create_all()` — Alembic migrations are not yet configured
- This project uses Supabase as a hosted PostgreSQL provider
- Tests folder exists but is currently empty — to be implemented in a future stage

---

## 🙋 Author

Built as a portfolio project to practice FastAPI, PostgreSQL, SQLAlchemy, and backend development fundamentals.
