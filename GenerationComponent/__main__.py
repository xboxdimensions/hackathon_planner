"""The main python backend file for this component.

Responsible for connecting the differrent modules/sub components"""

from plan import Plan
from pprint import pprint

USER_OPTIONS = {"ProgramLength" : 3, # years
				"CourseLoad" : 4, # courses / semester
				"Completed" : ['CSSE1001', 'MATH1051']
				}

PROGRAM_OPTIONS = {"Required" : ['COMP2048', 'COMP3506', 'CSSE1001', 'CSSE2002',
								 'CSSE2010', 'INFS1200', 'MATH1061', ('STAT1201', 'STAT1301')
								 ],
					"ProgramElectives": ['ELECTIVES LIST HERE']
					} 


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
	for course in UserOptions["Completed"]:
			plan.add_completed(course)
			continue
	for course in requirements:
		plan.add_course(course)
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