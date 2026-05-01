from services import username_services as service
from utils import output as out
import json

async def run(username , output):
            data = await service.load_data(username)
            print(data)
            if output:
                out.export_output(str(data),output)
            
