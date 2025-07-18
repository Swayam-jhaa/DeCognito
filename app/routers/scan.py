from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
import os
import requests

from connectors import whois, shodan, sherlock, breachdirectory
from app.dependencies import get_db
from app.models import ScanHistory

router = APIRouter(
    prefix="/scan",
    tags=["scan"]
)

# Existing single scan models
class ScanRequest(BaseModel):
    query: str
    type: str  # "email", "username", "domain", "ip"

class ScanResponse(BaseModel):
    query: str
    type: str
    result: dict

# Bulk scan models
class SingleQuery(BaseModel):
    query: str
    type: str  # "email", "username", "domain", "ip"

class MultiScanRequest(BaseModel):
    queries: list[SingleQuery]

@router.post("/", response_model=ScanResponse)
async def do_scan(
    req: ScanRequest,
    db: Session = Depends(get_db)
):
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

    record = ScanHistory(
        query=req.query,
        type=req.type,
        result=json.dumps(result)
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "query": req.query,
        "type": req.type,
        "result": result
    }

def summarize_with_gemini(results):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "No Gemini API key configured."
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    prompt = (
        "Given the following OSINT scan results, summarize the most relevant findings and connections for an investigator:\n\n"
        + json.dumps(results, indent=2)
    )
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        candidates = response.json().get("candidates")
        if candidates and "content" in candidates[0]:
            return candidates[0]["content"]["parts"][0]["text"]
        else:
            return "No summary generated."
    else:
        return f"Gemini API error: {response.text}"

@router.post("/bulk_scan_and_summarize/")
async def bulk_scan_and_summarize(
    req: MultiScanRequest,
    db: Session = Depends(get_db)
):
    results = []
    for q in req.queries:
        if q.type == "domain":
            result = whois.lookup(q.query)
        elif q.type == "ip":
            result = shodan.lookup_ip(q.query)
        elif q.type == "username":
            result = sherlock.lookup_username(q.query)
        elif q.type == "email":
            result = breachdirectory.check_email_breaches(q.query)
        else:
            result = {"error": "Invalid scan type"}
        record = ScanHistory(
            query=q.query,
            type=q.type,
            result=json.dumps(result)
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        results.append({"query": q.query, "type": q.type, "result": result})

    summary = summarize_with_gemini(results)
    return {
        "results": results,
        "summary": summary
    }
from connectors.twitter_scrapper import scrape_twitter

@router.get("/twitter_posts/")
async def get_twitter_posts(username: str):
    """
    Get the latest tweets for a given username.
    """
    return scrape_twitter(username)