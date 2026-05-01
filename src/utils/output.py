from config import constants as const
import json


def format_result(data):
    
    org = data.get("isp", "")
    parts = org.split(" ", 1)
    asn = parts[0] if parts else "Unknown"
    isp = parts[1] if len(parts) > 1 else org
    city = data.get("city", "Unknown")
    country = data.get("country", "Unknown")

    abuse_score = data.get("abuse_score")
    total_reports = data.get("total_reports")

    blacklist = data.get("blacklist")

    # ---- clean abuse ----
    if abuse_score is None or abuse_score == 0:
        abuse_text = "No reported abuse"
    else:
        abuse_text = f"Yes ({abuse_score}) reports"

    # ---- blacklist ----
    if blacklist is True:
        blacklist_text = "BLACKLISTED"
    else:
        blacklist_text = "Clean"

    return f"""
        ISP: {isp}
        City: {city}
        Country: {country}
        ASN: {asn}
        Known Issues: {abuse_text}
        Blacklist: {blacklist_text}
        """.strip()



def export_output(data, filename):
    const.OUTPUT_DIR.mkdir(exist_ok=True)
    file_path = const.OUTPUT_DIR / filename
    file_path.write_text(data)