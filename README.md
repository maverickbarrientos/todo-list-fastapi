# Todo List API

Backend API for user-owned tasks with CRUD operations, filtering, and authentication.  
Built with **FastAPI**, **SQLAlchemy (async)**, and **Pydantic**. Designed for **learning real-world backend patterns**: service layer, dependency injection, protected endpoints.

---

## Features

- ✅ Task CRUD (Create, Read, Update, Delete)
- ✅ Filtering by category
- ✅ Limit query parameter
- ✅ Ownership protection (user-specific tasks)
- ✅ Service layer separation (business logic)
- ✅ Protected endpoints using `current_active_user`
- 🔜 Future: Websockets notifications

---

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy (Async)
- Pydantic
- PostgreSQL / SQLite (for development)
- Uvicorn (server)

---

## Setup

1. Clone the repo:
```bash
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api
