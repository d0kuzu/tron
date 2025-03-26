from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.models.base import Base
from app.db.models.wallet_log import WalletLog
from app.main import app


engine = create_engine(settings.SYNC_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_create_wallet_info(client, db):
    data = {
        "address": settings.TRON_ADDRESS,
    }

    response = client.post("/tron/wallet_info", json=data)

    assert response.status_code in [200, 404], f"Unexpected status code: {response.status_code}"

    if response.status_code == 404:
        assert response.json() == {"detail": "Wallet not found"}
    else:
        wallet_info = response.json()

        assert isinstance(wallet_info, dict), "Response should be a dictionary"
        assert "balance_trx" in wallet_info, "Missing 'balance_trx' in response"
        assert "bandwidth" in wallet_info, "Missing 'bandwidth' in response"
        assert "energy" in wallet_info, "Missing 'energy' in response"

        assert isinstance(wallet_info["balance_trx"], (int, float)), "Invalid balance type"
        assert isinstance(wallet_info["bandwidth"], int), "Invalid bandwidth type"
        assert isinstance(wallet_info["energy"], int), "Invalid energy type"

        wallet_log = db.query(WalletLog).filter_by(wallet_address=data["address"]).first()
        assert wallet_log is not None, "Wallet log entry was not created"
        assert wallet_log.wallet_address == data["address"], "Wallet address mismatch"
        assert wallet_log.balance_trx == wallet_info["balance_trx"], "Balance mismatch"
        assert wallet_log.bandwidth == wallet_info["bandwidth"], "Bandwidth mismatch"
        assert wallet_log.energy == wallet_info["energy"], "Energy mismatch"

def test_get_wallet_logs(db):
    wallet_log1 = WalletLog(
        wallet_address="TQ5JU61ph2w9GmmneM5v8V8Bq9eGHkmq3V",
        balance_trx=1000,
        bandwidth=500,
        energy=300,
    )
    wallet_log2 = WalletLog(
        wallet_address="TQ5JU61ph2w9GmmneM5v8V8Bq9eGHkmq3V",
        balance_trx=1500,
        bandwidth=600,
        energy=400,
    )

    db.add(wallet_log1)
    db.add(wallet_log2)
    db.commit()

    logs = db.query(WalletLog).filter(WalletLog.wallet_address == "TQ5JU61ph2w9GmmneM5v8V8Bq9eGHkmq3V").all()

    assert len(logs) >= 2
    assert logs[0].wallet_address == wallet_log1.wallet_address
    assert logs[1].wallet_address == wallet_log2.wallet_address
