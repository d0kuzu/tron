import httpx
from app.core.config import settings

async def get_wallet_info(address: str):
    url = f"https://api.trongrid.io/v1/accounts/{address}"
    headers = {"TRON-PRO-API-KEY": settings.TRON_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        balance_trx = data.get("balance", 0) / 1_000_000
        bandwidth = data.get("bandwidth", 0)
        energy = data.get("energy", 0)

        return {
            "balance_trx": balance_trx,
            "bandwidth": bandwidth,
            "energy": energy
        }
    elif response.status_code == 404:
        return None
    else:
        response.raise_for_status()
