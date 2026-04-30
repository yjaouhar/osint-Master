import ipaddress

def ip_validate(ip):
    try:
        return ipaddress.ip_address(ip)
        
    except ValueError:
        return None