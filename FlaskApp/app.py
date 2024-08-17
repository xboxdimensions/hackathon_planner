from flask import Flask, render_template, request, redirect, url_for

import sys, os
sys.path.insert(0, os.path.abspath('../'))
from GenerationComponent.generate import generateOptions
from Scaper.course_scraper import course_finder
DEVELOPMENT_ENV = True

app = Flask(__name__)

data = {"test" : 1}


COURSES = {2024: [("MATH1061", "Maths and Stuff"), ("MATh1072", "Worse Maths and stuff")], 2025: [], 2026: [], 2027: []}

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
    print(data)

    # Get the program options & data
    
    programOptions = {"Required":[], "ProgramElectives":[]}
    # ask will for this ^^^ 
    
    #
    userPlan = generateOptions(data, programOptions)
    print({"AvailiableCourses":["CSSE1001"], "Plan":userPlan.get_return()})
    return {"AvailiableCourses":["CSSE1001"], "Plan":userPlan.get_return()}
     

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)

