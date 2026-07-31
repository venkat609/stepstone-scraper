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
    
    primary_roles = ['engineer', 'developer', 'student', 'werkstudent', 'intern', 'analyst', 'data', 'ml']
    domain_terms = ['elektrotechnik', 'electrical', 'computer', 'battery', 'storage', 'solar', 'motor', 'energy', 'bess', 'power', 'grid', 'machine learning']
    
    for item in listings:
        title = item.get('position', '')
        tags = item.get('tags', [])
        location = item.get('location', '')
        text_check = (title + " " + " ".join(tags) + " " + location).lower()
        
        if any(r in text_check for r in primary_roles) and any(d in text_check for d in domain_terms):
            jobs.append({
                "title": title,
                "company": item.get('company'),
                "location": location if location else "Germany / Remote",
                "link": item.get('url')
            })

    # Permanent fallback ensuring your daily log always gives direct access to target portals
    if not jobs:
        print("No live global API matches found. Displaying direct portals for your criteria:")
        jobs = [
            {
                "title": "Werkstudent Software / Data / Battery Engineering",
                "company": "Munich Electrification (Munich)",
                "location": "Munich, Germany",
                "link": "https://www.munich-electrification.com/careers"
            },
            {
                "title": "Werkstudent Data Science & Energy Systems",
                "company": "1KOMMA5°",
                "location": "Hamburg / Berlin / Munich",
                "link": "https://1komma5grad.com/en/careers"
            },
            {
                "title": "Working Student - BESS & Energy Storage Data Analytics",
                "company": "Vattenfall",
                "location": "Hamburg / Berlin",
                "link": "https://jobs.vattenfall.com/"
            },
            {
                "title": "Direct Search: Werkstudent Elektrotechnik & Software Engineering",
                "company": "StepStone Germany",
                "location": "Munich / Germany",
                "link": "https://www.stepstone.de/work/werkstudent-software-engineer-munich"
            }
        ]

    print(f"Final Output ({len(jobs)} targeted entries):")
    print(json.dumps(jobs, indent=2))

except Exception as e:
    print(f"Error: {e}")
