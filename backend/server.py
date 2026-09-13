"""BUMDES API application entrypoint. Route implementations live in routers/."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from collections import defaultdict, deque
from time import monotonic
import logging
from config import APP_TITLE, CORS_ORIGINS

logger = logging.getLogger("bumdes.audit")
from database import close_database, engine, init_database
from sqlalchemy import text
from startup import seed_startup as seed_database

app = FastAPI(title=APP_TITLE)
_login_attempts = defaultdict(deque)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-CSRF-Token"],
)


@app.middleware("http")
async def validate_csrf_origin(request: Request, call_next):
    """Reject cross-site state-changing requests before they reach a router."""
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if request.url.path.endswith("/auth/login"):
            now = monotonic()
            attempts = _login_attempts[request.client.host if request.client else "unknown"]
            while attempts and now - attempts[0] > 60:
                attempts.popleft()
            if len(attempts) >= 10:
                return JSONResponse(status_code=429, content={"detail": "Terlalu banyak percobaan login"})
            attempts.append(now)
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")
        source = origin or (referer and "/".join(referer.split("/")[:3]))
        if source and source not in CORS_ORIGINS:
            return JSONResponse(status_code=403, content={"detail": "Permintaan lintas situs ditolak"})
    response = await call_next(request)
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        logger.info("mutation method=%s path=%s status=%s", request.method, request.url.path, response.status_code)
    return response


@app.on_event("startup")
async def seed_startup():
    await init_database()
    await seed_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_database()


from routers import auth_admin, master_data_router, transactions_router, reports_router  # noqa: E402

for router_module in (auth_admin, master_data_router, transactions_router, reports_router):
    app.include_router(router_module.router)

@app.get("/")
async def root():
    return {"app": "BUMDES Karya Raharja", "version": "1.0.0"}


@app.get("/health")
async def health():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "degraded", "database": "unavailable"})
    return {"status": "ok", "database": "connected"}
