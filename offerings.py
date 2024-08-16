from course_scraper import course_finder
import requests

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)
courses = course_finder(2460)


def offerings(courses):
    sems = {}
    for courseCode, courseName in courses.items():
        offerings = []
        url = f"https://my.uq.edu.au/programs-courses/course.html?course_code={
            courseCode}"
        response = requests.get(url, headers=headers)
        text = response.text
        text = str(text)
        rangeS = text.find("Current course offerings</h1>")
        text = text[rangeS:]
        rangeE = text.find("<!--")
        text = text[:rangeE]
        if "Semester 1" in text:
            offerings.append("Semester 1")
        if "Semester 2" in text:
            offerings.append("Semester 2")
        if "Summer Semester" in text:
            offerings.append("Summer Semester")
        sems[courseCode] = offerings
    return sems
