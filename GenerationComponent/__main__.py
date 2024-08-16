"""The main python backend file for this component.

Responsible for connecting the differrent modules/sub components"""

BLANK = 'XXXX0000'


USER_OPTIONS = {"ProgramLength" : 3, # years
				"CourseLoad" : 4, # courses / semester
				"AlreadyCompleted" : ['CSSE1001', 'MATH1051']
				}

PROGRAM_OPTIONS = {"Required" : ['CSSE1001',
								 ('MATH1051', 'MATH1071'),
								   'CSSE2002',
									 ('STAT1201', 'STAT1301')
								],
					"ProgramElectives": ['COMP3400', 'CSSE2010', 'MATH1061']
					} 

def generate_options(UserOptions, ProgramOptions):
	"""Generates a plan with blanks - along with a set of options for those blanks.

	Eg returns: {1: [['CSSE1001', 'MATH1051', BLANK, BLANK],
					 ['STAT1301', BLANK, BLANK, BLANK]],
				 2: [[SEM1], 
				 	 [SEM2]]
				}
	"""
	return {1: [BLANK]} # TODO

