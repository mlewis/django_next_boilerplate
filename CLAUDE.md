# CLAUDE.md — AI Assistant Guide for Django + Next.js Boilerplate

This file provides context for AI assistants working in this repository. Read it
before making any changes.

---

## Project Overview

A full-stack hackathon boilerplate wiring together a Django (Ninja) API backend
and a Next.js 14 (App Router) frontend with end-to-end TypeScript type safety.

| Layer | Stack |
|-------|-------|
| Backend API | Django 5.2 + Django Ninja 1.6 |
| Authentication | JWT (django-ninja-jwt) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Next.js 14 App Router + TypeScript 5 |
| UI Library | Mantine UI v8 |
| Data Fetching | TanStack Query v5 + openapi-fetch |
| API Types | openapi-typescript (auto-generated from Django Ninja) |
| Backend Lint/Format | ruff |
| Backend Type Check | mypy (strict mode) |
| Backend Tests | pytest-django + Factory Boy |
| Frontend Lint | ESLint + TypeScript-ESLint |
| Frontend Type Check | tsc |
| Frontend Tests | Vitest + React Testing Library |
| CI | GitHub Actions |
| Containers | Docker + docker-compose |

---

## Repository Layout

```
.
├── backend/
│   ├── config/
│   │   ├── api.py              # NinjaAPI instance + router registration
│   │   ├── urls.py             # Root URL config (mounts /api/)
│   │   └── settings/
│   │       ├── base.py         # Shared settings (JWT, middleware, apps)
│   │       ├── development.py  # SQLite, DEBUG=True, CORS localhost:3000
│   │       └── production.py   # PostgreSQL, DEBUG=False, SSL, HSTS
│   ├── apps/
│   │   └── items/              # Example CRUD domain — use as a template
│   │       ├── models.py
│   │       ├── schemas.py      # Pydantic in/out schemas for Ninja
│   │       ├── api.py          # Ninja router with 5 endpoints
│   │       └── tests/
│   │           ├── factories.py
│   │           └── test_api.py
│   ├── manage.py
│   ├── requirements.txt        # Production deps
│   ├── requirements-dev.txt    # Dev/test deps (includes prod)
│   ├── pyproject.toml          # ruff, mypy, pytest config
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx      # Root layout: MantineProvider + Providers
│   │   │   ├── providers.tsx   # QueryClientProvider + DevTools
│   │   │   ├── page.tsx        # Home page — items list example
│   │   │   └── globals.css     # @import "@mantine/core/styles.css"
│   │   ├── lib/
│   │   │   ├── api-client.ts   # openapi-fetch typed client + setAuthToken()
│   │   │   └── query-client.ts # TanStack Query singleton (staleTime 60s)
│   │   └── types/
│   │       └── api.d.ts        # AUTO-GENERATED — do not edit by hand
│   ├── package.json
│   ├── tsconfig.json           # strict, paths: @/* → ./src/*
│   ├── next.config.mjs         # Rewrites /api/* → Django backend
│   ├── vitest.config.ts
│   ├── postcss.config.mjs      # postcss-preset-mantine + autoprefixer
│   ├── .eslintrc.json
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml          # db + backend + frontend services
├── .github/workflows/ci.yml   # Backend + frontend CI jobs
└── README.md
```

---

## Development Commands

### Docker (recommended for full stack)

```bash
# Start all services (db, backend, frontend)
docker-compose up --build

# Create Django superuser
docker-compose exec backend python manage.py createsuperuser
```

Service URLs:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/api/docs
- Django Admin: http://localhost:8000/admin/

---

### Backend (manual)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # edit SECRET_KEY at minimum

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Tests**
```bash
pytest                        # run all tests
pytest --tb=short -q          # compact output (matches CI)
```

**Lint & Format**
```bash
ruff check .                  # lint
ruff format --check .         # format check (use `ruff format .` to fix)
```

**Type Check**
```bash
mypy .
```

---

### Frontend (manual)

```bash
cd frontend
pnpm install
cp .env.example .env.local    # set NEXT_PUBLIC_API_URL=http://localhost:8000

pnpm dev                      # dev server on :3000
```

**Tests**
```bash
pnpm test                     # run once
pnpm test:watch               # watch mode
```

**Lint**
```bash
pnpm lint
```

**Type Check**
```bash
pnpm typecheck
```

---

### Regenerating API Types

After any backend API change, regenerate TypeScript types:

```bash
# Terminal 1 — backend must be running
cd backend && python manage.py runserver

# Terminal 2
cd frontend && pnpm generate-types
```

`src/types/api.d.ts` is committed so CI does not need a running server. Always
regenerate and commit it whenever endpoints or schemas change.

---

## Key Conventions

### Backend

**App structure** — follow the `items` app as the canonical template:
- `models.py` — Django ORM models
- `schemas.py` — Pydantic schemas (`*In` for input, `*Out` for output)
- `api.py` — `ninja.Router` with route handlers
- `tests/factories.py` — Factory Boy factories
- `tests/test_api.py` — pytest-django tests

**Registering a new app:**
1. Create `backend/apps/yourapp/` following the template above
2. Add `"apps.yourapp"` to `INSTALLED_APPS` in `config/settings/base.py`
3. Add `api.add_router("/yourapp", your_router)` in `config/api.py`
4. Run `python manage.py makemigrations && python manage.py migrate`
5. Regenerate frontend types: `pnpm generate-types`

**Authentication** — use `from ninja_jwt.authentication import JWTAuth` on
protected endpoints. Public endpoints omit `auth=JWTAuth()`.

**Settings** — never import from settings directly. Always use
`from django.conf import settings`. The active settings module is chosen via
`DJANGO_SETTINGS_MODULE` in `.env`.

**Schemas** — Ninja uses Pydantic v2. Input schemas are `ItemIn`, output schemas
are `ItemOut`. Always define explicit output schemas; never return raw ORM objects.

**Code style** — ruff enforces E, F, I (isort), N (naming), UP (pyupgrades).
Line length 88. `from __future__ import annotations` is preferred.

**mypy** — strict mode is enabled. Annotate all function arguments and return
types. Do not use `type: ignore` without a comment explaining why.

**Tests** — use `@pytest.fixture` and Factory Boy. Use `client.get(...)` with
`content_type="application/json"`. Auth headers:
```python
headers = {"Authorization": f"Bearer {access_token}"}
```

---

### Frontend

**API calls** — always use the typed `apiClient` from `@/lib/api-client`:
```typescript
const { data } = await apiClient.GET("/api/items/")
const { data } = await apiClient.POST("/api/items/", { body: { title: "foo" } })
```
Paths and request/response shapes are fully typed via `src/types/api.d.ts`.

**Authentication** — after a successful login, call `setAuthToken(token)` from
`@/lib/api-client`. This attaches `Authorization: Bearer <token>` to all
subsequent requests.

**Data fetching** — wrap all server-state fetches in `useQuery` / `useMutation`
from TanStack Query. Do not fetch in `useEffect`.

**UI components** — use Mantine v8 components exclusively. Do not install
Tailwind, shadcn/ui, or other component libraries alongside Mantine.

**Path alias** — `@/` maps to `src/`. Always use the alias in imports.

**Routing** — this project uses the Next.js 14 App Router. Place pages in
`src/app/`. Use `layout.tsx` for shared layouts and `page.tsx` for routes.

**API proxy** — `next.config.mjs` rewrites `/api/*` to the Django backend, so
client-side fetches can use `/api/...` directly (no CORS issues). The
`api-client.ts` handles the SSR vs CSR base URL distinction automatically.

**Tests** — write tests in Vitest + React Testing Library. Colocate test files
under `src/lib/__tests__/` or alongside components. Mock `openapi-fetch` for
unit tests.

**TypeScript** — strict mode. No `any`. Use generated types from `api.d.ts` for
all API payloads.

---

## API Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/pair` | Obtain access + refresh tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| POST | `/api/auth/verify` | Verify token validity |

```bash
# Get tokens
curl -X POST http://localhost:8000/api/auth/pair \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Items (example domain)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/items/` | Required | List current user's items |
| POST | `/api/items/` | Required | Create item (returns 201) |
| GET | `/api/items/{id}` | None | Get single item |
| PATCH | `/api/items/{id}` | Required, owner | Update item |
| DELETE | `/api/items/{id}` | Required, owner | Delete item |

### Schema endpoints
- `GET /api/docs` — Swagger UI
- `GET /api/openapi.json` — OpenAPI 3.0 schema

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | *(required)* | Django secret key |
| `DJANGO_SETTINGS_MODULE` | `config.settings.development` | Settings module |
| `DJANGO_DEBUG` | `True` | Debug mode |
| `DATABASE_URL` | — | PostgreSQL URL (production only) |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |
| `ALLOWED_HOSTS` | — | Comma-separated allowed hosts (production) |

### Frontend (`frontend/.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Django API base URL |

---

## CI/CD

`.github/workflows/ci.yml` runs on every push and pull request.

**Backend job** (Python 3.12):
1. `pip install -r requirements-dev.txt`
2. `ruff check .`
3. `ruff format --check .`
4. `mypy .`
5. `pytest --tb=short -q`

**Frontend job** (Node 20, pnpm 9):
1. `pnpm install --frozen-lockfile`
2. `pnpm lint`
3. `pnpm typecheck`
4. `pnpm test`

All four checks (lint, format, type-check, tests) must pass before merging.

---

## Docker Architecture

```
┌─────────────────────────────────────┐
│ docker-compose                      │
│                                     │
│  ┌──────────┐   ┌────────────────┐  │
│  │ frontend │──▶│    backend     │  │
│  │ :3000    │   │    :8000       │  │
│  └──────────┘   └───────┬────────┘  │
│                         │           │
│                  ┌──────▼────────┐  │
│                  │  db (pg 16)   │  │
│                  │  :5432        │  │
│                  └───────────────┘  │
└─────────────────────────────────────┘
```

- Frontend rewrites `/api/*` to backend (avoids browser CORS)
- Backend connects to db via `DATABASE_URL`
- Live-reload via Docker volumes (backend and frontend source mounted)
- Backend waits for db healthcheck before starting

---

## Common Gotchas

1. **`api.d.ts` is stale** — if TypeScript complains about unknown endpoints or
   wrong types, regenerate: `pnpm generate-types` (backend must be running).

2. **Missing migrations** — after editing any model, always run
   `python manage.py makemigrations` and commit the migration file.

3. **JWT expiry** — access tokens expire in 60 minutes; refresh tokens in 7 days.
   Call `/api/auth/refresh` with the refresh token to get a new access token.

4. **CORS in development** — the frontend dev server proxies `/api/*` to the
   backend, so no CORS headers are needed for browser requests. Direct
   browser-to-backend calls (e.g. from Postman) are allowed from
   `http://localhost:3000` and `http://127.0.0.1:3000`.

5. **Settings module** — `manage.py` loads `.env` automatically. Make sure
   `DJANGO_SETTINGS_MODULE` is set correctly; production should always use
   `config.settings.production`.

6. **pnpm only** — the frontend Dockerfile and CI use pnpm. Do not add a
   `package-lock.json` or `yarn.lock`.

7. **Mantine PostCSS** — Mantine requires `postcss-preset-mantine`. Do not
   remove `postcss.config.mjs` or the Mantine styles import in `globals.css`.
