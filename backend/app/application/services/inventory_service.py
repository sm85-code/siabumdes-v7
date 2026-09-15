"""Inventory business logic using relational models."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models.inventory import Produk, StokKeluar, StokMasuk


class InsufficientStockError(Exception):
    def __init__(self, produk_id: int, available: int, requested: int):
        self.produk_id = produk_id
        self.available = available
        self.requested = requested
        super().__init__(f"Stok tidak cukup untuk produk {produk_id}: tersedia {available}, diminta {requested}")


async def get_produk(session: AsyncSession, produk_id: int) -> Optional[Produk]:
    return await session.get(Produk, produk_id)


async def check_stock(session: AsyncSession, produk_id: int, qty: int) -> int:
    """Return current stock. Raises InsufficientStockError if qty > available."""
    produk = await session.get(Produk, produk_id)
    if not produk:
        raise ValueError(f"Produk {produk_id} tidak ditemukan")
    if produk.stok_saat_ini < qty:
        raise InsufficientStockError(produk_id, produk.stok_saat_ini, qty)
    return produk.stok_saat_ini


async def record_stok_masuk(
    session: AsyncSession,
    *,
    produk_id: int,
    jumlah: int,
    harga_beli_satuan: int,
    unit_id: str = "UU05",
    tanggal: Optional[datetime] = None,
) -> StokMasuk:
    if jumlah <= 0:
        raise ValueError("jumlah harus > 0")
    produk = await session.get(Produk, produk_id)
    if not produk:
        raise ValueError(f"Produk {produk_id} tidak ditemukan")

    total = jumlah * harga_beli_satuan
    row = StokMasuk(
        tanggal=tanggal or datetime.now(timezone.utc),
        produk_id=produk_id,
        jumlah=jumlah,
        harga_beli_satuan=harga_beli_satuan,
        total_biaya=total,
        status_keuangan="belum_sinkron",
        unit_id=unit_id,
    )
    produk.stok_saat_ini += jumlah
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row


async def record_stok_keluar(
    session: AsyncSession,
    *,
    produk_id: int,
    jumlah: int,
    tipe_keluar: str,
    unit_id: str = "UU05",
    keterangan: Optional[str] = None,
    tanggal: Optional[datetime] = None,
    allow_negative: bool = False,
) -> StokKeluar:
    if jumlah <= 0:
        raise ValueError("jumlah harus > 0")
    produk = await session.get(Produk, produk_id)
    if not produk:
        raise ValueError(f"Produk {produk_id} tidak ditemukan")

    if not allow_negative and produk.stok_saat_ini < jumlah:
        raise InsufficientStockError(produk_id, produk.stok_saat_ini, jumlah)

    row = StokKeluar(
        tanggal=tanggal or datetime.now(timezone.utc),
        produk_id=produk_id,
        jumlah=jumlah,
        tipe_keluar=tipe_keluar,
        keterangan=keterangan,
        unit_id=unit_id,
    )
    produk.stok_saat_ini -= jumlah
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row


async def list_low_stock(session: AsyncSession, threshold: int = 5, unit_id: Optional[str] = None) -> list[Produk]:
    stmt = select(Produk).where(Produk.stok_saat_ini <= threshold)
    if unit_id:
        stmt = stmt.where(Produk.unit_id == unit_id)
    return list((await session.execute(stmt)).scalars().all())
