import requests
import os

def check_breaches(email: str) -> dict:
    api_key = os.getenv("HIBP_API_KEY")
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "DeCognito-Scanner"
    }

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=true"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return {"breaches": []}
        elif response.status_code == 200:
            return {"breaches": response.json()}
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
