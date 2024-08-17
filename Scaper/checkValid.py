import requests
import json
from course_scraper import courseData
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)


# Checks if inputted code exists ()


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
        return courseData(courseCode)


print(checkValid('CSSE1001'))
