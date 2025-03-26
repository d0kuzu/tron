from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.db.models.wallet_log import WalletLog
from app.services.tron_service import get_wallet_info


async def log_wallet_request(db: AsyncSession, address: str):
    wallet_info = await get_wallet_info(address)
    if wallet_info is None:
        return None

    wallet_log = WalletLog(
        wallet_address=address,
        balance_trx=wallet_info['balance_trx'],
        bandwidth=wallet_info['bandwidth'],
        energy=wallet_info['energy']
    )

    db.add(wallet_log)
    await db.commit()
    await db.refresh(wallet_log)

    return wallet_log
