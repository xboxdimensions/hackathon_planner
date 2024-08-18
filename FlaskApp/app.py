from flask import Flask, render_template, request, redirect, url_for

import sys, os
from pprint import pprint
sys.path.insert(0, os.path.abspath('../'))
from GenerationComponent.generate import generateOptions
from Scaper.course_scraper import scrapePlansAndCore
from FlaskApp.data import degreeList
DEVELOPMENT_ENV = True

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", degreeList=degreeList)


@app.route("/api", methods=["POST"])
def generate():
    """

    Returns data dict containing an ordered list of all courses they could choose.
    A plan contains the prefilled required courses.

    {"AvailiableCourses" : [("COURSE1", "This is course 1"), ("COURSE2", "This is info 2"), ("COURSE3", "ffs")],
    "Plan": { 2024 : [["CSSE1001", "CSSE1000"],
                       ["CourseSemester2", "Course2Semester2"]],
              2025 : [["CSSE2002"], []],
              2026 : [[], []]
            }
    }
    """
    data = request.get_json()

    # Get the program options & data
    info = scrapePlansAndCore(data['ProgramCode'])
    pprint(info)
    required = info['core']
    electives = info['electives']
    programOptions = {"Required": required, "ProgramElectives":electives}
    # pprint(programOptions)
    # print(programOptions["Required"])

    #
    userPlan = generateOptions(data, programOptions)
    rtrn = {"electives":electives,"CoreCourses":userPlan.get_extra('required'), "Plan":userPlan.get_return()}
    print(rtrn)
    return rtrn




rules = {'MATH1040': {'Name': 'Mathematical Foundations I', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['MATH7040'], 'Companion': [], 'RecommendPreq': []}, 'COMP2048': {'Name': 'Theory of Computing', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1061',), ('CSSE1001', 'ENGG1001')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'COMP3506': {'Name': 'Algorithms and Data Structures', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE2002',), ('MATH1061', '(CSSE2010'), ('STAT2202)',)], 'Incompatible': ['COMP2502', 'COMP7505'], 'Companion': [], 'RecommendPreq': []}, 'CSSE1001': {'Name': 'Introduction to Software Engineering', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['COMP1502', 'CSSE7030', 'ENGG1001'], 'Companion': [], 'RecommendPreq': []}, 'CSSE2002': {'Name': 'Programming in the Large', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001')], 'Incompatible': ['COMP2500', 'COMP7908', 'CSSE7023'], 'Companion': [], 'RecommendPreq': []}, 'CSSE2010': {'Name': 'Introduction to Computer Systems', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001')], 'Incompatible': ['COMP1300', 'COMP2303', 'COMP2302', 'CSSE1000', 'CSSE7035', 'CSSE7201', 'ELEC2002'], 'Companion': [], 'RecommendPreq': []}, 'INFS1200': {'Name': 'Introduction to Information Systems', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['INFS7900', 'MGTS3203', 'MGTS7206', 'BISM2207', 'BISM3203', 'BISM7206'], 'Companion': [], 'RecommendPreq': []}, 'MATH1061': {'Name': 'Discrete Mathematics', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['MATH7861'], 'Companion': [], 'RecommendPreq': []}, 'STAT1201': {'Name': 'Analysis of Scientific Data', 'Offerings': ['Semester 1', 'Semester 2', 'Summer Semester'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['ECON1310', 'ENVM2000', 'STAT1301', 'STAT2201', 'STAT2203', 'STAT2701', 'PUBH2007', 'HRSS3100'], 'Companion': [], 'RecommendPreq': []}, 'STAT1301': {'Name': 'Advanced Analysis of Scientific Data', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['ECON1310', 'ENVM2000', 'STAT1201', 'STAT2201', 'STAT2203', 'STAT2701', 'PUBH2007', 'HRSS3100'], 'Companion': [], 'RecommendPreq': []}, 'DECO3801': {'Name': 'Design Computing Studio 3 - Build', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE2002', 'COMP2140')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'COMP1100': {'Name': 'Introduction to Software Innovation', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['COMP7110'], 'Companion': [], 'RecommendPreq': ['CSSE1001']}, 'COMP2140': {'Name': 'Web/Mobile Programming', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('DECO1400',), ('CSSE1001', 'ENGG1001')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'COSC2500': {'Name': 'Numerical Methods in Computational Science', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('SCIE1000', '(CSSE1001'), ('MATH1051', 'MATH1071)', '(MATH1051', 'MATH1071'), ('MATH1052', 'MATH1072')], 'Incompatible': ['MATH2200', 'COSC7500'], 'Companion': [], 'RecommendPreq': []}, 'CSSE2310': {'Name': 'Computer Systems Principles and Programming', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001')], 'Incompatible': ['COMP2303', 'COMP7306', 'CSSE7231'], 'Companion': [], 'RecommendPreq': ['CSSE2010']}, 'DATA2001': {'Name': 'Fundamentals of Data Science', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001'), ('INFS1200',)], 'Incompatible': ['DATA7001'], 'Companion': [], 'RecommendPreq': []}, 'DECO1400': {'Name': 'Introduction to Web Design', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['DECO7140', 'IENV7961', 'MMDS1400', 'MMDS7961'], 'Companion': [], 'RecommendPreq': []}, 'DECO2500': {'Name': 'Human-Computer Interaction', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('DECO1400', 'CSSE1001', 'ENGG1001')], 'Incompatible': ['COMP2506', 'COMP3501', 'COMP7904', 'DECO7250'], 'Companion': [], 'RecommendPreq': []}, 'INFS2200': {'Name': 'Relational Database Systems', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('INFS1200',)], 'Incompatible': ['BSIS7206', 'COMM7605', 'INFS7903'], 'Companion': [], 'RecommendPreq': []}, 'MATH1051': {'Name': 'Calculus and Linear Algebra I', 'Offerings': ['Semester 1', 'Semester 2', 'Summer Semester'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['MATH1071', 'MATH7051'], 'Companion': [], 'RecommendPreq': []}, 'MATH1071': {'Name': 'Advanced Calculus &amp; Linear Algebra I', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['MATH1051', 'MATH7051', 'MATH7501'], 'Companion': [], 'RecommendPreq': []}, 'COMP3301': {'Name': 'Operating Systems Architecture', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('COMP2303', 'CSSE2310')], 'Incompatible': ['COMP3300', 'COMP7303', 'COMP7308'], 'Companion': [], 'RecommendPreq': []}, 'COMP3320': {'Name': 'Vulnerability Assessment and Penetration Testing', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE2310',), ('COMS3000', 'CYBR3000')], 'Incompatible': [], 'Companion': ['COMS3200'], 'RecommendPreq': ['COMS3200']}, 'COMP3400': {'Name': 'Functional and Logic Programming', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1061',), ('CSSE2002',)], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'COMP3702': {'Name': 'Artificial Intelligence', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'CSSE7030)', 'ENGG1001')], 'Incompatible': ['COMP3701', 'COMP7701', 'COMP7702'], 'Companion': [], 'RecommendPreq': ['MATH1061']}, 'COMP3710': {'Name': 'Pattern Recognition and Analysis', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1051', 'MATH1071'), ('CSSE1001', 'ENGG1001')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': ['MATH2302', 'COMP3506']}, 'COMP3820': {'Name': 'Digital Health Software Project', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE2002', 'CSSE7023', 'COMP2140', 'CSSE2310', 'CSSE7231'), ('DECO2500', 'DECO7250', 'BIOE6901')], 'Incompatible': ['COMP3000'], 'Companion': [], 'RecommendPreq': ['DECO2800', 'DECO7280', 'DECO3800', 'DECO7380']}, 'COMP4403': {'Name': 'Compilers and Interpreters', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('COMP3506',)], 'Incompatible': ['COMP7402'], 'Companion': [], 'RecommendPreq': ['CSSE2010']}, 'COMP4702': {'Name': 'Machine Learning', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001'), ('MATH1051', 'MATH1071'), ('STAT1201', 'STAT2003', 'STAT2201', 'STAT2202', 'STAT2203')], 'Incompatible': ['COGS4021', 'COMP3700', 'COMP7703', 'ELEC4700', 'ELEC7701'], 'Companion': [], 'RecommendPreq': ['COMP3702']}, 'COMP4703': {'Name': 'Natural Language Processing', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1061',), ('STAT1201', 'STAT1301', 'STAT2203', 'STAT2003', 'STAT2201'), ('CSSE1001', 'ENGG1001')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'COMS3200': {'Name': 'Computer Networks I', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('COMP2303 OR CSSE2310',)], 'Incompatible': ['COMS7201'], 'Companion': [], 'RecommendPreq': []}, 'COSC3000': {
    'Name': 'Vizualization, Computer Graphics &amp; Data Analysis', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('COSC2500', 'CSSE2002')], 'Incompatible': ['MATH3203'], 'Companion': [], 'RecommendPreq': ['SCIE2100']}, 'COSC3500': {'Name': 'High-Performance Computing', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('COSC2500', 'CSSE2002', 'CSSE2010', 'CSSE2310', 'PHYS3071')], 'Incompatible': ['COSC7502'], 'Companion': [], 'RecommendPreq': []}, 'CSSE3012': {'Name': 'The Software Process', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('(COMP2140', 'CSSE2002'), ('DECO2500', 'DECO2800', 'DECO2850))', 'CSSE3200')], 'Incompatible': ['COMP3500', 'COMP7503', 'CSSE3002', 'CSSE7001'], 'Companion': [], 'RecommendPreq': []}, 'CSSE3100': {'Name': 'Reasoning About Programs', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1061',), ('CSSE2002',)], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'CSSE3200': {'Name': 'Software Engineering Studio: Design, Implement and Test', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE2002',)], 'Incompatible': ['DECO2800'], 'Companion': [], 'RecommendPreq': []}, 'CYBR3000': {'Name': 'Information Security', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE2310', 'CSSE7231')], 'Incompatible': ['COMS3000', 'COMS7003', 'CYBR7002'], 'Companion': [], 'RecommendPreq': []}, 'DECO3500': {'Name': 'Social and Mobile Computing', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('DECO2500', 'DECO7250'), ('CSSE1001', 'ENGG1001', 'CSSE7030')], 'Incompatible': ['COMP3505', 'COMP7705', 'DECO7350'], 'Companion': [], 'RecommendPreq': []}, 'INFS3200': {'Name': 'Advanced Database Systems', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('INFS2200',)], 'Incompatible': ['INFS7907'], 'Companion': [], 'RecommendPreq': []}, 'INFS3202': {'Name': 'Web Information Systems', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001'), ('INFS1200',), ('DECO1400',)], 'Incompatible': ['INFS7202'], 'Companion': [], 'RecommendPreq': []}, 'INFS3208': {'Name': 'Cloud Computing', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001',), ('INFS1200',)], 'Incompatible': ['INFS3204', 'INFS7204', 'INFS7208'], 'Companion': [], 'RecommendPreq': []}, 'INFS4203': {'Name': 'Data Mining', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('CSSE1001', 'ENGG1001'), ('INFS2200',)], 'Incompatible': ['INFS7203'], 'Companion': [], 'RecommendPreq': []}, 'INFS4205': {'Name': 'Advanced Techniques for High Dimensional Data', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('INFS2200', 'INFS7903'), ('COMP3506', 'COMP7505')], 'Incompatible': ['INFS4200', 'INFS7200', 'INFS7205'], 'Companion': [], 'RecommendPreq': []}, 'MATH3201': {'Name': 'Scientific Computing: Advanced Techniques &amp; Applications', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH2000', 'MATH2001'), ('COSC2500', 'MATH2100')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'MATH3202': {'Name': 'Operations Research & Mathematical Planning', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1051', 'MATH1071'), ('MATH1052', 'MATH1072')], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'MATH3302': {'Name': 'Coding &amp; Cryptography', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH2301',)], 'Incompatible': [], 'Companion': [], 'RecommendPreq': []}, 'MATH1052': {'Name': 'Multivariate Calculus & Ordinary Differential Equations', 'Offerings': ['Semester 1', 'Semester 2', 'Summer Semester'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['MATH1072', 'MATH7052'], 'Companion': [], 'RecommendPreq': []}, 'MATH1072': {'Name': 'Advanced Multivariate Calculus & Ordinary Differential Equations', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['MATH1052', 'MATH7052', 'MATH7502'], 'Companion': ['MATH1051', 'MATH1071'], 'RecommendPreq': []}, 'DECO1100': {'Name': 'Design Thinking', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['DECO7110', 'IENV1000', 'IENV1301', 'IENV7911', 'IENV7913'], 'Companion': [], 'RecommendPreq': []}, 'DECO1800': {'Name': 'Design Computing Studio I - Interactive Technology', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['DECO7180'], 'Companion': ['CSSE1001', 'DECO1400'], 'RecommendPreq': []}, 'DECO2300': {'Name': 'Digital Prototyping and Extended Reality', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('DECO2500',), ('CSSE1001', 'ENGG1001')], 'Incompatible': ['DECO7230'], 'Companion': [], 'RecommendPreq': []}, 'DECO2850': {'Name': 'Design Computing Studio 2 - Interaction Design', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('DECO1800',)], 'Incompatible': ['DECO2800', 'DECO7280', 'DECO7285'], 'Companion': ['COMP2140'], 'RecommendPreq': []}, 'DECO3850': {'Name': 'Physical Computing Studio', 'Offerings': ['Semester 1'], 'Units': '4', 'Duration': '1', 'Prerequisite': [('DECO2300',), ('DECO2500',), ('DECO2800', 'DECO2850', 'DSGN2100')], 'Incompatible': ['DECO7385'], 'Companion': [], 'RecommendPreq': []}, 'ENGG1300': {'Name': 'Introduction to Electrical Systems', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('Mathematical Methods, Maths B', 'MATH1040.')], 'Incompatible': ['ENGG1030', 'ENGG1060', 'ELEC1000'], 'Companion': ['MATH1050'], 'RecommendPreq': []}, 'MATH1050': {'Name': 'Mathematical Foundations II', 'Offerings': ['Semester 1', 'Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': '', 'Incompatible': ['MATH1051', 'MATH1052', 'MATH7050'], 'Companion': [], 'RecommendPreq': []}, 'MATH2001': {'Name': 'Calculus &amp; Linear Algebra II', 'Offerings': ['Semester 1', 'Semester 2', 'Summer Semester'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1051', 'MATH1071'), ('MATH1052', 'MATH1072')], 'Incompatible': ['MATH2000', 'MATH2901', 'MATH7000'], 'Companion': [], 'RecommendPreq': []}, 'MATH2301': {'Name': 'Linear & Abstract Algebra & Number Theory', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1051', 'MATH1071, MATH1061')], 'Incompatible': ['MATH2300', 'MATH7307'], 'Companion': [], 'RecommendPreq': []}, 'MATH2302': {'Name': 'Discrete Mathematics II', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1061',)], 'Incompatible': ['MATH2300', 'MATH7308'], 'Companion': [], 'RecommendPreq': []}, 'MATH3104': {'Name': 'Mathematical Biology', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH2100',)], 'Incompatible': ['MATH7134'], 'Companion': [], 'RecommendPreq': []}, 'SCIE1000': {'Name': 'Theory &amp; Practice in Science', 'Offerings': ['Semester 1', 'Semester 2', 'Summer Semester'], 'Units': '2', 'Duration': '1', 'Prerequisite': [], 'Incompatible': ['SCIE1100'], 'Companion': [], 'RecommendPreq': []}, 'SCIE2100': {'Name': 'Bioinformatics 1: Introduction', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('SCIE1000',), ('STAT1201)', '(MATH1051', 'MATH1071'), ('CSSE1001',)], 'Incompatible': ['COSC2000'], 'Companion': [], 'RecommendPreq': []}, 'STAT2003': {'Name': 'Mathematical Probability', 'Offerings': ['Semester 1'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('MATH1051', 'MATH1071')], 'Incompatible': ['STAT2001'], 'Companion': [], 'RecommendPreq': []}, 'STAT2004': {'Name': 'Statistical Modelling &amp; Analysis', 'Offerings': ['Semester 2'], 'Units': '2', 'Duration': '1', 'Prerequisite': [('(MATH1051', 'MATH1071) + (STAT1201, STAT1301', 'STAT2201) + (STAT2003', 'STAT2203)')], 'Incompatible': ['STAT2002', 'STAT2904', 'STAT7004'], 'Companion': [], 'RecommendPreq': []}}

# returns true if no incompabilities occur in current sem or previous ones


def check_no(value, sem):
    lists = request.get_json()['list']
    for check in lists[:sem]:
        if set(rules[value]['Incompatible']).isdisjoint(set(check)):
            pass
        else:
            return False

    return True

# flags if preqs are met for this course


def check_yes(value, sem):
    lists = request.get_json()['list']
    try :
        checkers = rules[value]['Prerequisite']
        yesh = [False for i in range(len(checkers))]
        for index, val in enumerate(checkers):
            if isinstance(val, tuple):
                for check in lists[:sem-1]:
                    boold = not set(val).isdisjoint(set(check))
                    if boold:
                        yesh[index] = True
                        break
            else:
                upto = set()
                for check in lists[:sem-1]:
                    upto = upto.union(set(check))
                yesh[index] = set(val).intersection(upto) == upto
    
    except:
        return False not in yesh

# def check_preqs() -> bool:

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    value  = data["value"]
    place = int(data["place"][-1])
    lists = request.get_json()['list']
    if check_no(value, place) and not (any(value in sublist for sublist in lists)):
        if not check_yes(value, place):
            return {"status": "no", "data": lists }
        lists[place].append(value)
    print(lists)
    return {"status": "OK" , "data": lists}


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)

