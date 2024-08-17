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
    return render_template("index_copy.html", degreeList=degreeList)


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
    print(info)
    required = info['core']
    electives = info['electives']
    programOptions = {"Required": required, "ProgramElectives":electives}
    # pprint(programOptions)
    # print(programOptions["Required"])
    
    #
    userPlan = generateOptions(data, programOptions)
    rtrn = {"AvailiableCourses":electives+userPlan.get_extra('required'), "Plan":userPlan.get_return()}
    print(rtrn)
    return rtrn
     

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)

