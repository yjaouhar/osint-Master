import argparse
import asyncio
from core import ip_lookup as ip 
from core import username_lookup as username
from core import domain_enum as domain



parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-i", "--ip", help="IP address" )
group.add_argument("-u", "--username", help="Username")
group.add_argument("-d", "--domain", help="Domain")

parser.add_argument("-o", "--output", help="Output file")

args = parser.parse_args()
if args.ip:
    asyncio.run(ip.run(args.ip, args.output))
elif args.username:
    asyncio.run(username.run(args.username, args.output))
elif args.domain:
    asyncio.run(domain.run(args.domain, args.output))