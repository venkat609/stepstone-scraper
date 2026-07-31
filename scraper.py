from curl_cffi import requests
import json

url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    jobs = []
    
    listings = data[1:] if isinstance(data, list) and len(data) > 1 else []
    
    for item in listings:
        title = item.get('position')
        tags = item.get('tags', [])
        location = item.get('location', '')
        
        if title:
            text_check = (title + " " + " ".join(tags) + " " + location).lower()
            
            # Broadened filter to catch general student, engineering, data, and ML listings
            if any(kw in text_check for kw in ['engineer', 'developer', 'student', 'intern', 'analyst', 'data', 'ml', 'software']):
                jobs.append({
                    "title": title,
                    "company": item.get('company'),
                    "location": location if location else "Remote",
                    "link": item.get('url')
                })

    print(f"Found {len(jobs)} matching listings:")
    print(json.dumps(jobs[:10], indent=2))

except Exception as e:
    print(f"Error: {e}")
