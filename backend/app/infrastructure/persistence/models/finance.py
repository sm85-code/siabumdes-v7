"""Relational finance models (Account + double-entry Transaction).

Preserves original calculation semantics:
- saldo = debit - credit  if normal_balance == 'debit'
- saldo = credit - debit  if normal_balance == 'kredit'
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Account(Base):
    """Chart of Accounts."""
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("code", "group", name="uq_account_code_group"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)  # aset | kewajiban | ekuitas | pendapatan | beban
    subcategory: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    normal_balance: Mapped[str] = mapped_column(String(16), nullable=False)  # debit | kredit
    parent_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    group: Mapped[str] = mapped_column(String(32), nullable=False, default="BUMDES", index=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)


class Transaction(Base):
    """Double-entry journal transaction (one debit + one credit)."""
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    unit_usaha_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    transaction_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
    debit_account_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    credit_account_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    mitra_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    reference: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    created_by: Mapped[str] = mapped_column(String(36), nullable=False)
    is_closing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)


class ClosedPeriod(Base):
    """Closed accounting periods (used by laba-rugi filter)."""
    __tablename__ = "closed_periods"
    __table_args__ = (UniqueConstraint("group", "period", name="uq_closed_period_group"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    group: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    period: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM
    closed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    closed_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
