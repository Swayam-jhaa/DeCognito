import os
import requests
from dotenv import load_dotenv

# Load RAPIDAPI_KEY from your .env
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
BASE_URL = "https://breachdirectory.p.rapidapi.com/"

def check_email_breaches(email: str) -> dict:
    """
    Query BreachDirectory via RapidAPI.
    Returns a dict with either:
      - {"breaches": [...]} on success, or
      - {"error": "..."} on failure.
    """
    headers = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
}

    params = {"func": "auto", "term": email}

    try:
        resp = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json() or {}

        # data’s keys are breach names; map to list
        return {"breaches": list(data.keys())}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
