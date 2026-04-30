from utils import validators
from utils import output as out

from services import ip_services as service


async def run(input,output):

    ip = validators.ip_validate(input)
    if ip:
        data = await service.load_data(ip)
        content = out.format_result(data)

        print(content)
        if output:
            out.export_json(content,output)
            print(f"Data saved in {output}")
    else:
        print("Error : Ip not valid '"+input+"'")
