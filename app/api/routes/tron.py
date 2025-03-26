from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.exceptions import AddressNotFound

from app.db.models.wallet_log import WalletLog
from app.db.repos.wallet_log_repos import log_wallet_request
from app.dto.wallet import WalletInfoResponse, WalletInfoRequest
from app.db.session import get_db

from app.services.tron_service import get_wallet_info

router = APIRouter()


@router.post("/wallet_info", response_model=WalletInfoResponse)
async def get_wallet_info_endpoint(request: WalletInfoRequest, db: AsyncSession = Depends(get_db)):
    wallet_address = request.address

    try:
        wallet_info = await log_wallet_request(db, wallet_address)
        if wallet_info is None:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet_info
    except AddressNotFound:
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/wallet_logs")
async def get_wallet_logs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    stmt = select(WalletLog).offset(skip).limit(limit)
    result = await db.execute(stmt)
    logs = result.scalars().all()
    return logs
