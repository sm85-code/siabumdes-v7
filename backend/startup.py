"""Database seed and migration lifecycle for the FastAPI application."""
import logging
from services.mongodb_service import db
from models import Account, UnitUsaha, User, UserRole
from services.jwt_service import hash_password
from seed_data import CHART_OF_ACCOUNTS, UNIT_USAHA_SEED, VALID_ACCOUNT_CATEGORIES

logger = logging.getLogger(__name__)


async def _ensure_indexes() -> None:
    indexes = {
        "users": [("email", {"unique": True}), ("username", {"unique": True})],
        "transactions": [("date", {}), ("unit_usaha_id", {}), ("created_by", {}), ("debit_account_code", {}), ("credit_account_code", {})],
        "accounts": [("code", {"unique": True})],
        "unit_usaha": [("code", {"unique": True})],
        "transaction_types": [("code", {"unique": True})],
    }
    for collection_name, definitions in indexes.items():
        collection = getattr(db, collection_name)
        for field, options in definitions:
            try:
                await collection.create_index(field, **options)
            except Exception as exc:
                logger.warning("Index %s.%s tidak dibuat: %s", collection_name, field, exc)


def _validate_seed_data() -> None:
    account_codes = [code for code, *_ in CHART_OF_ACCOUNTS]
    duplicates = {code for code in account_codes if account_codes.count(code) > 1}
    if duplicates:
        raise RuntimeError(f"Duplicate account codes in seed: {sorted(duplicates)}")

    invalid_seed_categories = sorted({category for _, _, category, _, _ in CHART_OF_ACCOUNTS if category not in VALID_ACCOUNT_CATEGORIES})
    if invalid_seed_categories:
        raise RuntimeError(f"COA seed has invalid categories: {invalid_seed_categories}")
    invalid_seed_pairs = sorted({(category, subcategory) for _, _, category, subcategory, _ in CHART_OF_ACCOUNTS if subcategory not in VALID_ACCOUNT_CATEGORIES.get(category, ())})
    if invalid_seed_pairs:
        raise RuntimeError(f"COA seed has invalid category/subcategory pairs: {invalid_seed_pairs}")

    required_subcategories = {"kas_bank", "modal_desa", "modal_masyarakat", "saldo_laba", "bagi_hasil_desa", "bagi_hasil_masyarakat"}
    actual_subcategories = {subcategory for _, _, _, subcategory, _ in CHART_OF_ACCOUNTS}
    missing_subcategories = sorted(required_subcategories - actual_subcategories)
    if missing_subcategories:
        raise RuntimeError(f"COA seed is missing required subcategories: {missing_subcategories}")


async def _migrate_account_subcategories() -> None:
    corrections = {
        "3.1.01.01": "modal_desa",
        "3.1.01.02": "modal_masyarakat",
        "3.2.01.01": "saldo_laba",
        "3.2.01.02": "saldo_laba",
        "3.2.01.03": "saldo_laba",
        "3.2.01.04": "saldo_laba",
        "3.2.02.01": "bagi_hasil_desa",
        "3.2.02.02": "bagi_hasil_masyarakat",
    }
    for code, subcategory in corrections.items():
        await db.accounts.update_many({"code": code}, {"$set": {"subcategory": subcategory}})


DATA_RESET_VERSION = 2


async def _reset_legacy_account_data_once() -> None:
    marker = await db.system_config.find_one({"key": "account_data_reset_version"})
    if marker and marker.get("value", 0) >= DATA_RESET_VERSION:
        return

    await db.accounts.delete_many({})
    await db.transaction_types.delete_many({})
    await db.transactions.delete_many({})
    await db.system_config.update_one(
        {"key": "account_data_reset_version"},
        {"$set": {"value": DATA_RESET_VERSION}},
        upsert=True,
    )
    logger.warning("Reset legacy accounts, transaction types, and transactions for migration version %s", DATA_RESET_VERSION)


async def seed_startup() -> None:
    _validate_seed_data()
    await _reset_legacy_account_data_once()
    await _ensure_indexes()
    await _migrate_account_subcategories()
    if await db.accounts.count_documents({}) == 0:
        docs = [Account(code=code, name=name, category=cat, subcategory=sub, normal_balance=nb).to_mongo() for code, name, cat, sub, nb in CHART_OF_ACCOUNTS]
        if docs:
            await db.accounts.insert_many(docs)
        logger.info("Seeded %s accounts", len(docs))
    if await db.unit_usaha.count_documents({}) == 0:
        docs = [UnitUsaha(code=code, name=name, description=desc, revenue_scheme=scheme).to_mongo() for code, name, desc, scheme in UNIT_USAHA_SEED]
        if docs:
            await db.unit_usaha.insert_many(docs)
        logger.info("Seeded %s unit usaha", len(docs))
    logger.info("Transaction types remain empty; admin will configure them through the application.")
    await db.transactions.update_many({"unit_usaha_id": ""}, {"$set": {"unit_usaha_id": None}})
    await db.accounts.update_many({"group": {"$exists": False}}, {"$set": {"group": "BUMDES"}})
    async for acc in db.accounts.find({"subcategory": {"$ne": "kas_bank"}, "category": "aset"}, {"_id": 0}):
        if any(word in (acc.get("name") or "").lower() for word in ("kas", "bank")):
            await db.accounts.update_one({"code": acc["code"], "group": acc.get("group", "BUMDES")}, {"$set": {"subcategory": "kas_bank"}})
    for t in await db.transaction_types.find({"group": {"$exists": False}}, {"_id": 0}).to_list(500):
        uc = t.get("unit_codes") or []
        await db.transaction_types.update_one({"code": t["code"]}, {"$set": {"group": uc[0] if uc else "BUMDES"}})
    if await db.users.count_documents({}) == 0:
        default_users = [("admin@bumdes.id", "admin", "Admin Utama", UserRole.ADMIN, "admin123"), ("budianto@bumdes.id", "budianto", "Budianto (Direktur)", UserRole.DIREKTUR, "direktur123"), ("riska@bumdes.id", "riska", "Riska Vianti (Bendahara)", UserRole.BENDAHARA, "bendahara123")]
        for email, username, name, role, password in default_users:
            await db.users.insert_one(User(email=email, username=username, name=name, role=role, password_hash=hash_password(password)).to_mongo())
        logger.info("Seeded default users")
    await db.users.update_many(
        {"plain_password": {"$exists": True}},
        {"$unset": {"plain_password": ""}},
    )
