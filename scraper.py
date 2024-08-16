import requests
from bs4 import BeautifulSoup

code = 2497
url = f"https://my.uq.edu.au/programs-courses/requirements/program/{code}/2024"

response = requests.get(url)

print(response)
