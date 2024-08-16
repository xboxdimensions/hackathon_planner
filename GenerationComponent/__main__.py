"""The main python backend file for this component.

Responsible for connecting the differrent modules/sub components"""

from plan import Plan
from semesterIterator import semIter
from pprint import pprint

USER_OPTIONS = {"ProgramLength" : 3, # years
				"CourseLoad" : 4, # courses / semester
				"AlreadyCompleted" : ['CSSE1001', 'MATH1051']
				}

PROGRAM_OPTIONS = {"Required" : ['COMP2048', 'COMP3506', 'CSSE1001', 'CSSE2002',
								 'CSSE2010', 'INFS1200', 'MATH1061', ('STAT1201', 'STAT1301')
								 ],
					"ProgramElectives": ['ELECTIVES LIST HERE']
					} 

COURSE_INFO = {"CSSE2002" : ['CSSE1001'], "COMP2048": ['CSSE2002'], "COMP3506": ['CSSE2002', 'MATH1061']}
# TODO ADD SUPPORT FOR PREREQUISITE A OR (B AND C)

def prerequisites(course):
	if course not in COURSE_INFO.keys():
		return []
	return COURSE_INFO[course]

def generate_options(UserOptions={}, ProgramOptions={}):
	"""Generates a plan with blanks - along with a set of options for those blanks.

	Eg returns: {1: [['CSSE1001', 'MATH1051', BLANK, BLANK],
					 ['STAT1301', BLANK, BLANK, BLANK]],
				 2: [[SEM1], ...... .... ... .. .
				 	 [SEM2]]
				}
	"""
	# initial plan
	plan = Plan(UserOptions["ProgramLength"], UserOptions["CourseLoad"])
	requirements = ProgramOptions["Required"].copy()

	# Goes through the requirements trying to add each course to the first 
	# possible place.
	# If a requirement has two options- this will be displayed to the user
	for course in requirements:
		if isinstance(course, tuple):
			plan.add_required_choice(course)
			continue # have this dealt with later
		prereqs = prerequisites(course)
		while prereqs:
			print(prereqs)
			# add the prerequisite to first possible place
			i = iter(semIter()) # iterator for year and semester
			plan.add_course(prereqs[0], i.year, i.sem)
			prereqs.pop(0)
		plan.add_course(course, i.year, i.sem)
	return plan


if __name__ == "__main__":
	print("\n \n")
	print("\n Generation Options with the following inputs \n")
	pprint(USER_OPTIONS)
	print()
	pprint(PROGRAM_OPTIONS)
	print()
	print( " - " * 10)
	options = generate_options(USER_OPTIONS, PROGRAM_OPTIONS)
	print(options)