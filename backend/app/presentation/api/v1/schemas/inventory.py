from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ProdukCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=100)
    nama_produk: str = Field(min_length=1, max_length=255)
    kategori: str = Field(min_length=1, max_length=100)
    satuan: str = Field(min_length=1, max_length=20)
    harga_beli: int = Field(ge=0)
    harga_jual: int = Field(ge=0)


class ProdukOut(BaseModel):
    id: int
    sku: str
    nama_produk: str
    kategori: str
    stok_saat_ini: int
    satuan: str
    harga_beli: int
    harga_jual: int
    unit_id: str

    model_config = {"from_attributes": True}


class StokMasukCreate(BaseModel):
    produk_id: int = Field(gt=0)
    tanggal: date = Field(default_factory=date.today)
    jumlah: int = Field(gt=0)
    harga_beli_satuan: int = Field(ge=0)


class StokKeluarCreate(BaseModel):
    produk_id: int = Field(gt=0)
    tanggal: date = Field(default_factory=date.today)
    jumlah: int = Field(gt=0)
    tipe_keluar: Literal["penjualan", "rusak", "kadaluarsa"]
    keterangan: Optional[str] = Field(default=None, max_length=500)


class StokMutasiOut(BaseModel):
    id: int
    pesan: str
    stok_saat_ini: Optional[int] = None
    total_biaya: Optional[int] = None
