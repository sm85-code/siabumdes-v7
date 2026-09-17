"""Compatibility facade for domain models."""
from models.base import *
from models.auth import *
from models.master_data import *
from models.transactions import *
# Inventory (Produk, StokMasuk, StokKeluar) di-export oleh package models/__init__.py
# via relative import — jangan import models.inventory di sini (bentrok models.py vs models/).
