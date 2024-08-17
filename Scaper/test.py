
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup



def scrapePlansAndCore(program_code: str) -> dict:
	headers = requests.utils.default_headers()
	headers.update(
		{
			'User-Agent': 'My User Agent 1.0',
		}
	)

	url = f"https://my.uq.edu.au/programs-courses/requirements/program/{
		program_code}/2024"
	html = requests.get(url, headers=headers).text
	out = html
	s = out
	out = out.split("programRequirements: ")[1]
	out = out.split(",\n routes: ")[0]

	j = json.loads(out)
	if not j:
		return dict()
	# pprint(j['payload']['components'][1]['payload'])
	# out = json.loads(out)
	with open("output.txt", "w") as f:
		json.dump(j['payload']['components'][1]['payload'], f)

	payload = j['payload']['components'][1]['payload']['body']
	content = [tab['body'] for tab in payload]

	data = {'core': set(), 'electives': set(), 'plans': set()}
	for i, tab in enumerate(content):
		tab_courses = set()
		if tab:
			for course in tab:
				if 'curriculumReference' in course:
					# a single course
					tab_courses.add(course['curriculumReference']['code'])
				elif 'equivalenceGoup' in course:
					# a choice
					tab_courses.add(set(choice for choice in course['equivalenceGroup']))
				else:
					pprint(course)
					pass # RANDOM ELECTIVES TODO
		if i == 0:
			data['core'] = tab_courses
		if tab_courses and len(list(tab_courses)[0]) == 10:
			data['plans'] = tab_courses
		else:
			data['electives'].union(tab_courses)
	return data

pprint(scrapePlansAndCore('2451'))