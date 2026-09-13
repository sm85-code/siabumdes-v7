"""Shared dependencies for reporting calculation modules."""
from typing import Optional

from fastapi import HTTPException

from database import db

__all__ = ["Optional", "HTTPException", "db"]
