from pydantic import BaseModel

class WalletInfoRequest(BaseModel):
    address: str

class WalletInfoResponse(BaseModel):
    balance_trx: int
    bandwidth: int
    energy: int