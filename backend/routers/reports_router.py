"""Compatibility aggregator for modular routes."""
from fastapi import APIRouter, Depends
from config import API_PREFIX
from dependencies import require_password_ready
from routers.reports import public_dashboard
from routers.reports import periods
from routers.reports import financial
from routers.reports import exports
from routers.reports import pdf

router = APIRouter(prefix=API_PREFIX)
router.include_router(public_dashboard.router, dependencies=[Depends(require_password_ready)])
router.include_router(periods.router, dependencies=[Depends(require_password_ready)])
router.include_router(financial.router, dependencies=[Depends(require_password_ready)])
router.include_router(exports.router, dependencies=[Depends(require_password_ready)])
router.include_router(pdf.router, dependencies=[Depends(require_password_ready)])
