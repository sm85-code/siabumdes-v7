"""SQLAlchemy models for finance domain.

Note: current finance/transactions data lives in the generic
application_entities (StoredEntity) document store.
Add concrete ORM tables here when migrating away from JSONB.
"""
from __future__ import annotations

from app.core.database import Base

# Placeholder for future relational finance models (Account, JournalEntry, etc.)
