"""The main python backend file for this component.

Responsible for connecting the differrent modules/sub components"""

from GenerationComponent.plan import Plan
from pprint import pprint


PROGRAM_OPTIONS = {"Required" : ['COMP2048', 'COMP3506', 'CSSE1001', 'CSSE2002',
								 'CSSE2010', 'INFS1200', 'MATH1061', ('STAT1201', 'STAT1301')
								 ],
					"ProgramElectives": ['ELECTIVES LIST HERE']
					} 


def generateOptions(UserOptions={}, ProgramOptions={}):
	"""Generates a plan with blanks - along with a set of options for those blanks.

	Eg returns: {1: [['CSSE1001', 'MATH1051', BLANK, BLANK],
					 ['STAT1301', BLANK, BLANK, BLANK]],
				 2: [[SEM1], ...... .... ... .. .
				 	 [SEM2]]
				}
	"""
	# initial plan
	load = 2 if UserOptions['Load'] == 'part' else 4
	print(UserOptions['Load'])
	print(load)
	plan = Plan(int(UserOptions['startingYear']), load)
	requirements = ProgramOptions["Required"].copy()

	# Goes through the requirements trying to add each course to the first 
	# possible place.
	# If a requirement has two options- this will be displayed to the user
	
	# for course in UserOptions["Completed"]:
	# 		plan.add_completed(course)
	# 		continue
	plan._options['core'] = requirements
	for course in requirements:
		plan.add_course(course, required=True)
	return plan


if __name__ == "__main__":
	print("\n \n")
	print("\n Generation Options with the following inputs \n")
	pprint(USER_OPTIONS)
	print()
	pprint(PROGRAM_OPTIONS)
	print()
	print( " - " * 10)
	options = generateOptions(USER_OPTIONS, PROGRAM_OPTIONS)
	print(options)