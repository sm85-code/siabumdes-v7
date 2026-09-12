from typing import Optional
from pydantic import BaseModel
from .base import BaseDocument, now_utc

class UnitUsaha(BaseDocument):
    code: str  # e.g. "UU01"
    name: str
    description: str = ""
    revenue_scheme: str = ""  # description of bagi hasil
    active: bool = True
    created_at: datetime = Field(default_factory=now_utc)

class UnitUsahaCreate(BaseModel):
    code: str
    name: str
    description: str = ""
    revenue_scheme: str = ""

class Mitra(BaseDocument):
    unit_usaha_id: str
    name: str
    mitra_type: str = ""  # peternak_domba, peternak_ikan, tukang_kayu, dll
    phone: str = ""
    address: str = ""
    modal: float = 0.0  # untuk unit 4 (perdagangan)
    active: bool = True
    created_at: datetime = Field(default_factory=now_utc)

class MitraCreate(BaseModel):
    unit_usaha_id: str
    name: str
    mitra_type: str = ""
    phone: str = ""
    address: str = ""
    modal: float = 0.0

class Account(BaseDocument):
    code: str  # e.g. "1.1.01.01"
    name: str
    category: str  # aset | kewajiban | ekuitas | pendapatan | beban
    subcategory: str = ""  # aset_lancar, aset_tetap, dll
    normal_balance: str  # debit | kredit
    parent_code: Optional[str] = None
    group: str = "BUMDES"  # "BUMDES" | "UU01" | ... | "UU06" — kelompok pemilik akun
    active: bool = True

class AccountCreate(BaseModel):
    code: str
    name: str
    category: str
    subcategory: str = ""
    normal_balance: str
    parent_code: Optional[str] = None
    group: str = "BUMDES"
