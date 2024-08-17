from flask import Flask, render_template, request, redirect, url_for

import sys, os
from pprint import pprint
sys.path.insert(0, os.path.abspath('../'))
from GenerationComponent.generate import generateOptions
from Scaper.separated_tabs import seperatedTabs
DEVELOPMENT_ENV = True

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index_copy.html")


@app.route("/api", methods=["POST"])
def generate():  
    """
    
    Returns data dict containing an ordered list of all courses they could choose.
    A plan contains the prefilled required courses. 
    
    {"AvailiableCourses" : ["COURSE1", "COURSE2", "COURSE3"],
    "Plan": { 2024 : [["CSSE1001", "CSSE1000"],
                       ["CourseSemester2", "Course2Semester2"]],
              2025 : [["CSSE2002"], []],
              2026 : [[], []]
            }
    }
    """
    data = request.get_json()

    # Get the program options & data
    
    courses = seperatedTabs(data['ProgramCode'])
    required = courses[0]
    electives = courses[1:]
    programOptions = {"Required": required, "ProgramElectives":electives}
    # pprint(programOptions)
    # print(programOptions["Required"])
    
    #
    userPlan = generateOptions(data, programOptions)
    pprint({"AvailiableCourses":electives, "Plan":userPlan.get_return()})
    return {"AvailiableCourses":["CSSE1001"], "Plan":userPlan.get_return()}
     

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)

