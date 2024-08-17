COURSE_INFO = {"CSSE2002" : ['CSSE1001'], "COMP2048": ['CSSE2002'], "COMP3506": ['CSSE2002', 'MATH1061'],
			   "CSSE2010": [('CSSE1001', 'ENGG1100')]}

SEM_INFO = {"STAT1201" : [2], "STAT1301" : [2]}

def prerequisites(course):
	return []
	# TODO ADD SUPPORT FOR PREREQUISITE A OR (B AND C)
	if course not in COURSE_INFO.keys():
		return []
	return COURSE_INFO[course]