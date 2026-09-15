"""Thin finance router – delegates to finance_service."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.finance_service import calc_balances, close_period, list_closed_periods
from app.core.dependencies import get_db
from app.presentation.api.v1.schemas.finance import (
    BalanceItem,
    BalanceResponse,
    ClosePeriodRequest,
    ClosePeriodResponse,
)

router = APIRouter(prefix="/api/v1/accounts", tags=["Accounts"])


@router.get("/balances", response_model=BalanceResponse)
async def get_balances(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    unit_usaha_id: Optional[str] = Query(None),
    group: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    bal, _ = await calc_balances(session, start_date, end_date, unit_usaha_id, group)
    items = [
        BalanceItem(code=code, debit=v["debit"], credit=v["credit"], saldo=v["saldo"])
        for code, v in sorted(bal.items())
    ]
    return BalanceResponse(
        balances=items,
        group=group,
        unit_usaha_id=unit_usaha_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.post("/close-period", response_model=ClosePeriodResponse)
async def close_accounting_period(
    body: ClosePeriodRequest,
    session: AsyncSession = Depends(get_db),
):
    row = await close_period(session, body.group, body.period)
    return ClosePeriodResponse(id=row.id, group=row.group, period=row.period)


@router.get("/closed-periods", response_model=list[str])
async def get_closed_periods(
    group: str = Query(...),
    session: AsyncSession = Depends(get_db),
):
    return await list_closed_periods(session, group)
