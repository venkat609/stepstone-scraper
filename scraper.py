import requests
from bs4 import BeautifulSoup
import json

url = "https://www.stepstone.de/jobs/werkstudent-software-engineer/in-munich"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
jobs = []

# Broaden search to find job listing links directly
for item in soup.find_all('article'):
    title_elem = item.find('a')
    if title_elem and title_elem.get('href') and '/stellenangebote--' in title_elem.get('href'):
        title = title_elem.get_text(strip=True)
        link = "https://www.stepstone.de" + title_elem.get('href') if not title_elem.get('href').startswith('http') else title_elem.get('href')
        if title and {"title": title, "link": link} not in jobs:
            jobs.append({"title": title, "link": link})

print(f"Found {len(jobs)} jobs:")
print(json.dumps(jobs[:10], indent=2))
