import dns.resolver
import ssl
import socket
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

async def sub_domain(session,domain):
      
    subs = set()
    try:
        async with session.get(
            f"https://rapiddns.io/subdomain/{domain}?full=1&down=1",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=aiohttp.ClientTimeout(total=30)
        ) as r:
            if r.status == 200:
                soup = BeautifulSoup(await r.text(), "html.parser")
                for td in soup.find_all("td"):
                    txt = td.text.strip().lower()
                    # RapidDNS returns many table cells, so keep only real subdomains of the target.
                    if txt.endswith(domain) and "*" not in txt:
                        subs.add(txt)
    except:
        pass
    print(f"[rapiddns] {len(subs)}")
    return subs

    

def get_ip(domain):
    try:
        return dns.resolver.resolve(domain, "A")[0].to_text()
    except:
        return "N/A"


def get_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            return f"Valid until {date.strftime('%Y-%m-%d')}"
    except:
        return "Not found"
    
SERVICES = {
    "amazonaws.com": {
        "name": "AWS S3 bucket",
        "fingerprint": "NoSuchBucket"          # error message ديال S3
    },
    "github.io": {
        "name": "GitHub Pages",
        "fingerprint": "There isn't a GitHub Pages site here"
    },
    "herokuapp.com": {
        "name": "Heroku",
        "fingerprint": "No such app"
    },
    "azurewebsites.net": {
        "name": "Azure",
        "fingerprint": "404 Web Site not found"
    },
    "netlify.app": {
        "name": "Netlify",
        "fingerprint": "Not Found - Request ID"
    },
    "vercel.app": {
        "name": "Vercel",
        "fingerprint": "The deployment could not be found"
    },
    "pages.dev": {
        "name": "Cloudflare Pages",
        "fingerprint": "cloudflare"
    },
    "shopify.com": {
        "name": "Shopify",
        "fingerprint": "Sorry, this shop is currently unavailable"
    },
    "fastly.net": {
        "name": "Fastly",
        "fingerprint": "Fastly error: unknown domain"
    },
}

async def check_takeover(session, domain):
    matched_service = None
    try:
        cnames = dns.resolver.resolve(domain, "CNAME")
        for cname in cnames:
            cname = str(cname)
            for pattern, service in SERVICES.items():
                # Map the CNAME target to a provider profile before checking the HTTP fingerprint.
                if pattern in cname:
                    matched_service = service
                    break
    except dns.resolver.NoAnswer as e:
        return None 
    except dns.resolver.NXDOMAIN as e: 
        return None  
    except Exception as e:
        return None

    if not matched_service:
        return None

    try:
        async with session.get(
            f"http://{domain}",
            timeout=aiohttp.ClientTimeout(total=5),
            allow_redirects=True
        ) as r:
            body = await r.text()
            # A provider-specific error page is the signal that the DNS record may be dangling.
            if matched_service["fingerprint"].lower() in body.lower():
                return matched_service["name"]
    except:
        pass

    return None
