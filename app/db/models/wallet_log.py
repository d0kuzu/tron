from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

from app.db.models.base import Base


class WalletLog(Base):
    __tablename__ = 'wallet_logs'

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    request_time = Column(DateTime, default=datetime.datetime.utcnow)
    balance_trx = Column(Integer)
    bandwidth = Column(Integer)
    energy = Column(Integer)
