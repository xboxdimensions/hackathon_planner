"""
Checks if course code exists
"""

import requests
import json
from course_scraper import courseData
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

def isCourseCodeValid(courseCode: str) -> dict:
    """Checks if a course code is valid to be looked up via api

    takes in course code string returns dictionary of course data if exists else {}
    """

    url = f"https://my.uq.edu.au/programs-courses/course.html?course_code={
        courseCode}"
    text = str(requests.get(url, headers=headers).text) # Get the page of the cours

    if ("This course is not currently offered, please contact the school or faculty of your program."
            in text or "The course you requested could not be found." in text):
        return {} # The course doesn't exist / isn't offerred
    else:
        return courseData(courseCode) # return the course data
