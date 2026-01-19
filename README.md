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
git clone https://github.com/your-username/todo-list-fastapi.git
cd todo-list-fastapi
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Install Dependencies:
```
pip install -r requirements.txt
```

4. Run the server
```
uvicorn main:app --reload
```

5. Open documentation at http://127.0.0.1:8000/docs