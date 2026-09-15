"""Finance business logic using relational models."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models.finance import Account, ClosedPeriod, Transaction


def _to_amount(value) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def _saldo(debit: Decimal, credit: Decimal, normal_balance: str) -> Decimal:
    if normal_balance == "debit":
        return debit - credit
    return credit - debit


async def get_accounts_map(session: AsyncSession, group: Optional[str] = None) -> dict[str, Account]:
    stmt = select(Account).where(Account.active.is_(True))
    if group:
        stmt = stmt.where(Account.group == group)
    rows = (await session.execute(stmt)).scalars().all()
    return {a.code: a for a in rows}


async def calc_balances(
    session: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    unit_usaha_id: Optional[str] = None,
    group: Optional[str] = None,
) -> tuple[dict[str, dict], dict[str, Account]]:
    """Return {code: {debit, credit, saldo}} + accounts map.

    Same semantics as legacy _calc_balances.
    """
    conditions = [Transaction.unit_usaha_id == unit_usaha_id]
    if start_date and end_date:
        conditions.append(Transaction.date >= start_date)
        conditions.append(Transaction.date <= end_date)
    elif end_date:
        conditions.append(Transaction.date <= end_date)

    txs = (await session.execute(select(Transaction).where(and_(*conditions)))).scalars().all()
    bal: dict[str, dict] = {}
    for tx in txs:
        amt = _to_amount(tx.amount)
        bal.setdefault(tx.debit_account_code, {"debit": Decimal("0"), "credit": Decimal("0")})
        bal.setdefault(tx.credit_account_code, {"debit": Decimal("0"), "credit": Decimal("0")})
        bal[tx.debit_account_code]["debit"] += amt
        bal[tx.credit_account_code]["credit"] += amt

    accounts = await get_accounts_map(session, group)
    for code, v in bal.items():
        acc = accounts.get(code)
        nb = acc.normal_balance if acc else "debit"
        v["saldo"] = _saldo(v["debit"], v["credit"], nb)
    return bal, accounts


async def calc_balances_before(
    session: AsyncSession,
    before_date: str,
    unit_usaha_id: Optional[str] = None,
    group: Optional[str] = None,
) -> tuple[dict[str, dict], dict[str, Account]]:
    conditions = [
        Transaction.date < before_date,
        Transaction.unit_usaha_id == unit_usaha_id,
    ]
    txs = (await session.execute(select(Transaction).where(and_(*conditions)))).scalars().all()
    bal: dict[str, dict] = {}
    for tx in txs:
        amt = _to_amount(tx.amount)
        bal.setdefault(tx.debit_account_code, {"debit": Decimal("0"), "credit": Decimal("0")})
        bal.setdefault(tx.credit_account_code, {"debit": Decimal("0"), "credit": Decimal("0")})
        bal[tx.debit_account_code]["debit"] += amt
        bal[tx.credit_account_code]["credit"] += amt

    accounts = await get_accounts_map(session, group)
    for code, v in bal.items():
        acc = accounts.get(code)
        nb = acc.normal_balance if acc else "debit"
        v["saldo"] = _saldo(v["debit"], v["credit"], nb)
    return bal, accounts


async def close_period(
    session: AsyncSession,
    group: str,
    period: str,
    closed_by: Optional[str] = None,
) -> ClosedPeriod:
    """Mark an accounting period as closed (YYYY-MM)."""
    existing = await session.scalar(
        select(ClosedPeriod).where(ClosedPeriod.group == group, ClosedPeriod.period == period)
    )
    if existing:
        return existing
    row = ClosedPeriod(
        id=str(uuid4()),
        group=group,
        period=period,
        closed_at=datetime.now(timezone.utc),
        closed_by=closed_by,
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row


async def is_period_closed(session: AsyncSession, group: str, period: str) -> bool:
    row = await session.scalar(
        select(ClosedPeriod.id).where(ClosedPeriod.group == group, ClosedPeriod.period == period)
    )
    return row is not None


async def list_closed_periods(session: AsyncSession, group: str) -> list[str]:
    rows = (
        await session.execute(select(ClosedPeriod.period).where(ClosedPeriod.group == group))
    ).scalars().all()
    return list(rows)
