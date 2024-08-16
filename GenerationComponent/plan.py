"""Plan class"""

BLANK = 'XXXX0000'
SEMESTERS = 2

class Plan:
	def __init__(self, years: int = 4, courseLoad: int = 4) -> None:
		"""Initializes Blank plan
		"""
		self._years = years
		self._data = {n : ([BLANK]*courseLoad, [BLANK]*courseLoad) for n in range(1, years+1)}
		# TODO replace blanks with sets and just no blank
		self._options = {"required" : set(), "majorElectives" : []}

		self._courses = set() # QUICK WAY OF CHECKING IF USER IS TAKING COURSE

	def add_required_choice(self, course: str):
		"""Adds a required choice in the plan, this needs to be dealt
		with until the plan can be finalised.
		
		# TODO make it so that there are spaces left for these requirements
		"""
		self._options["required"].add(course)


	def get_length(self) -> int:
		"""Returns the program length in years"""
		return self._years

	def add_course(self, course: str, year: int, semester: int) -> bool:
		"""Adds course to first blank spot in given semester.

		DOES NOT CHECK FOR PREREQUISITES THIS IS DONE BEFORE CALLING THIS!!

		TODO CHECK IF COURSE IS AVAILIABLE THIS SEMESTER
		
		True = Successful addition, False = Did not get added
		
		"""
		
		if course in self._courses:
			return False # common occurance dont print anything
		print("Adding course", course, "to", year, semester)
		if (year < 1 or year > self._years or semester not in {1, 2}): # Validation Checking
			print(f"Could not add course. Year {year}, Semester {semester} is invalid.")
			return False

		# Going through and adding course as first blank spot
		for spot in self._data[year][semester-1]:
			if spot == BLANK:
				sem = self._data[year][semester-1]
				sem.pop() # remove last (blank) course
				sem.insert(0, course)
				self._courses.add(course)
				return True
		print(f"No spots availiable in year {year}, semester {semester}")
		return False
		



	def get_data(self) -> dict:
		"""Getter method for the whole data"""
		return self._data

	def get_year(self, year: int) -> list:
		"""Getter method for data in year"""
		return self._data[year]

	def __str__(self) -> str:
		"""String representation is each year (two semesters) followed by newlines"""
		return "\n".join(str(val) for val in self._data.values())

		

