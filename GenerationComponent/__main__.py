"""The main python backend file for this component.

Responsible for connecting the differrent modules/sub components"""

from plan import Plan
from semesterIterator import semIter
from pprint import pprint

USER_OPTIONS = {"ProgramLength" : 3, # years
				"CourseLoad" : 4, # courses / semester
				"AlreadyCompleted" : ['CSSE1001', 'MATH1051']
				}

PROGRAM_OPTIONS = {"Required" : ['CSSE1001',
								 ('MATH1051', 'MATH1071'),
								   'CSSE2002',
									 ('STAT1201', 'STAT1301'),

									'REQ1', 'REQ2', 'REQ3', 'REQ4', 'REQ5'
								],
					"ProgramElectives": ['COMP3400', 'CSSE2010', 'MATH1061'
						  , 'EL1', 'EL2', 'EL3']
					} 

COURSE_INFO = {"CSSE1001" : [], "CSSE2002" : ["CSSE1001"], 'REQ4' : ['REQ1', 'REQ2']}

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
		i = iter(semIter()) # iterator for year and semester
		if isinstance(course, tuple):
			plan.add_required_choice(course)
			continue # have this dealt with later
		prereqs = prerequisites(course)
		while prereqs:
			print(prereqs)
			# add the prerequisite
			added = False
			while not added:
				added = plan.add_course(prereqs[0], i.year, i.sem)
				next(i)
				if i.year > plan.get_length():
					break # if we have checked every spot in the program 
						# length then it isnt possible
			prereqs.pop(0)
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