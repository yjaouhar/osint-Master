from config import constants as const
import json


def format_result(data):
    # ipinfo returns the ASN and provider in one field like "AS123 Example ISP".
    org = data.get("isp", "")
    parts = org.split(" ", 1) if org else []
    asn = parts[0] if parts else "Unknown"
    isp = parts[1] if len(parts) > 1 else org
    city = data.get("city", "Unknown")
    country = data.get("country", "Unknown")

    abuse_score = data.get("abuse_score")
    total_reports = data.get("total_reports")


    # ---- clean abuse ----
    if abuse_score is None or abuse_score == 0:
        abuse_text = "No reported abuse"
    else:
        abuse_text = f"This IP was reported {total_reports} times. Confidence of Abuse is {abuse_score}%:"

    return f"""
ISP: {isp}
City: {city}
Country: {country}
ASN: {asn}
Known Issues: {abuse_text}
        """.strip()


def format_output(domain, results):
    lines = [f"Main Domain: {domain}\n", f"Subdomains found: {len(results)}"]
    
    for r in results:
        lines.append(f"  - {r['sub']} (IP: {r['ip']})")
        lines.append(f"    SSL Certificate: {r['ssl']}")
    
    # Only keep subdomains that matched a known provider fingerprint during takeover checks.
    risks = [r for r in results if r["risk"]]
    lines.append("\nPotential Subdomain Takeover Risks:")
    if risks:
        for r in risks:
            lines.append(f"  - Subdomain: {r['sub']}")
            lines.append(f"    CNAME points to a non-existent {r['risk']}")
            lines.append(f"    Recommended Action: Remove or update the DNS record")
    else:
        lines.append("  None detected")
    
    return "\n".join(lines)

    



def export_output(data, filename):
    const.OUTPUT_DIR.mkdir(exist_ok=True)
    file_path = const.OUTPUT_DIR / filename
    file_path.write_text(data)
