from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import json

from app.dependencies import get_db
from app.models import ScanHistory

router = APIRouter(
    prefix="/history",
    tags=["history"]
)

class HistoryItem(BaseModel):
    id: int
    query: str
    type: str
    result: dict
    timestamp: str

@router.get("/", response_model=List[HistoryItem])
def list_history(db: Session = Depends(get_db)):
    rows = db.query(ScanHistory).order_by(ScanHistory.timestamp.desc()).all()
    items = []
    for row in rows:
        items.append(HistoryItem(
            id=row.id,
            query=row.query,
            type=row.type,
            result=json.loads(row.result),
            timestamp=row.timestamp.isoformat()
        ))
    return items
