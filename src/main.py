import argparse
import asyncio
from core import ip_lookup as ip 
from core import username_lookup as username
from core import domain_enum as domain



parser = argparse.ArgumentParser(
    description="Welcome to osintmaster multi-function Tool",
    formatter_class=argparse.RawTextHelpFormatter
)

group = parser.add_argument_group("OPTIONS")

group.add_argument("-i", "--ip", help='Search information by IP address')
group.add_argument("-u", "--username", help='Search information by username')
group.add_argument("-d", "--domain", help='Enumerate subdomains and check for takeover risks')
group.add_argument("-o", "--output", help='File name to save output')

args = parser.parse_args()

args = parser.parse_args()
if args.ip:
    asyncio.run(ip.run(args.ip, args.output))
elif args.username:
    asyncio.run(username.run(args.username, args.output))
elif args.domain:
    asyncio.run(domain.run(args.domain, args.output))
