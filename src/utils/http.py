from config.settings import ABUSEIPDB_KEY
import json
async def fetch(session, url, headers=None, params=None):
    try:
        async with session.get(url, headers=headers, params=params, timeout=10) as resp:
            return await resp.json()
    except Exception as e:
        # Return a consistent payload shape so callers can still use .get() safely.
        return {"error": str(e)}
    

async def get_ipinfo(session, ip):
    url = f"https://ipinfo.io/{ip}/json"
    return await fetch(session, url)


async def get_abuse(session, ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSEIPDB_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    return await fetch(session, url, headers=headers, params=params)

