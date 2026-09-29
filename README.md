# Job Application Tracker API

![CI](https://github.com/Charanya3408/job-tracker-api/actions/workflows/ci.yml/badge.svg)

A REST API for tracking job applications and analyzing your search funnel:
which sources actually get responses, and how many applications reach
interviews and offers.

**Stack:** Python, FastAPI, SQLAlchemy 2.0, SQLite, JWT auth, pytest, Docker, GitHub Actions

## Features

- JWT authentication with bcrypt-hashed passwords
- Full CRUD for applications, strictly scoped per user
  (another user's records return 404, never 403, so IDs don't leak)
- Filtering and pagination on the list endpoint
- SQL-aggregated analytics: funnel conversion, response rate by source,
  weekly application volume
- 16 automated tests on an isolated in-memory database, run in CI on every push

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Get a JWT access token |
| GET | `/auth/me` | Current user |
| POST | `/applications` | Add an application |
| GET | `/applications` | List (filters: `status`, `source`, `limit`, `offset`) |
| GET / PATCH / DELETE | `/applications/{id}` | Read, update, delete one |
| GET | `/analytics/summary` | Status counts, response / interview / offer rates |
| GET | `/analytics/by-source` | Response and interview rate per source |
| GET | `/analytics/weekly` | Applications per week |

Interactive docs are served at `/docs` (Swagger UI).

## Run locally

    git clone https://github.com/Charanya3408/job-tracker-api.git
    cd job-tracker-api
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Optional: `python -m scripts.seed` loads sample data for `test1@example.com`
(register that account first).

## Tests

    python -m pytest -v

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | dev-only value | JWT signing key. **Set this in any real deployment.** |
| `DATABASE_URL` | `sqlite:///./tracker.db` | Any SQLAlchemy URL (e.g. Postgres) |

## Possible next steps

- Alembic migrations
- Postgres in Docker Compose
- Refresh tokens and rate limiting on auth routes
- Streamlit dashboard on top of the analytics endpoints
