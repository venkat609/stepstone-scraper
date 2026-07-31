import requests
from bs4 import BeautifulSoup
import json

url = "https://www.stepstone.de/jobs/werkstudent-software-engineer/in-munich"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # Strict 10-second timeout prevents the action from hanging
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []
        
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'ItemList':
                    for element in data.get('itemListElement', []):
                        item = element.get('item', {})
                        jobs.append({
                            "title": item.get('title'),
                            "link": item.get('url')
                        })
            except Exception:
                pass
                
        print(f"Found {len(jobs)} structured jobs:")
        print(json.dumps(jobs[:10], indent=2))
    else:
        print("Blocked or redirected by anti-bot protection.")

except requests.exceptions.Timeout:
    print("Request timed out safely.")
