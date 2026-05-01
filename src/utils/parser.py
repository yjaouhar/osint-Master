import re

def parse_description(content):
    followers = re.search(r"(\d+) Followers", content)
    following = re.search(r"(\d+) Following", content)
    posts = re.search(r"(\d+) Posts", content)
    full_name =  re.search(r"-\s*(.*?)\s*\(@", content)
    key = "Instagram: "
    start = content.index(key)
    bio = content[start+len(key):]
    return {
        "followers": followers.group(1) if followers else None,
        "following": following.group(1) if following else None,
        "posts": posts.group(1) if posts else None,
        "full_name" : full_name.group(1) if full_name else None,
        "bio" : bio
    }