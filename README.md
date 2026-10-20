# FastAPI – The Complete Course 2026

My hands-on notes and code while working through **[FastAPI - The Complete Course 2026 (Beginner + Advanced)](https://www.udemy.com/)** by Eric Roby & Chad Darby on Udemy.

Goal: build production-style REST APIs with Python and FastAPI, from the basics through databases, authentication and deployment.

## Repository Structure

| Folder | What's inside |
|---|---|
| `0-Study material` | Notes and reference material for FastAPI concepts |
| `1-Request Method Logic` | GET, POST, PUT, DELETE logic, path & query parameters |
| `2-Move Fast With FastAPI` | Pydantic validation, status codes, HTTP exceptions |
| `3-Database with SQL` | SQLAlchemy models, SQL database integration, CRUD (incl. DELETE on DB) |

More sections will be added as I progress through the course.

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite (local dev)

## Getting Started

```bash
# clone
git clone https://github.com/IshwarRajChauhan/<repo-name>.git
cd <repo-name>

# virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install fastapi uvicorn sqlalchemy

# run any section (example)
cd "3-Database with SQL"
uvicorn main:app --reload
```

Then open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## What I've Covered So Far

- [x] Request methods (GET, POST, PUT, DELETE)
- [x] Path parameters
- [x] Status codes & HTTP exceptions
- [x] Database setup with SQL / SQLAlchemy
- [x] CRUD operations on a database (incl. DELETE)
- [ ] Authentication (OAuth2, JWT)
- [ ] Authorization & user roles
- [ ] Testing
- [ ] Deployment

## Course

- **Title:** FastAPI - The Complete Course 2026 (Beginner + Advanced)
- **Instructors:** Eric Roby, Chad Darby
- **Platform:** Udemy

## Author

**Ishwar Raj Chauhan**
GitHub: [@IshwarRajChauhan](https://github.com/IshwarRajChauhan)

---

*This repo is for learning purposes. Course content belongs to its respective instructors.*
