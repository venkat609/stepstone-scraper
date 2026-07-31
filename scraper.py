import requests
from bs4 import BeautifulSoup
import json

url = "https://www.stepstone.de/jobs/werkstudent-software-engineer/in-munich"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print(f"Status Code: {response.status_code}")
