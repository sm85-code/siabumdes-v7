"""Application entrypoint (Clean Architecture)."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.api.v1.routers import accounts, stok

app = FastAPI(title="BUMDES Karya Raharja", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stok.router)
app.include_router(accounts.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"app": "BUMDES Karya Raharja", "version": "2.0.0"}
