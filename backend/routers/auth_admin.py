"""Compatibility aggregator for authentication routes."""
from fastapi import APIRouter
from routers.auth import session, profile, admin_users, gdrive

router = APIRouter()
for module in (session, profile, admin_users, gdrive):
    router.include_router(module.router)
