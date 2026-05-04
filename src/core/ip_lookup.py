from utils import validators
from utils import output as out

from services import ip_services as service

# Define an asynchronous function that takes user input (expected to be an IP)
async def run(input):

    ip = validators.ip_validate(input)

    if ip:
        # Call an async function to fetch data related to the IP
        # (likely from an API or database)
        data = await service.load_data(str(ip))

        return out.format_result(data)

    else:
        print("Error : Ip not valid '" + input + "'")