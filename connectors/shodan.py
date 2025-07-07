import os
import shodan

# Load API key from environment (add SHODAN_API_KEY to your .env)
_api_key = os.getenv("SHODAN_API_KEY")
_client = shodan.Shodan(_api_key)

def lookup_ip(ip: str) -> dict:
    """
    Perform a Shodan lookup for an IP address.
    Returns a dict of host information or an error.
    """
    try:
        host = _client.host(ip)
        return {
            "ip_str": host.get("ip_str"),
            "organization": host.get("org"),
            "os": host.get("os"),
            "ports": host.get("ports"),
            "vulns": host.get("vulns"),
            "data": host.get("data"),
        }
    except shodan.APIError as e:
        return {"error": str(e)}
