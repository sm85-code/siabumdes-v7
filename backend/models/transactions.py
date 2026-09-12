from typing import Optional
from pydantic import BaseModel
from .base import BaseDocument, now_utc

class Transaction(BaseDocument):
    date: str  # YYYY-MM-DD
    unit_usaha_id: Optional[str] = None  # null = bumdes-level
    transaction_type: str  # e.g. "penerimaan_bagi_hasil", "beban_operasional", "modal_mitra", etc
    description: str
    amount: float
    debit_account_code: str
    credit_account_code: str
    mitra_id: Optional[str] = None
    reference: str = ""  # optional invoice/nota number
    created_by: str  # user id
    created_at: datetime = Field(default_factory=now_utc)

class TransactionCreate(BaseModel):
    date: str
    unit_usaha_id: Optional[str] = None
    transaction_type: str
    description: str
    amount: float
    debit_account_code: str
    credit_account_code: str
    mitra_id: Optional[str] = None
    reference: str = ""

class RevenueShare(BaseDocument):
    period: str  # YYYY-MM
    unit_usaha_id: str
    gross_revenue: float = 0.0
    operational_cost: float = 0.0
    net_revenue: float = 0.0  # gross - op cost
    manager_share: float = 0.0  # 30%
    bumdes_share: float = 0.0  # 70%
    manager_user_id: Optional[str] = None
    status: str = "draft"  # draft | disetor
    settled_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=now_utc)

class RevenueShareCreate(BaseModel):
    period: str
    unit_usaha_id: str
    gross_revenue: float
    operational_cost: float = 0.0
