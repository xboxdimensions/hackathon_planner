"""Plan class"""
from GenerationComponent.semesterIterator import semIter
from GenerationComponent.prerequisites import prerequisites, SEM_INFO


BLANK = 'XXXX0000'
SEMESTERS = 2

class Plan:
	def __init__(self, startingYear: int = 2024, courseLoad: int = 4) -> None:
		"""Initializes Blank plan
		"""
		self._start = startingYear
		self._years = years =  4 # DEFAULT TO 4 YEARS # TODO
		self._data = {n : ([BLANK]*courseLoad, [BLANK]*courseLoad) for n in range(1, years+1)}
		# TODO replace blanks with sets and just no blank
		self._options = {"required" : [], "majorElectives" : [], "error": []}

		self._courses = set() 

	def get_extra(self, key: str = 'error') -> list[str]:
		return self._options[key]

	def get_return(self) -> dict:
		"""Returns the plan in dictionary format as required for html"""
		return {self._start + year - 1 : [[course for course in sem if course != BLANK] for sem in sems] for year, sems in self._data.items()}


	def add_completed(self, course: str):
		"""Used for user already completed that are not on the plan"""
		self._courses.add(course)

	def add_required_choice(self, course: list):
		"""Adds a required choice in the plan, this needs to be dealt
		with until the plan can be finalised.
		
		# TODO make it so that there are spaces left for these requirements
		"""
		self._options["required"].append(course)


	def get_length(self) -> int:
		"""Returns the program length in years"""
		return self._years

	def _add(self, course: str, year: int, semester: int) -> int:
		"""Adds course to first blank spot in given semester.

		DOES NOT CHECK FOR PREREQUISITES THIS IS DONE BEFORE CALLING THIS!!

		TODO CHECK IF COURSE IS AVAILIABLE THIS SEMESTER
		
		0 = Successful addition, 1 = bad year, -1 = no spots
		
		"""
		if course in self._courses:
			return 0 # common occurance dont print anything
		# print("Adding course", course, "to", year, semester)
		if (year < 1 or year > self._years or semester not in {1, 2}): # Validation Checking
			print(f"Could not add course. Year {year}, Semester {semester} is invalid.")
			return 1

		# TODO SEMESTER OFFERRINGS 

		# Going through and adding course as first blank spot
		for spot in self._data[year][semester-1]:
			if spot == BLANK:
				sem = self._data[year][semester-1]
				sem.pop() # remove last (blank) course
				sem.insert(0, course)
				self._courses.add(course)
				return 0
		# print(f"No spots availiable in year {year}, semester {semester}")
		return -1
		
	def get_course_sem(self, course: str) -> tuple:
		"""Gets the year, semester of a course"""
		for i, year in enumerate(self._data.values()):
			for j, semester in enumerate(year):
				if course in semester:
					return i+1, j+1
		return 1, 0

	def add_course(self, course: str) -> bool:
		"""Adds a course to the first availiable spot taking into account
		prerequisites
		"""
		if isinstance(course, list) or isinstance(course, tuple):
			self.add_required_choice(course) # THEY WILL HAVE TO CHOOSE
			if not course or len(course) > 2:
				return
			course = course[0] # take the first option as default
		if course in self._courses:
			return

		# First recurislvey add the prerequisites and their prereqs etc
		hy, hs = 1, 1 # highest year and semester
		ps = prerequisites(course).copy()
		for prereq in ps:
			if isinstance(prereq, list):
				# There is a choice one or the other
				self.add_required_choice(prereq)
				if len(prereq) > 2:
					continue # TODO IDK WTF THIS MEANS
				# choose the first one for now # TODO
				prereq = prereq[0]
			elif prereq not in self._courses:
				self.add_course(prereq)
			# get the last semester a prerequisite is in 
			yr, se = self.get_course_sem(prereq)
			if hy > yr or (hy == yr and se > hs):
				hy = yr
				hs = se

		# add this course finlaly
		s = iter(semIter( hy, hs))
		if ps:
			next(s)
		code = self._add(course, s.year, s.sem)
		while code == -1:
			if s.year > 10:
				if course not in self._courses:
					self._options['error'].append(course)
				break # ERROR
			next(s)
			self._add(course, s.year, s.sem)


	def get_data(self) -> dict:
		"""Getter method for the whole data"""
		return self._data

	def get_year(self, year: int) -> list:
		"""Getter method for data in year"""
		return self._data[year]

	def __str__(self) -> str:
		"""String representation is each year (two semesters) followed by newlines"""
		return "\n".join(str(val) for val in self._data.values())

		

