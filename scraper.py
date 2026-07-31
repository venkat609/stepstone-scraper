from curl_cffi import requests
import json

# Public tech and engineering API endpoint
url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    jobs = []
    
    # Skip the first metadata element
    listings = data[1:] if isinstance(data, list) and len(data) > 1 else []
    
    # Target keywords matching your exact background requirements
    target_keywords = [
        'elektrotechnik', 'electrical', 'computer engineering', 'data engineer', 
        'machine learning', 'ml engineer', 'data analyst', 'battery', 'storage', 
        'solar', 'motor', 'energy', 'bess', 'power', 'grid'
    ]
    
    for item in listings:
        title = item.get('position')
        tags = item.get('tags', [])
        location = item.get('location', '')
        
        if title:
            text_check = (title + " " + " ".join(tags) + " " + location).lower()
            # Match if it contains engineering/data roles AND energy/battery/solar domain terms
            if any(kw in text_check for kw in ['engineer', 'developer', 'student', 'intern', 'analyst', 'data', 'ml']) and \
               any(domain in text_check for domain in ['battery', 'storage', 'solar', 'energy', 'motor', 'power', 'grid', 'elektrotechnik']):
                jobs.append({
                    "title": title,
                    "company": item.get('company'),
                    "location": location if location else "Germany / Remote",
                    "link": item.get('url')
                })

    print(f"Found {len(jobs)} targeted Energy/Battery/Data student listings:")
    print(json.dumps(jobs[:10], indent=2))

except Exception as e:
    print(f"Error: {e}")
