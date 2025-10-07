# Kenkeputa Micro-Commerce

Kenkeputa Micro-Commerce is a full-stack sample commerce platform composed of a FastAPI backend and an Expo/React Native client. It illustrates authentication, role-based authorization, product catalog management, and cart workflows leveraging a RESTful API.

## Project Structure

```
├── client/                # Expo mobile client
│   ├── app/               # Screens and navigation routes
│   ├── services/          # API client ([client/services/api.ts](client/services/api.ts))
│   └── utils/             # Async storage helpers ([client/utils/storage.ts](client/utils/storage.ts))
└── server/                # FastAPI backend
    ├── app/api            # Routers, services, repositories
    │   ├── v1/auth        # Auth endpoints and schemas
    │   ├── v1/products    # Product endpoints ([server/app/api/v1/products/routes.py](server/app/api/v1/products/routes.py))
    │   └── services       # Business logic such as [`app.api.services.product.ProductService`](server/app/api/services/product.py)
    ├── app/core           # Config, dependencies, base classes
    ├── app/utils          # Helpers (JWT, logging, password hashing)
    ├── scripts/           # Utilities (admin creation)
    └── tests/             # Pytest suites
```

## Features

- User registration and login with JWT tokens via [`app.api.v1.auth.routes`](server/app/api/v1/auth/routes.py).
- Admin-only product CRUD powered by [`app.api.services.product.ProductService`](server/app/api/services/product.py).
- Cart management for regular users with relational integrity enforced in Alembic migrations.
- Centralized logging configured by [`app.utils.logger`](server/app/utils/logger.py) with rotating file handlers.
- Expo client implementing authentication, product catalog, cart, and profile flows (see [client/app](client/app)).

## Prerequisites

| Tool | Version |
| --- | --- |
| Python | 3.12+ |
| Poetry | 1.8+ |
| PostgreSQL | 14+ |
| Node.js | 18 LTS |
| Expo CLI | Latest |

## Backend Setup

1. **Install dependencies**
   ```bash
   cd server
   poetry install --with dev
   ```

2. **Environment variables**

   Duplicate the provided sample:
   ```bash
   cp .env.sample .env
   ```

   Required fields match [`app.core.config.Settings`](server/app/core/config.py):

   | Variable | Description |
   | --- | --- |
   | `SECRET_KEY` | Application secret for JWT signing |
   | `ALGORITHM` | JWT algorithm (e.g. `HS256`) |
   | `ACCESS_TOKEN_EXPIRY` | Access token TTL in hours |
   | `REFRESH_TOKEN_EXPIRY` | Refresh token TTL in hours |
   | `DATABASE_TYPE` | e.g. `postgresql` |
   | `DATABASE_HOST` | Database host |
   | `DATABASE_PORT` | Database port |
   | `DATABASE_USER` | Database username |
   | `DATABASE_PASSWORD` | Database password |
   | `DATABASE_NAME` | Target database |

3. **Create the database**

   ```bash
   sudo -u <postgres_user> psql
   CREATE DATABASE kenkeputa_micro_commerce;
   ```

4. **Apply migrations**

   ```bash
   poetry run alembic upgrade head
   ```

5. **Run the API**

   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   API documentation becomes available at:
   - Swagger UI: `http://localhost:8000/v1/docs`
   - ReDoc: `http://localhost:8000/v1/redoc`

6. **Seed an administrator**

   Use the provided script ([server/scripts/create_admin.py](server/scripts/create_admin.py)):
   ```bash
   poetry run python scripts/create_admin.py --email admin@example.com --password "StrongPass123!"
   ```

   Re-running with the same email promotes an existing user and optionally resets the password.

7. **Run automated checks**

   ```bash
   poetry run ruff check app tests
   poetry run pytest -v --disable-warnings
   ```

   Tests rely on the fixtures in [`server/tests/conftest.py`](server/tests/conftest.py), which bootstrap an in-memory SQLite instance.

## Frontend Setup

1. **Install dependencies**
   ```bash
   cd client
   npm install
   ```

2. **Configure API base URL**

   Update `API_BASE_URL` in [client/services/api.ts](client/services/api.ts) to point at your running FastAPI server (e.g. `http://localhost:8000`).  
   When testing with Expo Go on a physical device, replace `localhost` with your computer’s LAN IP address shown in the Expo CLI URLs.

3. **Launch the Expo app**
   ```bash
   npx expo start
   ```

   - Press `i` for iOS simulator, `a` for Android emulator, or scan the QR code with Expo Go.
   - The authentication flow persists tokens using [`storage`](client/utils/storage.ts), so remember to clear AsyncStorage when switching accounts.

## Typical Development Flow

1. Start the backend with Uvicorn.
2. Start the Expo development server.
3. Register a new account through the client or API.
4. Promote the user to admin via the admin script if product management is needed.
5. Access protected product endpoints with the admin token; cart endpoints remain accessible to standard users.

## Logging & Monitoring

- Application logs are written to the `/logs` directory configured in [`app.utils.logger`](server/app/utils/logger.py).
- Console logs mirror file output at `INFO` level for quick inspection.

## Useful Commands

| Task | Command |
| --- | --- |
| Format / lint backend | `poetry run ruff check app tests --fix` |
| Run backend tests | `poetry run pytest` |
| Generate new migration | `poetry run alembic revision --autogenerate -m "message"` |
| Downgrade last migration | `poetry run alembic downgrade -1` |
| Clear Expo cache | `npx expo start -c` |

## Troubleshooting

- **JWT validation errors**: Ensure your client sends the `Authorization: Bearer <token>` header. The dependency [`app.core.dependencies.security.get_current_user`](server/app/core/dependencies/security.py) enforces this.
- **Admin-only routes return 403**: Verify the user has `role="admin"` in the database or rerun the admin script.
- **Database connectivity**: Confirm the `.env` values reflect your local PostgreSQL credentials and that the database server is running.

Happy hacking!
