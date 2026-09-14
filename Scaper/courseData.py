import html
import re


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
    """Parse a UQ prerequisite expression into AND/OR structures.

    The planner represents an AND as a list and an OR as a tuple.  UQ
    publishes prerequisite text such as:
    ``CSSE2002 and (MATH1061 or MATH1081)``.
    """
    marker = text.find('course-prerequisite">')
    if marker < 0:
        return []

    expression = text[marker + len('course-prerequisite">'):]
    expression = expression.split("</p>", 1)[0]
    expression = re.sub(r"<[^>]+>", " ", expression)
    expression = html.unescape(expression).upper()

    if "GRADE" in expression:
        return []

    tokens = re.findall(r"\(|\)|\bAND\b|\bOR\b|[A-Z]{4}\d{4}", expression)
    if not tokens:
        return []

    position = 0

    def parse_factor():
        nonlocal position
        if position >= len(tokens):
            return []
        if tokens[position] == "(":
            position += 1
            value = parse_or()
            if position < len(tokens) and tokens[position] == ")":
                position += 1
            return value
        value = tokens[position]
        position += 1
        return value

    def parse_and():
        nonlocal position
        value = parse_factor()
        while position < len(tokens) and tokens[position] == "AND":
            position += 1
            right = parse_factor()
            left_values = value if isinstance(value, list) else [value]
            right_values = right if isinstance(right, list) else [right]
            value = left_values + right_values
        return value

    def parse_or():
        nonlocal position
        value = parse_and()
        while position < len(tokens) and tokens[position] == "OR":
            position += 1
            right = parse_and()
            left_values = value if isinstance(value, tuple) else (value,)
            right_values = right if isinstance(right, tuple) else (right,)
            value = left_values + right_values
        return value

    return parse_or()

def flatten(S):
    if not S:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]+ flatten(S[1:]))
    return S[:1] + flatten(S[1:])

def split(s: str) -> list:
    if '(' in s or ')' in s:
        s = ''.join(c for c in s if c not in '()')
    if (" AND " in s) or (" OR " in s):
        if 0 <= s.find(" AND ") <= s.find(" OR ") or s.find(" OR ") < 0:
            sep = " AND "
        else:
            sep = " OR "
        a, b = s.split(sep, maxsplit= 1)
        
        if sep == " AND ":
            return [a, split(b)]
        else:
            return [(a, split(b))]
    return s

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