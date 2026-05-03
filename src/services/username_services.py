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
            p.instagram_check(session,  username),
            p.linkedin_check(session, username),
        ]

        results = await asyncio.gather(*tasks)
        data = ""
        for i in results:
            data+=i

        return f"""
- username: {username}
- platform: {data}
- summary: 
    -total_checked: {len(results)},
        """
        
