relatedCourses = {'course-incompatible">': 'Incompatible',
                  'course-companion">': "Companion",
                  'recommended-prerequisite">': "RecommendPreq"}


def name(text: str):
    rangeS = text.find('<h1 id="course-title">')+22
    text = text[rangeS:]
    rangeE = text.find('</h1>')
    text = text[:rangeE]
    text = text.split(" ")
    return " ".join(text[0:-1])


def preqs(text: str):
    coursesFound = []
    rangeS = text.find('course-prerequisite">')+21
    if rangeS == 20:
        return coursesFound
    text = text[rangeS:]
    rangeE = text.find("</p>")
    text = text[:rangeE]
    if "grade" in text:
        return ""

    first = text.split(" and ")
    for x in first:
        x = x.removeprefix("(")
        x = x.removesuffix(")")
        coursesFound.append(tuple(x.split(" or ")))
    return coursesFound


def UnitAmount(text: str) -> str:
    rangeS = text.find('course-units">')+14
    text = text[rangeS:]
    rangeE = text.find('</p>')
    return text[:rangeE]


def durationLength(text: str) -> str:
    if "One" in text:
        return "1"
    elif "Two" in text:
        return "2"
    else:
        return "ERROR"


def offerings(text: str) -> list:
    offerings = []
    rangeS = text.find("Current course offerings</h1>")
    text = text[rangeS:]
    rangeE = text.find("<!--")
    text = text[:rangeE]
    if "Semester 1" in text:
        offerings.append(1)
    if "Semester 2" in text:
        offerings.append(2)
    return offerings


def sidebar(text: str, filter: str) -> list:
    coursesFound = []
    rangeS = text.find(filter)+len(filter)
    if rangeS == 20 or rangeS == len(filter)-1:
        return coursesFound
    text = text[rangeS:]
    rangeE = text.find("</p>")
    text = text[:rangeE]
    # print(rangeS, rangeE)
    courses = text.split(", ")
    for entries in courses:
        if len(entries) == 8:
            coursesFound.append(entries)
        else:
            entries = entries.split(" ")
            for entry in entries:
                if entry[0:4].isalpha() and entry[4:9].isdigit():
                    coursesFound.append(entry)
    return coursesFound
