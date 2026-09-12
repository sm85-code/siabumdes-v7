"""BUMDES API application entrypoint. Route implementations live in routers/."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import APP_TITLE, CORS_ORIGINS
from services.mongodb_service import client
from startup import seed_startup as seed_database

app = FastAPI(title=APP_TITLE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-CSRF-Token"],
)


@app.on_event("startup")
async def seed_startup():
    await seed_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


from routers import auth_admin, master_data_router, transactions_router, reports_router  # noqa: E402

for router_module in (auth_admin, master_data_router, transactions_router, reports_router):
    app.include_router(router_module.router)

@app.get("/")
async def root():
    return {"app": "BUMDES Karya Raharja", "version": "1.0.0"}
