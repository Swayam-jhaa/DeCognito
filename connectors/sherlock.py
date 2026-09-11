import subprocess
import re

def lookup_username(username: str) -> dict:
    """
    Call the sherlock CLI, capture its text output, and parse lines that start with “[+]”.
    Returns a dict mapping site names to URLs.
    """
    try:
        # Run sherlock without JSON, just get text
        proc = subprocess.run(
            ["sherlock", "--print-found", username],
            capture_output=True,
            text=True
        )
        if proc.returncode not in (0, 1):
            # 1 is expected when profiles are found
            return {"error": f"Sherlock exited with code {proc.returncode}", 
                    "stderr": proc.stderr.strip()}

        site_map = {}
        # Regex to match lines like: "[+] GitHub: https://github.com/elonmusk"
        pattern = re.compile(r"^\[\+\]\s+(.+?):\s+(https?://\S+)", re.MULTILINE)

        for match in pattern.finditer(proc.stdout):
            site, url = match.groups()
            site_map[site.strip()] = url.strip()

        if not site_map:
            return {"error": "No profiles found."}
        return site_map

    except FileNotFoundError:
        return {"error": "Sherlock CLI not installed in this environment."}
    except Exception as e:
        return {"error": str(e)}
    
