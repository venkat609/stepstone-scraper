from curl_cffi import requests
import json

# Target StepStone's internal search query endpoint parameter pattern
url = "https://www.stepstone.de/candidate/search/results?what=Werkstudent%20Software%20Engineer&where=M%C3%BCnchen"

headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    # Extract listings if returned in JSON structure
    listings = data.get('listings', []) or data.get('jobs', [])
    
    jobs = []
    for item in listings[:10]:
        title = item.get('title') or item.get('headline')
        job_id = item.get('id') or item.get('objectId')
        link = f"https://www.stepstone.de/stellenangebote--{job_id}" if job_id else ""
        if title:
            jobs.append({"title": title, "link": link})

    print(f"Found {len(jobs)} jobs via API:")
    print(json.dumps(jobs, indent=2))

except Exception as e:
    print(f"API fallback format parsing, error: {e}")
