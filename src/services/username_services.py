from utils import platforms as p
import json

import asyncio
import aiohttp
async def load_data(username):
    async with aiohttp.ClientSession() as session:
        
        tasks = [
            p.github_lookup(session, username),
            p.hackerNews_lookup(session, username),
            p.mastodon_lookup(session, username),
            p.instagram_check(session,  f"https://www.instagram.com/{username}"),
            p.linkedin_check(session, username),
        ]

        results = await asyncio.gather(*tasks)

        return {
            "username": username,
            "platforms": results,
            "summary": {
                "total_checked": len(results),
                "most_active": "GitHub"
            }
        }
        
