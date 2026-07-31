from curl_cffi import requests
import json

url = "https://hacker-news.firebaseio.com/v0/topstories.json"

try:
    response = requests.get(url, impersonate="chrome120", timeout=15)
    print(f"Status Code: {response.status_code}")
    
    # Increase the search pool to 30 stories
    story_ids = response.json()[:30]
    jobs = []
    
    for story_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item_res = requests.get(item_url, impersonate="chrome120", timeout=5)
        item_data = item_res.json()
        
        if item_data and 'title' in item_data:
            title = item_data['title']
            # Pull any tech, hiring, or software related posts
            if any(keyword in title.lower() for keyword in ['hiring', 'engineer', 'developer', 'software', 'tech', 'remote', 'ai']):
                jobs.append({
                    "title": title,
                    "link": item_data.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                })

    # Fallback to general top stories if keyword match is low
    if not jobs and story_ids:
        for story_id in story_ids[:5]:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            item_res = requests.get(item_url, impersonate="chrome120", timeout=5)
            item_data = item_res.json()
            if item_data and 'title' in item_data:
                jobs.append({
                    "title": item_data['title'],
                    "link": item_data.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                })

    print(f"Found {len(jobs)} listings:")
    print(json.dumps(jobs[:10], indent=2))

except Exception as e:
    print(f"Error: {e}")
