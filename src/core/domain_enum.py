from services import domain_services 
from utils import output as o
async def run(domain , output):
    results = await domain_services.load_data(domain)
    data = o.format_output(domain, results)
    print(data)
    if output:
        o.export_output(data,output)
        print(f"Data saved in {output}")