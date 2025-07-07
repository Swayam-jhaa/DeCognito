from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db import Base

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    type = Column(String, index=True)
    result = Column(Text)  # store JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)
