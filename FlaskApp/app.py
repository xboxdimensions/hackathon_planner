from flask import Flask, render_template

DEVELOPMENT_ENV = True

app = Flask(__name__)

data = {"test" : 1}


COURSES = {2024: [("MATH1061", "Maths and Stuff"), ("MATh1072", "Worse Maths and stuff")], 2025: [], 2026: [], 2027: []}

YEARS = range(2024, 2028)
@app.route("/")
def index():
    return render_template("index.html", years=YEARS, courses = COURSES)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)

