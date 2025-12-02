import requests

def extract_domains(data):
    domains = []
    if isinstance(data, dict):
        for key in ["domain", "domain_suffix", "domain_keyword"]:
            if key in data:
                value = data[key]
                if isinstance(value, list):
                    domains.extend([v.strip() for v in value if v.strip()])
                elif isinstance(value, str):
                    domains.append(value.strip())
        if "domain_regex" in data:
            value = data["domain_regex"]
            if isinstance(value, list):
                domains.extend([f"/{v.strip()}/" for v in value if v.strip()])
            elif isinstance(value, str):
                domains.append(f"/{value.strip()}/")
    elif isinstance(data, list):
        for item in data:
            domains.extend(extract_domains(item))
    return domains

urls = [
    "https://raw.githubusercontent.com/jackszb/sukka-surge/main/domainset/reject.json",
    "https://raw.githubusercontent.com/jackszb/sukka-surge/main/domainset/reject_extra.json",
    "https://raw.githubusercontent.com/jackszb/sukka-surge/main/domainset/reject_phishing.json"
]

all_domains = []

for url in urls:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch: {url}")
        continue
    data = response.json()
    if "rules" in data:
        for rule in data["rules"]:
            all_domains.extend(extract_domains(rule))

all_domains = list(set([d.strip() for d in all_domains if d.strip()]))

adguard_list = []
for domain in all_domains:
    if domain.startswith("||") or domain.startswith("@@") or domain.startswith("/") or "*" in domain:
        adguard_list.append(domain)
    else:
        adguard_list.append(f"||{domain}^")

with open("domains.adblock", "w") as f:
    for item in sorted(adguard_list):
        f.write(item + "\n")

print("AdGuard file generated: domains.adblock")
