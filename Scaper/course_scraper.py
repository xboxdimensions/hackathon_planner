import requests
from Scaper.courseData import relatedCourses, sidebar, UnitAmount, durationLength, offerings, preqs, name

import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup


headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)
num = [1602, 2000, 2007, 2031, 2033, 2040, 2041, 2052, 2063, 2066, 2102, 2129, 2131, 2132, 2139, 2140, 2142, 2171, 2175, 2180, 2181, 2235, 2237, 2241, 2243, 2252, 2253, 2261, 2264, 2266, 2290, 2293, 2298, 2299, 2306, 2312, 2316, 2317, 2320, 2334, 2335, 2336, 2337, 2338, 2339, 2350, 2354, 2355, 2357, 2367, 2368, 2369, 2370, 2371, 2372, 2373, 2376, 2378, 2379, 2380, 2381, 2382, 2387, 2388, 2392, 2405, 2413, 2414, 2415, 2417, 2419, 2420, 2421, 2422, 2423, 2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471, 2472, 2473, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2481, 2482, 2483, 2484, 2485, 2486, 2487, 2488, 2489, 2490, 2491, 2492, 2493, 2494, 2495, 2496, 2497, 2498, 2499, 2500, 2501, 2502, 2503, 2504, 2505, 2506, 2507, 2508, 2509, 2510, 2511, 2512, 2514, 2515, 2516, 2517, 2519, 2521, 2522, 2524, 2525, 2526, 2527, 2528, 2529, 2530, 2531, 5007, 5010, 5013, 5015, 5025, 5028, 5033, 5036, 5040, 5042, 5068,
       5077, 5079, 5084, 5086, 5090, 5096, 5116, 5119, 5127, 5131, 5145, 5147, 5151, 5164, 5181, 5188, 5193, 5199, 5221, 5228, 5229, 5240, 5248, 5251, 5255, 5257, 5267, 5290, 5299, 5319, 5326, 5333, 5336, 5341, 5343, 5364, 5365, 5368, 5369, 5370, 5398, 5399, 5420, 5429, 5430, 5444, 5448, 5454, 5463, 5473, 5478, 5479, 5491, 5497, 5498, 5500, 5519, 5520, 5522, 5523, 5527, 5528, 5530, 5533, 5535, 5547, 5550, 5551, 5556, 5557, 5558, 5559, 5560, 5561, 5562, 5564, 5565, 5566, 5571, 5573, 5576, 5580, 5581, 5583, 5584, 5585, 5590, 5591, 5592, 5596, 5597, 5598, 5599, 5600, 5602, 5607, 5609, 5610, 5616, 5625, 5627, 5641, 5643, 5646, 5648, 5650, 5651, 5660, 5666, 5677, 5678, 5681, 5682, 5683, 5684, 5685, 5688, 5689, 5690, 5692, 5695, 5703, 5704, 5705, 5706, 5708, 5711, 5712, 5718, 5722, 5725, 5726, 5728, 5729, 5730, 5734, 5736, 5737, 5738, 5739, 5740, 5741, 5742, 5743, 5744, 5745, 5746, 5747, 5748, 5749, 5750, 5751, 5752, 5753, 5754, 5755, 5759, 5760, 5761, 5763, 5764, 5765, 5766, 5767, 5771]


""" course_scraper.py

course_finder

plan_finder

courseData

checkValid

getNames

"""
# FUNCTION 1) GIVE programCode - return (courses, plans)


def scrapePlansAndCore(program_code: str) -> dict:
    print(program_code)
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'My User Agent 1.0'})
    url = f"https://my.uq.edu.au/programs-courses/requirements/program/{program_code}/2024"
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
    # with open("output.txt", "w") as f:
    #     json.dump(j['payload']['components'][1]['payload'], f)

    payload = j['payload']['components'][1]['payload']['body']
    content = [tab['body'] for tab in payload]

    data = {'core': set(), 'electives': set(), 'plans': set()}
    for i, tab in enumerate(content):
        if len(tab) > 1:
            if 'body' in tab[1]:
                # there are sub sub sections
                tab = tab[0]['body']
        tab_courses = set()
        if tab:

            for course in tab:
                print("------")
                print(course)
                print("------")
                if 'rowType' not in course:
                    # print(course)
                    continue
                # print(course)
                # print()
                # print(course['rowType']) #, course['name'])
                # try:
                #     print(course['equivalenceGroup'])
                #     print(course['rowType'] == "EquivalenceGroup")
                # except:
                #     pass
                if course['rowType'] == "CurriculumReference":
                    # a single course
                    # print(course['curriculumReference']['code'])
                    print("=" * 10)
                    print(course['curriculumReference']['code'])
                    print("=" * 10)
                    tab_courses.add(course['curriculumReference']['code'])
                elif course['rowType'] == "EquivalenceGroup":
                    # a choice
                    tab_courses.add(tuple(choice['curriculumReference']['code'] for choice in course['equivalenceGroup']))
                else:
                    pass # wild card items
        print(tab_courses)
        if i == 0:
            data['core'] = tab_courses
        if tab_courses and len(list(tab_courses)[0]) == 10:
            data['plans'] = tab_courses
        elif tab_courses:
            for course in tab_courses:
                if course not in data['core'] and len(course) == 8:
                    data['electives'].add(course)
    print(data['electives'])           
    return {key : list(s) for key, s in data.items()}
# def course_finder(program_code: int) -> tuple[dict, dict]:
#     """
#     Gets basic course information in one lookup

#     Takes in a program_code returns two dictionaries
#     """
#     courses = dict()
#     plans = dict()

#     # Go to course requirements page
#     url = f"https://my.uq.edu.au/programs-courses/requirements/program/{
#         program_code}/2024"
    # response = requests.get(url, headers=headers)
    # text = response.text
    # text = str(text)
    # delimter = text.split('"')
    # last_key = None
    # for index, text in enumerate(delimter):
    #     if text[0:4].isalpha() and text[5:9].isdigit():
    #         courses[text] = {}
    #     if text[0:6].isalpha() and text[6:11].isdigit():
    #         plans[text] = {}
    #         last_key = text
    #     if delimter[index-2] == "name" and delimter[index-1] == ":" and last_key != None:
    #         plans[last_key]["Name"] = text
    #         last_key = None
    #     if delimter[index-2] == "subtype" and delimter[index-1] == ":" and last_key != None:
    #         plans[last_key]["Subtype"] = text

# FUNCTION 2) input plans (see above) return courses (like above)


def plan_finder(planCode: str) -> dict[str]:
    courses = {}
    url = f"https://my.uq.edu.au/programs-courses/requirements/plan/{
        planCode}/2024"
    response = requests.get(url, headers=headers)
    text = response.text
    text = str(text)
    codes = text.split('"code":')[1:]
    for t in codes:
        if t[5:9].isdigit():
            index = t.find('fromTerm')-3
            # end = t.find('",', index)
            i = t.find(',"name":"')+9
            courses[t[1:9]] = {}
    return courses

# FUNCTION 3) give courses (see above) and returns data


def courseData(coursesList: list) -> dict:
    courses = {course: dict() for course in coursesList}
    for courseCode in courses.keys():
        print("Now on " + courseCode)
        url = f"https://my.uq.edu.au/programs-courses/course.html?course_code={
            courseCode}"
        response = requests.get(url, headers=headers)
        text = response.text
        text = str(text)
        courses[courseCode]["Name"] = name(text)
        courses[courseCode]["Offerings"] = offerings(text)
        courses[courseCode]["Units"] = UnitAmount(text)
        courses[courseCode]["Duration"] = durationLength(text)
        courses[courseCode]["Prerequisite"] = preqs(text)
        for filter, header in relatedCourses.items():
            courses[courseCode][header] = sidebar(text, filter)

    return courses


# print(courseData(["INFS1200", "DECO1400"]))
# Checks if inputted code exists or returns false


def checkValid(courseCode):
    url = f"https://my.uq.edu.au/programs-courses/course.html?course_code={
        courseCode}"
    response = requests.get(url, headers=headers)
    text = response.text
    text = str(text)
    if ("This course is not currently offered, please contact the school or faculty of your program."
            in text or "The course you requested could not be found." in text):
        return False
    else:
        rangeS = text.find('<h1 id="course-title">')+22
        text = text[rangeS:]
        rangeE = text.find('</h1>')
        text = text[:rangeE]
        text = text.split(" ")
        name = " ".join(text[0:-1])
        code = text[-1]
        code = code[1:-1]
        courses = {}
        courses[code] = {}
        courses[code]["Name"] = name
        return courseData(courses)


def getNames(num: list[int]) -> dict[str:int]:
    with open("courseNames.json", "w") as f:
        names = {}
        for code in num:
            url = f"https://my.uq.edu.au/programs-courses/requirements/program/{
                code}/2024"
            response = requests.get(url, headers=headers)
            text = response.text
            text = str(text)
            try:
                text = text.split('"authorGivenName":"')[1]
                text = text.split('"name":"')[1]
                text = text.split('","template')[0]
                text = text.replace("\\", "")
                names[code] = text
            except IndexError:
                continue
        f.write(str(names))
