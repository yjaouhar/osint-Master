import argparse
import asyncio
from core import ip_lookup as ip 
from core import username_lookup as username
from core import domain_enum as domain
from services import healp
from utils import output as o

# Create argument parser with custom description and formatting
# add_help=False disables the default -h/--help
parser = argparse.ArgumentParser(
    description="Welcome to osintmaster multi-function Tool",
    formatter_class=argparse.RawTextHelpFormatter,
    add_help=False
)

# Create a group for organizing CLI options
group = parser.add_argument_group("OPTIONS")

group.add_argument("-i", "--ip", help='Search information by IP address')
group.add_argument("-u", "--username", help='Search information by username')
group.add_argument("-d", "--domain", help='Enumerate subdomains and check for takeover risks')
group.add_argument("-o", "--output", help='File name to save output')
parser.add_argument("-h","--healp", action="store_true", help="Show help message") # Custom help flag (since default help is disabled)

args = parser.parse_args()
data = ""
if args.ip:
    data = asyncio.run(ip.run(args.ip))    # Run IP lookup asynchronously

elif args.username:
    data = asyncio.run(username.run(args.username))   # Run username lookup asynchronously


elif args.domain:
    data = asyncio.run(domain.run(args.domain))   # Run domain enumeration asynchronously

else:
    healp.show() # If no valid option is provided, show help and exit
    exit()

if data!="":
    print(data)
    if args.output:
        o.export_output(data,args.output)
        print(f"Data saved in {args.output}")