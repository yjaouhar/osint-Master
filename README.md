# OSINT-Master 🔍

> **Disclaimer:** This tool is for **educational purposes only**. Always obtain explicit permission before gathering information on any target. Unauthorized use may violate laws such as GDPR, CFAA, and local cybersecurity regulations.

---

## Overview

OSINT-Master is a multi-functional passive reconnaissance tool that collects publicly available information based on IP addresses, usernames, and domains. It is built for security researchers, ethical hackers, and students learning about cybersecurity.

---

## Features

- **IP Lookup** — Geolocation, ISP, ASN, and abuse history
- **Username Search** — Check presence across 5+ platforms (GitHub, LinkedIn, Instagram, HackerNews, Mastodon, Keybase)
- **Domain Enumeration** — Subdomain discovery, IP resolution, SSL certificate details, and subdomain takeover risk detection

---

## Prerequisites

- Python 3.8+
- pip

---

## Installation

```bash
git clone https://github.com/yjaouhar/OSINT-Master
cd osint-master
pip install -r requirements.txt
```

### requirements.txt

```
aiohttp
dnspython
beautifulsoup4
```

---

## Usage

```bash
python src/main.py --help
```

```
Welcome to osintmaster multi-function Tool

OPTIONS:
    -i  "IP Address"       Search information by IP address
    -u  "Username"         Search information by username
    -d  "Domain"           Enumerate subdomains and check for takeover risks
    -o  "FileName"         File name to save output
    --help                 Display this help message
```

---

## Examples

### IP Address Lookup

```bash
python src/main.py -i 8.8.8.8 -o result1.txt
```

```
ISP: Google LLC
City: Mountain View
Country: United States
ASN: 15169
Known Issues: No reported abuse
Data saved in result1.txt
```

**Data sources used:** ip-api.com, AbuseIPDB

---

### Username Search

```bash
python src/main.py -u "johndoe" -o result2.txt
```

```
GitHub: Found
  - Full Name: John Doe
  - Followers: 42
  - Repos: 17
  - Bio: Software Engineer

HackerNews: Found
  - Karma: 312
  - Submissions: 5
  - Joined: 2021-04-10

LinkedIn: Found
  - Full Name: John Doe
  - Headline: Backend Developer | Python | Go
  - Location: Casablanca, Morocco

Instagram: Not Found

Mastodon: Found
  - URL: https://mastodon.social/@johndo
  - Followers: 8
  - Following: 21

Recent Activity: Active on GitHub, last push 2 days ago
Data saved in result2.txt
```

**Platforms checked:** GitHub, HackerNews, LinkedIn, Instagram, Mastodon, Keybase

---

### Domain & Subdomain Enumeration

```bash
python src/main.py -d "example.com" -o result3.txt
```

```
Main Domain: example.com

Subdomains found: 3
  - www.example.com (IP: 93.184.216.34)
    SSL Certificate: Valid until 2026-07-01
  - mail.example.com (IP: 93.184.216.34)
    SSL Certificate: Valid until 2026-07-01
  - test.example.com (IP: N/A)
    SSL Certificate: Not found

Potential Subdomain Takeover Risks:
  - Subdomain: test.example.com
    CNAME record points to a non-existent AWS S3 bucket
    Recommended Action: Remove or update the DNS record to prevent potential misuse

Data saved in result3.txt
```

**Data sources used:** crt.sh, AlienVault OTX, HackerTarget, RapidDNS, URLScan, CertSpotter

---

## Project Structure

```
OSINT-master/
├── src
|    ├── main.py
|    ├── config
|    │   ├── constants.py
|    │   └── settings.py
|    ├── core
|    │   ├── domain_enum.py
|    │   ├── ip_lookup.py
|    │   └── username_lookup.py
|    ├── services
|    │   ├── domain_services.py
|    │   ├── ip_services.py
|    │   └── username_services.py
|    └── utils
|        ├── domain.py
|        ├── http.py
|        ├── output.py
|        ├── parser.py
|        ├── platforms.py
|        └── validators.py
├── output
├── README.md
└── requirements.txt

```

---

## API Configuration

Most features work without API keys. For extended functionality:

| Service | Required | Free Tier | Used For |
|---|---|---|---|
| ip-api.com | No | Yes (45 req/min) | IP geolocation |
| AbuseIPDB | Optional | Yes (1000 req/day) | IP abuse history |
| VirusTotal | Optional | Yes (500 req/day) | Extra subdomains |
| Scrapetable | Optional | Paid | LinkedIn data |

To configure API keys, create a `.env` file:

```env
ABUSEIPDB_KEY=your_key_here
VIRUSTOTAL_KEY=your_key_here
SCRAPETABLE_KEY=your_key_here
```

---

## How Subdomain Takeover Detection Works

A subdomain takeover occurs when a subdomain's DNS record (usually a CNAME) points to an external service (like AWS S3, GitHub Pages, Heroku) that no longer exists or is unclaimed. An attacker can register that service and serve malicious content under the legitimate domain.

**Detection method:**

1. Resolve the subdomain's CNAME record
2. Check if the CNAME points to a known vulnerable service (AWS, GitHub Pages, Heroku, Netlify, Vercel, etc.)
3. Send an HTTP request to the subdomain and check if the response body contains a known error fingerprint (e.g., `NoSuchBucket`, `There isn't a GitHub Pages site here`)
4. If both conditions match → flag as vulnerable

**Mitigation:**

- Remove unused DNS records immediately
- Regularly audit CNAME records for dangling pointers
- Monitor your subdomains with automated tools

---

## Ethical & Legal Considerations

- **Get Permission:** Only use this tool on systems you own or have explicit written permission to test.
- **Respect Privacy:** Do not store or share personal data beyond what is needed.
- **Follow the Law:** Adhere to GDPR, CFAA, and your local cybersecurity laws.
- **Report Responsibly:** If you find vulnerabilities, notify the affected party privately before any public disclosure.
- **Educational Use Only:** This tool is designed for learning. Misuse is the sole responsibility of the user.

---

## Known Limitations

- Instagram data is retrieved via HTML scraping and may break if Instagram changes its page structure.
- LinkedIn data requires a paid Scrapetable API key for full results.
- crt.sh applies rate limiting — the tool uses multiple fallback sources (AlienVault, RapidDNS, etc.) to compensate.
- Some subdomains using self-signed or no SSL certificates will not appear in certificate transparency logs.
- Subdomain takeover detection only covers CNAME-based takeovers for known services.

---

## Troubleshooting

**Getting 403 from a platform:**
Some platforms block automated requests. The tool uses browser-like User-Agent headers to minimize this. If the issue persists, add a delay between requests.

**DNS resolution errors:**
Make sure `dnspython` is installed:

```bash
pip install dnspython
```

---

## License

This project is for educational use only. See `LICENSE` for details.
