relatedCourses = {'course-incompatible">': 'Incompatible',
                  'course-prerequisite">': "Prerequisite",
                  'course-companion">': "Companion",
                  'recommended-prerequisite">': "RecommendPreq"}


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
        offerings.append("Semester 1")
    if "Semester 2" in text:
        offerings.append("Semester 2")
    if "Summer Semester" in text:
        offerings.append("Summer Semester")
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
