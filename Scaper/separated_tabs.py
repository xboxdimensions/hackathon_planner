import requests
import json
from courseData import relatedCourses, sidebar, UnitAmount, durationLength, offerings
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

program_code = 2451

# Use indexing on returned list to generate tabs. Does not include plans, nor specifies individual parts of the tab


def seperatedTabs(program_code) -> list[list[str]]:
    url = f"https://my.uq.edu.au/programs-courses/requirements/program/{
        program_code}/2024"
    response = requests.get(url, headers=headers)
    text = response.text
    text = str(text)
    text = text.split("programRequirements: ")[1]
    text = text.split(",\n routes: ")[0]
    options = []
    data = json.loads(text)
    with open("Scaper\\temp.json", "w") as f:
        f.write(str((text)))

    with open("Scaper\\temp.json", "r") as f:
        data = json.loads(f.read())
        # rules = data['payload']['components'][1]['payload']['header']
        for x in range(len(data['payload']['components'][1]['payload']['body'])):
            parts = []
            l = data['payload']['components'][1]['payload']['body'][x]['body']
            for entries in l:
                if entries.get("body"):
                    for item in entries['body']:
                        if item.get('rowType') and item['rowType'] == "EquivalenceGroup":
                            empty = []
                            for course in item['equivalenceGroup']:
                                code = course['curriculumReference']['code']
                                if not any(code in
                                           sublist for sublist in options):
                                    empty.append(
                                        code)
                            parts.append(empty)
                        elif item.get('body'):
                            parts.append(
                                item['body'][0]['curriculumReference']['code'])

                        else:
                            parts.append(item['curriculumReference']['code'])
                elif entries['rowType'] == "EquivalenceGroup":
                    empty = []
                    for course in entries['equivalenceGroup']:
                        code = course['curriculumReference']['code']
                        if not any(code in
                                   sublist for sublist in options):
                            empty.append(
                                code)
                    parts.append(empty)
                elif entries["rowType"] == "WildCardItem":
                    print("general elective moment")
                else:
                    if entries['curriculumReference']['code'].isdigit():
                        pass
                    else:
                        parts.append(entries['curriculumReference']['code'])
            options.append(parts)
    return options
