from sqlalchemy.orm import Session
from app.db.session import engine, AsyncSessionLocal
from app.db.models.wallet_log import WalletLog
from sqlalchemy.exc import IntegrityError
from app.db.models.base import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("database connected")

async def close_db():
    await engine.dispose()
    print("database connection closed")