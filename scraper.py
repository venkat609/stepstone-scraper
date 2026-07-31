import requests
from bs4 import BeautifulSoup
import json

url = "https://www.stepstone.de/work/werkstudent-software-engineer-munich"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
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
