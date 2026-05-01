from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2] 
OUTPUT_DIR = BASE_DIR / "output"
# PLATFORMS = {
#     "github": "https://api.github.com/users/{}",
#     "reddit": "https://www.reddit.com/user/{}/about.json",
#     "twitter": "https://twitter.com/{}",
#     "instagram": "https://www.instagram.com/{}",
#     "linkedin": "https://www.linkedin.com/in/{}"
# }