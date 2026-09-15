"""Endpoint inventory Unit Toko Offline (UU05).

Router ini menggunakan Async SQLAlchemy dan transaksi database atomik. Data
keuangan mingguan ditulis ke application_entities dengan bentuk yang sama
seperti koleksi transactions lama, sehingga tidak mengubah tabel keuangan inti.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import SessionLocal, StoredEntity, db
from models import Produk, StokKeluar, StokMasuk
from services.jwt_service import get_current_user_payload
from dependencies import user_from_payload

router = APIRouter(prefix="/api/stok", tags=["Stok"])
UNIT_ID = "UU05"
ALLOWED_ROLES = {"admin", "direktur", "bendahara"}


async def require_stok_access(payload: dict = Depends(get_current_user_payload)) -> dict:
    """Require an active session and restrict pengelola to the UU05 unit.

    Existing users may store either the unit code (UU05) or the generated
    document id in ``unit_usaha_id``. Resolve both representations against
    the canonical unit collection instead of weakening access to any unit.
    """
    user = await user_from_payload(payload)
    has_uu05_access = False
    if user.role == "pengelola" and user.unit_usaha_id:
        assigned_unit = str(user.unit_usaha_id).upper()
        has_uu05_access = assigned_unit == UNIT_ID
        if not has_uu05_access:
            unit = await db.unit_usaha.select_one({"id": user.unit_usaha_id}, {"_id": 0})
            has_uu05_access = bool(unit and str(unit.get("code", "")).upper() == UNIT_ID)
    if user.role not in ALLOWED_ROLES and not has_uu05_access:
        raise HTTPException(status_code=403, detail="Anda tidak memiliki akses ke modul stok UU05")
    if user.must_change_password:
        raise HTTPException(status_code=403, detail="PASSWORD_CHANGE_REQUIRED")
    return payload


class ProdukInput(BaseModel):
    sku: str = Field(min_length=1, max_length=100)
    nama_produk: str = Field(min_length=1, max_length=255)
    kategori: str = Field(min_length=1, max_length=100)
    satuan: str = Field(min_length=1, max_length=20)
    harga_beli: int = Field(ge=0)
    harga_jual: int = Field(ge=0)


class StokMasukInput(BaseModel):
    produk_id: int = Field(gt=0)
    jumlah: int = Field(gt=0)
    harga_beli_satuan: int = Field(ge=0)


class StokKeluarInput(BaseModel):
    produk_id: int = Field(gt=0)
    jumlah: int = Field(gt=0)
    tipe_keluar: Literal["penjualan", "rusak", "kadaluarsa"]
    keterangan: str | None = Field(default=None, max_length=500)


def produk_response(item: Produk) -> dict:
    return {
        "id": item.id,
        "sku": item.sku,
        "nama_produk": item.nama_produk,
        "kategori": item.kategori,
        "stok_saat_ini": item.stok_saat_ini,
        "satuan": item.satuan,
        "harga_beli": item.harga_beli,
        "harga_jual": item.harga_jual,
        "unit_id": item.unit_id,
    }


@router.post("/produk", status_code=status.HTTP_201_CREATED)
async def buat_produk(data: ProdukInput, _: dict = Depends(require_stok_access)):
    async with SessionLocal() as session:
        exists = await session.scalar(select(Produk).where(Produk.sku == data.sku, Produk.unit_id == UNIT_ID))
        if exists:
            raise HTTPException(status_code=409, detail="SKU sudah digunakan pada unit UU05")
        item = Produk(**data.model_dump(), unit_id=UNIT_ID)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return produk_response(item)


@router.get("/produk")
async def daftar_produk(_: dict = Depends(require_stok_access)):
    async with SessionLocal() as session:
        result = await session.scalars(select(Produk).where(Produk.unit_id == UNIT_ID).order_by(Produk.nama_produk))
        return [produk_response(item) for item in result.all()]


@router.post("/masuk", status_code=status.HTTP_201_CREATED)
async def catat_stok_masuk(data: StokMasukInput, _: dict = Depends(require_stok_access)):
    async with SessionLocal() as session:
        async with session.begin():
            product = await session.scalar(select(Produk).where(Produk.id == data.produk_id, Produk.unit_id == UNIT_ID).with_for_update())
            if not product:
                raise HTTPException(status_code=404, detail="Produk UU05 tidak ditemukan")
            total = data.jumlah * data.harga_beli_satuan
            item = StokMasuk(
                produk_id=product.id,
                jumlah=data.jumlah,
                harga_beli_satuan=data.harga_beli_satuan,
                total_biaya=total,
                status_keuangan="belum_sinkron",
                unit_id=UNIT_ID,
            )
            product.stok_saat_ini += data.jumlah
            session.add(item)
        await session.refresh(item)
        return {"pesan": "Stok masuk berhasil dicatat", "id": item.id, "total_biaya": total, "status_keuangan": item.status_keuangan}


@router.post("/keluar", status_code=status.HTTP_201_CREATED)
async def catat_stok_keluar(data: StokKeluarInput, _: dict = Depends(require_stok_access)):
    async with SessionLocal() as session:
        async with session.begin():
            product = await session.scalar(select(Produk).where(Produk.id == data.produk_id, Produk.unit_id == UNIT_ID).with_for_update())
            if not product:
                raise HTTPException(status_code=404, detail="Produk UU05 tidak ditemukan")
            if product.stok_saat_ini < data.jumlah:
                raise HTTPException(status_code=422, detail="Stok tidak mencukupi")
            item = StokKeluar(produk_id=product.id, unit_id=UNIT_ID, **data.model_dump())
            product.stok_saat_ini -= data.jumlah
            session.add(item)
        await session.refresh(item)
        return {"pesan": "Stok keluar berhasil dicatat", "id": item.id, "stok_saat_ini": product.stok_saat_ini}


@router.get("/mutasi")
async def daftar_mutasi(_: dict = Depends(require_stok_access)):
    async with SessionLocal() as session:
        masuk = (await session.execute(
            select(StokMasuk, Produk.nama_produk)
            .join(Produk, Produk.id == StokMasuk.produk_id)
            .where(StokMasuk.unit_id == UNIT_ID)
            .order_by(StokMasuk.tanggal.desc())
        )).all()
        keluar = (await session.execute(
            select(StokKeluar, Produk.nama_produk)
            .join(Produk, Produk.id == StokKeluar.produk_id)
            .where(StokKeluar.unit_id == UNIT_ID)
            .order_by(StokKeluar.tanggal.desc())
        )).all()
        rows = [
            {"id": item.id, "tanggal": item.tanggal, "nama_produk": nama, "jenis": "in", "jumlah": item.jumlah, "total_biaya": item.total_biaya, "status_keuangan": item.status_keuangan}
            for item, nama in masuk
        ] + [
            {"id": item.id, "tanggal": item.tanggal, "nama_produk": nama, "jenis": "out", "jumlah": item.jumlah, "total_biaya": 0, "status_keuangan": "terbuku"}
            for item, nama in keluar
        ]
        return sorted(rows, key=lambda row: row["tanggal"], reverse=True)


@router.get("/masuk/ringkasan-mingguan")
async def ringkasan_mingguan(_: dict = Depends(require_stok_access)):
    async with SessionLocal() as session:
        items = (await session.scalars(select(StokMasuk).where(StokMasuk.status_keuangan == "belum_sinkron", StokMasuk.unit_id == UNIT_ID))).all()
        return {"total_biaya": sum(item.total_biaya for item in items), "jumlah_item": len(items), "status_keuangan": "belum_sinkron" if items else "terkirim"}


@router.post("/mutasi")
async def catat_mutasi(data: dict, _: dict = Depends(require_stok_access)):
    jenis = data.get("jenis")
    if jenis == "in":
        return await catat_stok_masuk(StokMasukInput(produk_id=int(data["produk_id"]), jumlah=int(data["jumlah"]), harga_beli_satuan=int(data.get("harga_satuan", 0))))
    if jenis == "out":
        return await catat_stok_keluar(StokKeluarInput(produk_id=int(data["produk_id"]), jumlah=int(data["jumlah"]), tipe_keluar="penjualan", keterangan=data.get("keterangan")))
    raise HTTPException(status_code=422, detail="Jenis mutasi harus in atau out")


@router.post("/masuk/sinkronisasi-mingguan")
async def sinkronisasi_mingguan(_: dict = Depends(require_stok_access)):
    expected_transaction_name = "2. Pembelian Barang Dagangan (Sinkronisasi Aplikasi)"
    expected_debit = "1.1.05.51"
    expected_credit = "1.1.01.15"

    async with SessionLocal() as session:
        async with session.begin():
            items = list((await session.scalars(select(StokMasuk).where(StokMasuk.status_keuangan == "belum_sinkron", StokMasuk.unit_id == UNIT_ID).with_for_update())).all())
            total = sum(abs(item.total_biaya) for item in items)
            if not items:
                return {"pesan": "Tidak ada stok masuk yang perlu disinkronkan", "jumlah_item": 0, "total_biaya": 0}

            transaction_type = await db.transaction_types.select_one({"code": "2", "group": UNIT_ID}, {"_id": 0})
            if not transaction_type:
                transaction_type = await db.transaction_types.select_one({"name": expected_transaction_name, "group": UNIT_ID}, {"_id": 0})
            if not transaction_type:
                raise HTTPException(status_code=409, detail=f"Jenis transaksi UU05 wajib belum tersedia. Tambahkan: {expected_transaction_name}")
            if str(transaction_type.get("name", "")).strip() != expected_transaction_name:
                raise HTTPException(status_code=409, detail=f"Jenis transaksi UU05 dengan kode 2 tidak sesuai. Nama wajib: {expected_transaction_name}")

            debit_account = await db.accounts.select_one({"code": expected_debit, "group": UNIT_ID}, {"_id": 0})
            if not debit_account or str(debit_account.get("name", "")).strip() != "Persediaan Barang Dagangan":
                raise HTTPException(status_code=409, detail=f"Akun debit UU05 belum tersedia atau namanya tidak sesuai: {expected_debit} - Persediaan Barang Dagangan")
            credit_account = await db.accounts.select_one({"code": expected_credit, "group": UNIT_ID}, {"_id": 0})
            if not credit_account or str(credit_account.get("name", "")).strip() != "Kas/Bank - UU05":
                raise HTTPException(status_code=409, detail=f"Akun kredit UU05 belum tersedia atau namanya tidak sesuai: {expected_credit} - Kas/Bank - UU05")

            ledger = StoredEntity(
                namespace="transactions",
                id=str(uuid4()),
                payload={
                    "date": datetime.now(timezone.utc).date().isoformat(),
                    "unit_usaha_id": UNIT_ID,
                    "transaction_type": expected_transaction_name,
                    "description": expected_transaction_name,
                    "amount": total,
                    "debit_account_code": expected_debit,
                    "debit_account_name": "Persediaan Barang Dagangan",
                    "credit_account_code": expected_credit,
                    "credit_account_name": "Kas/Bank - UU05",
                    "reference": "sinkronisasi-stok-mingguan",
                    "created_by": "sistem-stok",
                },
            )
            session.add(ledger)
            for item in items:
                item.status_keuangan = "terkirim"
            return {"pesan": "Rekap stok berhasil terbuku di keuangan", "jumlah_item": len(items), "total_biaya": total, "status_keuangan": "terkirim"}
