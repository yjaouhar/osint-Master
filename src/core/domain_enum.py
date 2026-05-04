from services import domain_services 
from utils import output as o
async def run(domain):
    results = await domain_services.load_data(domain)
    return o.format_output(domain, results)
    