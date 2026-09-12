"""Shared dependencies for reporting calculation modules."""
from typing import Optional

from fastapi import HTTPException

from services.mongodb_service import db

__all__ = ["Optional", "HTTPException", "db"]
