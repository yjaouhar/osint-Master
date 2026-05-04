from services import username_services as service
from utils import output as out
import json

async def run(username ):
          return await service.load_data(username)
          
            
