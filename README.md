# Django + Next.js Hackathon Boilerplate

A batteries-included full-stack boilerplate for moving fast.

| Layer | Stack |
|-------|-------|
| Backend | Django 5 + Django Ninja + ninja-jwt |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Next.js 14 (App Router) + TypeScript |
| Styling | Mantine UI v7 |
| Data fetching | TanStack Query v5 + openapi-fetch |
| API types | openapi-typescript (generated from Django Ninja) |
| Linting | ruff (Python) + ESLint (TS) |
| Type checking | mypy (Python) + tsc (TypeScript) |
| Testing | pytest-django (Python) + Vitest (TypeScript) |
| CI | GitHub Actions |

---

## Quick Start (Docker)

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/ |
| API Docs (Swagger) | http://localhost:8000/api/docs |
| Django Admin | http://localhost:8000/admin/ |

Create a superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

---

## Manual Dev Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env             # edit as needed

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
pnpm install
cp .env.example .env.local       # edit as needed
pnpm dev
```

---

## Generating API Types

The TypeScript types in `frontend/src/types/api.d.ts` are generated from the
Django Ninja OpenAPI schema. After changing the backend API, regenerate them:

```bash
# 1. Run the backend
cd backend && python manage.py runserver

# 2. In another terminal, from the frontend directory:
cd frontend
pnpm generate-types
```

The generated file is committed to the repo so CI doesn't need a running server.

---

## Authentication

The API uses JWT. Obtain tokens:

```bash
curl -X POST http://localhost:8000/api/auth/pair \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

Use the `access` token in the `Authorization: Bearer <token>` header.
Refresh with `/api/auth/refresh`.

On the frontend, call `setAuthToken(token)` from `@/lib/api-client` after login.

---

## Running Tests & Linting

### Backend

```bash
cd backend

# Tests
pytest

# Lint
ruff check .
ruff format --check .

# Type check
mypy .
```

### Frontend

```bash
cd frontend

# Tests
pnpm test

# Lint
pnpm lint

# Type check
pnpm typecheck
```

---

## Project Structure

```
.
├── backend/
│   ├── config/
│   │   ├── api.py              # Main NinjaAPI instance, router registration
│   │   ├── urls.py
│   │   └── settings/
│   │       ├── base.py         # Shared settings
│   │       ├── development.py  # SQLite, DEBUG=True
│   │       └── production.py   # PostgreSQL, DEBUG=False
│   ├── apps/
│   │   └── items/              # Example CRUD domain
│   │       ├── api.py          # Ninja router
│   │       ├── models.py
│   │       ├── schemas.py      # Pydantic in/out schemas
│   │       └── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── pyproject.toml          # ruff + mypy + pytest config
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   ├── lib/
│   │   │   ├── api-client.ts   # openapi-fetch typed client
│   │   │   └── query-client.ts # TanStack Query singleton
│   │   └── types/
│   │       └── api.d.ts        # Generated from OpenAPI schema
│   ├── package.json
│   └── vitest.config.ts
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## Adding a New Domain

1. **Backend**: Create `backend/apps/yourapp/` with `models.py`, `schemas.py`, `api.py`
2. **Register**: Add `api.add_router("/yourapp", your_router)` in `config/api.py`
3. **Migrate**: `python manage.py makemigrations && python manage.py migrate`
4. **Regenerate types**: `pnpm generate-types`
5. **Frontend**: Use `apiClient.GET("/api/yourapp/")` with full type safety
