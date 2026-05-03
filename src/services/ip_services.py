from utils import http
import asyncio
import aiohttp
async def load_data(ip):
    async with aiohttp.ClientSession() as session:
        # Run both external lookups together so the CLI waits for one network round trip.
        tasks = [
            http.get_ipinfo(session, ip),
            http.get_abuse(session, ip),
        ]

        geo, abuse = await asyncio.gather(*tasks)

        # Keep a flat dictionary here because the output formatter expects normalized keys.
        return {
            "ip": str(ip),
            "country": geo.get("country"),
            "city": geo.get("city"),
            "isp": geo.get("org"),
            "location": geo.get("loc"),
            "abuse_score": abuse.get("data", {}).get("abuseConfidenceScore"),
            "total_reports": abuse.get("data", {}).get("totalReports"),
        }
        

