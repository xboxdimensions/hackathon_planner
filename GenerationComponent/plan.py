"""Plan class"""
from GenerationComponent.semesterIterator import semIter
from GenerationComponent.prerequisites import SEM_INFO
from Scaper.course_scraper import courseData as cD

def pre_off(code):
	if isinstance(code, str) and len(code) == 8:
		data = cD([code])
		return (data[code]['Prerequisite'], data[code]['Offerings'])

prerequisites = lambda code : pre_off(code)[0]
offerrings = lambda code : pre_off(code)[1]
BLANK = 'XXXX0000'
SEMESTERS = 2

class Plan:
	DATA = {}
	def __init__(self, startingYear: int = 2024, courseLoad: int = 4) -> None:
		"""Initializes Blank plan
		"""
		self._start = startingYear
		self._years = years =  4 # DEFAULT TO 4 YEARS # TODO
		self._data = {n : ([BLANK]*courseLoad, [BLANK]*courseLoad) for n in range(1, years+1)}
		# TODO replace blanks with sets and just no blank
		self._options = {"required" : [], "core" : [], "error": [], "extra": []}

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
		print(69, course, self._options['core'])
		if course not in self._options["required"] and not [c for c in course if c in self._options['core']]:
			print(69, course)
			self._options["required"].append(course)


	def get_length(self) -> int:
		"""Returns the program length in years"""
		return self._years

	def _add(self, course: str, year: int, semester: int) -> int:
		"""Adds course to first blank spot in given semester.

		DOES NOT CHECK FOR PREREQUISITES THIS IS DONE BEFORE CALLING THIS!!

		
		0 = Successful addition, 1 = bad year, -1 = no spots
		
		"""
		if isinstance(course, int):
			return 0
		if isinstance(course, str) and (course in self._courses or len(course) != 8):
			return 0 # common occurance dont print anything
		# print("Adding course", course, "to", year, semester)
		if course not in Plan.DATA:
			o = pre_off(course)
			if o:
				pr, os = o
				Plan.DATA[course] = (pr, os)
		else:
			os = Plan.DATA[course][1]
		try:
			if (year < 1 or year > self._years or semester not in os): # Validation Checking
				print(os, 6969)
				print(f"Could not add course. Year {year}, Semester {semester} is invalid.")
				return 1 
		except:
			print("there was a paul moment")
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

	def add_course(self, course: str, required=False) -> bool:
		"""Adds a course to the first availiable spot taking into account
		prerequisites
		"""
		if not course:
			return 0
		if isinstance(course, list):
			if course:
				for c in course:
					self.add_course(c)
				return

		if isinstance(course, tuple):
		
			# if it has a CORE / required choice they dont have to choose
			cores = [c for c in course if c in self._options['core']]
			print(cores)
			if cores:
				course = cores[0]
				for c in cores:
					self._options['extra'].append(c)
				
			else:
				self.add_required_choice(course) # THEY WILL HAVE TO CHOOSE
				if not course or len(course) > 2:
					return
				course = course[0] # take the first option as default
			return self.add_course(course)
			
		if course in self._courses:
			return # wtf is the point

		# First recurislvey add the prerequisites and their prereqs etc
		hy, hs = 1, 1 # highest year and semester
		ps = []
		if course not in Plan.DATA:
			o = pre_off(course)
			if o:
				ps, os = o
				Plan.DATA[course] = (ps, os)
		else:
			ps = Plan.DATA[course]
		for prereq in ps:
			if isinstance(prereq, list):
				if prereq:
					for c in prereq:
						self.add_course(c)
			elif isinstance(prereq, tuple):
				cores = [c for c in course if c in self._options['core']]
				if cores:
					course = cores[0]
					for c in cores:
						self._options['extra'].append(c)
					
				else:
				# There is a choice one or the other
					if isinstance(prereq, tuple) and len(prereq) == 2 and sum(len(x) for x in prereq) == 16:
						self.add_required_choice(prereq)
				# choose the first one for now # TODO
				if prereq:
					prereq = prereq[0]
			elif prereq not in self._courses:
				pass
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

		

