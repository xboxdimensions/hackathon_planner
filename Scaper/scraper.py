import requests
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)
code = 2497
url = f"https://my.uq.edu.au/programs-courses/requirements/program/{code}/2024"

response = requests.get(url, headers=headers)
text = response.text
text = str(text)
# text = "programRequirements:" +
text = text.split("programRequirements: ")[1]
text = text.split(",\n routes: ")[0]
print(text)
