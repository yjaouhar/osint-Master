from utils import domain as d
import aiohttp
import asyncio
async def load_data(domain):
    async with aiohttp.ClientSession() as session:
        sub_domains = await d.sub_domain(session, domain)
        results = []
        for sub in sub_domains:
            # DNS, SSL, and takeover checks are independent, so gather them per subdomain.
            ip, ssl_info, risk = await asyncio.gather(
                asyncio.to_thread(d.get_ip, sub),
                asyncio.to_thread(d.get_ssl, sub),
                d.check_takeover(session, sub)        
            )
            results.append({"sub": sub, "ip": ip, "ssl": ssl_info, "risk": risk})
        return results
