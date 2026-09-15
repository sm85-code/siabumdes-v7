"""SQLAlchemy models for inventory (produk & stok)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Produk(Base):
    __tablename__ = "produk"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    nama_produk: Mapped[str] = mapped_column(String(255), nullable=False)
    kategori: Mapped[str] = mapped_column(String(100), nullable=False)
    stok_saat_ini: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    satuan: Mapped[str] = mapped_column(String(20), nullable=False)
    harga_beli: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    harga_jual: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    unit_id: Mapped[str] = mapped_column(String(50), nullable=False, default="UU05", index=True)


class StokMasuk(Base):
    __tablename__ = "stok_masuk"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tanggal: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    produk_id: Mapped[int] = mapped_column(ForeignKey("produk.id"), nullable=False, index=True)
    jumlah: Mapped[int] = mapped_column(Integer, nullable=False)
    harga_beli_satuan: Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_biaya: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status_keuangan: Mapped[str] = mapped_column(String(30), nullable=False, default="belum_sinkron")
    unit_id: Mapped[str] = mapped_column(String(50), nullable=False, default="UU05", index=True)


class StokKeluar(Base):
    __tablename__ = "stok_keluar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tanggal: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    produk_id: Mapped[int] = mapped_column(ForeignKey("produk.id"), nullable=False, index=True)
    jumlah: Mapped[int] = mapped_column(Integer, nullable=False)
    tipe_keluar: Mapped[str] = mapped_column(String(30), nullable=False)
    keterangan: Mapped[str | None] = mapped_column(String(500), nullable=True)
    unit_id: Mapped[str] = mapped_column(String(50), nullable=False, default="UU05", index=True)
