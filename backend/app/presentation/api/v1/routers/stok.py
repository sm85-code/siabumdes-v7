"""Thin inventory router – delegates to inventory_service."""
from __future__ import annotations

from datetime import datetime, time, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.inventory_service import (
    InsufficientStockError,
    record_stok_keluar,
    record_stok_masuk,
)
from app.core.dependencies import get_db
from app.infrastructure.persistence.models.inventory import Produk
from app.presentation.api.v1.schemas.inventory import (
    ProdukCreate,
    ProdukOut,
    StokKeluarCreate,
    StokMasukCreate,
    StokMutasiOut,
)

router = APIRouter(prefix="/api/v1/stok", tags=["Stok"])
UNIT_ID = "UU05"


@router.post("/produk", response_model=ProdukOut, status_code=status.HTTP_201_CREATED)
async def buat_produk(data: ProdukCreate, session: AsyncSession = Depends(get_db)):
    exists = await session.scalar(select(Produk).where(Produk.sku == data.sku, Produk.unit_id == UNIT_ID))
    if exists:
        raise HTTPException(status_code=409, detail="SKU sudah digunakan")
    item = Produk(**data.model_dump(), unit_id=UNIT_ID)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.get("/produk", response_model=list[ProdukOut])
async def daftar_produk(session: AsyncSession = Depends(get_db)):
    rows = (await session.scalars(select(Produk).where(Produk.unit_id == UNIT_ID).order_by(Produk.nama_produk))).all()
    return list(rows)


@router.post("/masuk", response_model=StokMutasiOut, status_code=status.HTTP_201_CREATED)
async def catat_stok_masuk(data: StokMasukCreate, session: AsyncSession = Depends(get_db)):
    try:
        row = await record_stok_masuk(
            session,
            produk_id=data.produk_id,
            jumlah=data.jumlah,
            harga_beli_satuan=data.harga_beli_satuan,
            unit_id=UNIT_ID,
            tanggal=datetime.combine(data.tanggal, time.min, tzinfo=timezone.utc),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return StokMutasiOut(id=row.id, pesan="Stok masuk berhasil dicatat", total_biaya=row.total_biaya)


@router.post("/keluar", response_model=StokMutasiOut, status_code=status.HTTP_201_CREATED)
async def catat_stok_keluar(data: StokKeluarCreate, session: AsyncSession = Depends(get_db)):
    try:
        row = await record_stok_keluar(
            session,
            produk_id=data.produk_id,
            jumlah=data.jumlah,
            tipe_keluar=data.tipe_keluar,
            unit_id=UNIT_ID,
            keterangan=data.keterangan,
            tanggal=datetime.combine(data.tanggal, time.min, tzinfo=timezone.utc),
        )
    except InsufficientStockError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    produk = await session.get(Produk, data.produk_id)
    return StokMutasiOut(id=row.id, pesan="Stok keluar berhasil dicatat", stok_saat_ini=produk.stok_saat_ini if produk else None)
