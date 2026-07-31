from curl_cffi import requests
from bs4 import BeautifulSoup
import json

url = "https://www.stepstone.de/work/werkstudent-software-engineer-munich"

try:
    # Impersonate chrome to bypass anti-bot protections completely for free
    response = requests.get(url, impersonate="chrome120", timeout=15)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if '/stellenangebote--' in href and len(text) > 5:
            link = "https://www.stepstone.de" + href if not href.startswith('http') else href
            job_item = {"title": text, "link": link}
            if job_item not in jobs:
                jobs.append(job_item)

    print(f"Found {len(jobs)} jobs:")
    print(json.dumps(jobs[:10], indent=2))

except Exception as e:
    print(f"Error: {e}")
