from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class BalanceItem(BaseModel):
    code: str
    debit: Decimal
    credit: Decimal
    saldo: Decimal


class BalanceResponse(BaseModel):
    balances: list[BalanceItem]
    group: Optional[str] = None
    unit_usaha_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ClosePeriodRequest(BaseModel):
    group: str = Field(min_length=1, max_length=32)
    period: str = Field(pattern=r"^\d{4}-\d{2}$")  # YYYY-MM


class ClosePeriodResponse(BaseModel):
    id: str
    group: str
    period: str
    closed: bool = True
