import requests
import os

def check_email_breaches(email: str) -> dict:
    api_key = os.getenv("RAPIDAPI_KEY")
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
    }
    url = f"https://breachdirectory.p.rapidapi.com/?func=auto&term={email}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {"breaches": data.get("result", [])}
            else:
                return {"breaches": []}
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}