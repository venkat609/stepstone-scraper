import requests
from bs4 import BeautifulSoup
import json

url = "https://www.stepstone.de/jobs/werkstudent-software-engineer/in-munich"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
jobs = []

# Find job listing cards on StepStone
for item in soup.find_all('article', class_=lambda x: x and 'res-'.lower() in x.lower())[:10]:
    title_elem = item.find('a', {'data-genesis-element': 'BADGE'}) or item.find('h2')
    if title_elem:
        title = title_elem.get_text(strip=True)
        link = "https://www.stepstone.de" + title_elem.get('href', '') if title_elem.get('href') else ""
        jobs.append({"title": title, "link": link})

print(f"Found {len(jobs)} jobs:")
print(json.dumps(jobs, indent=2))
