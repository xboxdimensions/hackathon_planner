"""Semester iterator, year1 sem1, year1 sem 2, year 2 sem 1... etc"""

class semIter:
	def __init__(self, year = 1, sem = 1):
		self.year = year
		self.sem = sem

	def __iter__(self):
		return self
	
	def __next__(self):
		if self.sem == 2:
			self.year += 1
			self.sem = 1
		else:
			self.sem += 1
		return self.year, self.sem