ABUSEIPDB_KEY = "fd4a6af4852e43bd4080bcb67ac9e4d1bdac52a73ce3b64d8236cdb91a72cabe59c265a84e41d575"

async def fetch(session, url, headers=None, params=None):
    try:
        async with session.get(url, headers=headers, params=params, timeout=10) as resp:
            return await resp.json()
    except Exception as e:
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

async def check_blacklist(session, ip):
    reversed_ip = ".".join(str(ip).split(".")[::-1])
    
    query = f"{reversed_ip}.zen.spamhaus.org"

    url = f"https://dns.google/resolve?name={query}"

    result = await fetch(session, url)

    if result.get("Answer"):
        return {"blacklisted": True, "source": "Spamhaus"}
    return {"blacklisted": False}
#         {
#   "Status": 3,
#   "TC": false,
#   "RD": true,
#   "RA": true,
#   "AD": false,
#   "CD": false,
#   "Question": [
#     {
#       "name": "170.252.144.154.zen.spamhaus.org.",
#       "type": 1
#     }
#   ],
#   "Authority": [
#     {
#       "name": "zen.spamhaus.org.",
#       "type": 6,
#       "TTL": 10,
#       "data": "need.to.know.only. hostmaster.spamhaus.org. 2604301455 3600 600 432000 10"
#     }
#   ],
#   "Comment": "Response from 2a05:9403::26e."
# }
