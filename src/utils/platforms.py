from utils import output
from utils import parser
from config import settings
from bs4 import BeautifulSoup

async def github_lookup(session, username):
    url = f"https://api.github.com/users/{username}"
    try:
        async with session.get(url) as r:
            if r.status != 200:
                return parser.not_found("GitHub")

            data = await r.json()
            return f"""
        - GitHub:
            - found: True,
            - data: 
                - Id : {data.get("id")}
                - Full Name : {data.get("name")}
                - followers: {data.get("followers")}
                - repos: {data.get("public_repos")}
                - bio: {data.get("bio")}
""" 
    except Exception as e:
        print(f"[ERROR] {"GitHub"}: {e}")
        return parser.not_found("GitHub")

async def hackerNews_lookup(session, username):
    url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
    try:
        async with session.get(url) as r:
            if r.status != 200:
                return parser.not_found("HackerNews")

            data = await r.json()
            if not data:
                return parser.not_found("HackerNews")

            return f"""
        - HackerNews:
            - found: True
            - data: 
                - karma: {data.get("karma")}
                - created: {data.get("created")}
                - submissions: {len(data.get("submitted", []))}
                - about: {data.get("about", "")}
"""
    except Exception as e:
        print(f"[ERROR] {"HackerNews"}: {e}")
        return parser.not_found("HackerNews")
        
async def instagram_check(session, username):
    try:
        url = f"https://www.instagram.com/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}

        async with session.get(url, headers=headers, timeout=10) as r:
            text = await r.text()
            soup = BeautifulSoup(text, "html.parser")
            des = soup.find("meta", attrs={"name": "description"})
            if des:
                data =  parser.parse_description(des.get("content")) 
                return f"""
        - Instagram
            - found: True
            - data: {data}"""

            return parser.not_found("Instagram")

    except Exception as e:
        print(f"[ERROR] {"Instagram"}: {e}")
        return parser.not_found("Instagram")



async def linkedin_check(session, username):
    url = "https://v3.scrapetable.com/linkedin/people"
    headers = {
    "Content-Type": "application/json"
    }
    key=settings.SCRAPETABLE_KEY
    params = {
    "key":key ,
    "profileUrl": f"https://www.linkedin.com/in/{username}"
    }
    

    try:
        async with session.get(url, headers=headers,params=params, timeout=10) as r:
            data = await r.json()
            person = data.get("person")
            if not person or r.status == 404:
                return parser.not_found("LinkedIn")

            return f"""
        - LinkedIn
            - found: True
            - data: 
                - full-name: {person.get("fullName")}
                - headline: {person.get("headline")}
                - location: {person.get("geoCity")}
"""
    except Exception as e:
        print(f"[ERROR] {"LinkedIn"}: {e}")
        return parser.not_found("LinkedIn")
    
    
    
async def mastodon_lookup(session, username):
    url = f"https://mastodon.social/api/v1/accounts/lookup?acct={username}"
    headers = {
    "User-Agent": "Mozilla/5.0"
}
    try:
        async with session.get(url, headers=headers,timeout=10) as r:
            if r.status != 200:
                return parser.not_found("Mastodon")
            data = await r.json()
            return f"""
        - Mastodon
            - found: True
            - data: 
                - locked: {data.get("locked")}        
                - url: {data.get("url")}
                - followers: {data.get("followers_count")}
                - following: {data.get("following_count")}
"""
            

    except Exception as e:
        print(f"[ERROR] Mastodon: {e}")
        return parser.not_found("Mastodon")
    



