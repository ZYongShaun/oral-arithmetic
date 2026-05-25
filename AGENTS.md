# AGENTS.md

## Project Overview

小学一年级口算练习应用 (Primary Grade 1 Oral Arithmetic) — Duolingo-style gamified math practice.

**Stack:** Python/FastAPI backend + Vue 3/Vite frontends (user H5 + admin PC) + MySQL 8.0.

## Directory Map

```
backend/               FastAPI backend (port 8000)
  app/
    main.py            App entry point, CORS, root routes
    core/              config.py, database.py, security.py
    models/            SQLAlchemy ORM models (14 tables)
    schemas/           Pydantic request/response schemas
    services/          Business logic layer
    api/               Route handlers (one file per domain)
frontend-user/         Vue 3 mobile H5 (port 3000)
  src/
    router/index.js    Routes + auth guard
    utils/request.js   Axios instance + interceptors
    stores/            Pinia stores
    apis/              API call functions
    api/               Older API module (object literal style) — prefer apis/
    views/             Page components (.vue)
    components/        Shared components (.vue)
frontend-admin/        Vue 3 PC admin (port 3001, no vite.config.js yet)
docs/database.sql      Full DDL with seed data
scripts/setup.sh       One-time project init script
openspec/              Spec-driven development config
```

## Build / Run / Test Commands

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend user (runs on :3000, proxies /api → :8000)
cd frontend-user
npm run dev

# Frontend admin (runs on :3001, hardcoded baseURL to localhost:8000)
cd frontend-admin
npm run dev

# Production build
cd frontend-user && npm run build

# Docker
docker compose -f docker-compose.dev.yml up
docker compose up

# Install deps (first time)
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd frontend-user && npm install
cd frontend-admin && npm install

# DB setup (no migration framework yet — run DDL directly)
mysql -u root -p < docs/database.sql
```

**Testing:** No automated tests exist. Manual testing via Swagger UI at http://localhost:8000/docs.

**Linting:** No ESLint, Prettier, or ruff configs exist. When adding tooling, configure as needed — there are no prior conventions.

## Code Style

### Python (Backend)

**Imports** — 3 groups, blank line between: standard library → third-party → local (`app.*`). Alphabetical within each group. Use `from X import Y`, not bare `import X` except for `import re`:

```python
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
```

Inline/late imports (inside function bodies) are used selectively to avoid circular imports, e.g. `from app.models.child import Child` inside a route function in `api/auth.py:127`.

**Naming:** `snake_case` for functions/variables, `PascalCase` for classes. Modules are `snake_case.py`.

**Type hints** — required on all service-layer functions and dependencies. Route handlers may omit return type annotations (they use `response_model` in the decorator instead).

**Docstrings** — Chinese language, triple quotes. Required on all model classes, schema classes, and non-trivial service functions. Optional on simple route handlers.

**Error handling** — Use `HTTPException` with `status.HTTP_4XX` and a descriptive `detail` string:

```python
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username or phone already registered"
)
```

Wrap third-party calls (sqlalchemy `IntegrityError`, `jose.JWTError`) in `try/except` and re-raise as `HTTPException`. No custom exception classes. No exception logging.

**Routes** — All route handlers are `def` (sync, not `async def`). Router variable is always `router`. Always set `prefix` and `tags`. Paths use hyphens (`/quick-login`), no trailing slashes:

```python
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    ...
    return {"access_token": ..., "token_type": "bearer"}
```

Routes return plain dicts, not Pydantic model instances.

**SQLAlchemy models** — All models extend `Base` from `database.py`. Table name is lowercase plural. PK is `Integer, primary_key=True, autoincrement=True`. Use `relationship(back_populates=...)` (never `backref`). Cascade: `"all, delete-orphan"` for child collections. Use `comment=` for Chinese column descriptions:

```python
class Practice(Base):
    """练习记录表"""
    __tablename__ = "practices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    level = Column(Integer, nullable=False, comment="难度等级")
    child = relationship("Child", back_populates="practices")
```

**Pydantic schemas** — All extend `BaseModel`. Request: `<Action>Request`, Response: `<Resource>Response`, Update: `<Resource>Update`. Validators use `@validator('fieldname')` (Pydantic v1 style, use `@field_validator` for v2+):

```python
class Config:
    from_attributes = True  # only on response-mapped schemas
```

### JavaScript / Vue (Frontend)

**Imports** — Order: Vue/core libs → Element Plus → CSS → project modules. Use `@/` alias (resolves to `src/`), configured in `vite.config.js`:

```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
```

**Naming:** `camelCase` for JS functions/variables/files (e.g. `dailyTasks.js`, `useUserStore`). `PascalCase` for Vue component files (e.g. `Login.vue`, `Practice.vue`). Strings: single quotes.

**Vue components** — Always use `<script setup>` (Composition API). Never use Options API. Use `ref()` for primitives, `computed()` for derived values. Pages are in `views/`, shared components in `components/`:

```vue
<script setup>
import { ref, onMounted } from 'vue'
const loading = ref(false)
</script>
```

**Pinia stores** — Use **Options Store** style (matching `frontend-user/src/stores/`):

```js
import { defineStore } from 'pinia'
export const useUserStore = defineStore('user', {
  state: () => ({ token: '', userInfo: {} }),
  getters: { isLoggedIn: (state) => !!state.token },
  actions: { setToken(token) { this.token = token } }
})
```

The admin frontend's Setup Store style (`defineStore('name', () => { ... })`) is legacy and should be migrated to Options Store style when touching those files.

**API modules** — Prefer the named-function style from `apis/` (not the object-literal style from `api/`). Use `request.post(url, data)` shorthand:

```js
import request from '@/utils/request'
export function getRandomQuestions(data) {
  return request({ url: '/questions/random', method: 'post', data })
}
```

The duplicate `api/` and `apis/` directories in `frontend-user` are legacy — prefer `apis/`.

**Axios** — The `utils/request.js` interceptor unboxes `response.data` automatically, so API callers receive the payload directly. The request interceptor attaches `Bearer` token from `localStorage.getItem('access_token')`. On 401, it clears storage and redirects to `/login`.

**Routes** — All components are lazy-loaded via `() => import(...)`. Protected routes use `meta: { requiresAuth: true }`. Router guards check auth before each navigation.

**Element Plus** — Fully registered (not on-demand). Icons are globally registered via `for...in Object.entries(ElementPlusIconsVue)`. Use kebab-case in templates: `<el-icon><User /></el-icon>`. Notifications via `ElMessage.error()` / `ElMessage.success()`.

**CSS** — `<style scoped>` by default. Global resets in `App.vue` without `scoped`. SCSS (`lang="scss"`) is supported via `sass-embedded` but rarely used. Colors are hardcoded hex values. Brand gradient: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`. Mobile-first with max-width 750px.

## Backend Architecture

**Layer order for new features:** models → schemas → services → api routes.

Every new domain follows this pattern:
1. `models/x.py` — SQLAlchemy table definition
2. `schemas/x.py` — Pydantic request/response shapes
3. `services/x_service.py` — Business logic (pure functions, `db: Session` as first param)
4. `api/x.py` — Route handlers, wire Dependencies, call services

**Key patterns:**
- DB session via `Depends(get_db)` in every route
- Auth via `Depends(get_current_user)` (returns `User` model instance)
- Config via `settings = Settings()` singleton from `app.core.config`
- User-facing strings are in Chinese

## Environment

- Backend env: `backend/.env` (copy from `.env.example`)
- Frontend env vars: `import.meta.env.VITE_API_BASE_URL`
- Default admin: `admin` / `admin123`
- JWT: HS256, configured with 2-year expiry for home LAN convenience
- MySQL: database name `oral_arithmetic`, charset `utf8mb4`

## Git

`.gitignore` covers IDE files, logs, builds, and `.DS_Store`. No pre-commit hooks configured. Commit messages are in Chinese or English — no enforced convention.
