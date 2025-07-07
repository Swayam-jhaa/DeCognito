import whois

def lookup(domain: str) -> dict:
    """
    Perform a WHOIS lookup on the given domain.
    Returns a dict of key fields or an error message.
    """
    try:
        w = whois.whois(domain)
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "status": w.status
        }
    except Exception as e:
        return {"error": str(e)}
