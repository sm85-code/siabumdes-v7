"""Compatibility facade for domain models."""
from models.base import *
from models.auth import *
from models.master_data import *
from models.transactions import *
from models.inventory import Produk, StokKeluar, StokMasuk  # noqa: F401 — dual-way stock sync
