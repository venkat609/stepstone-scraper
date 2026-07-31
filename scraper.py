from curl_cffi import requests
import json

# Public tech and startup job board API
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
    
    # Strict matching parameters for your background
    primary_roles = ['engineer', 'developer', 'student', 'werkstudent', 'intern', 'analyst', 'data', 'ml']
    domain_terms = ['elektrotechnik', 'electrical', 'computer', 'battery', 'storage', 'solar', 'motor', 'energy', 'bess', 'power', 'grid', 'machine learning']
    
    for item in listings:
        title = item.get('position', '')
        tags = item.get('tags', [])
        location = item.get('location', '')
        
        text_check = (title + " " + " ".join(tags) + " " + location).lower()
        
        # Must contain a core student/engineering role AND at least one domain keyword
        has_role = any(r in text_check for r in primary_roles)
        has_domain = any(d in text_check for d in domain_terms)
        
        if has_role and has_domain:
            jobs.append({
                "title": title,
                "company": item.get('company'),
                "location": location if location else "Germany / Remote",
                "link": item.get('url')
            })

    print(f"Found {len(jobs)} specialized listings:")
    print(json.dumps(jobs[:10], indent=2))

except Exception as e:
    print(f"Error: {e}")
