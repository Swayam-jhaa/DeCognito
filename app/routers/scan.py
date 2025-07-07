# app/routers/scan.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from connectors import whois, shodan, sherlock, breachdirectory
from app.dependencies import get_db
from app.models import ScanHistory

router = APIRouter(
    prefix="/scan",
    tags=["scan"]
)

class ScanRequest(BaseModel):
    query: str       # e.g. email, username, domain, ip
    type: str        # one of: "email", "username", "domain", "ip"

class ScanResponse(BaseModel):
    query: str
    type: str
    result: dict

@router.post("/", response_model=ScanResponse)
async def do_scan(
    req: ScanRequest,
    db: Session = Depends(get_db)
):
    # Dispatch to the appropriate connector
    if req.type == "domain":
        result = whois.lookup(req.query)
    elif req.type == "ip":
        result = shodan.lookup_ip(req.query)
    elif req.type == "username":
        result = sherlock.lookup_username(req.query)
    elif req.type == "email":
        result = breachdirectory.check_email_breaches(req.query)
    else:
        raise HTTPException(status_code=400, detail="Invalid scan type")

    # Persist the scan into the database
    record = ScanHistory(
        query=req.query,
        type=req.type,                # match your model’s `type` column
        result=json.dumps(result)     # store the result as a JSON string
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # Return the scan result
    return {
        "query": req.query,
        "type": req.type,
        "result": result
    }
