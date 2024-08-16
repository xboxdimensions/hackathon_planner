"""Timetable class"""

BLANK = 'XXXX0000'
SEMESTERS = 2

class Timetable:
	def __init__(self, years: int = 4, courseLoad: int = 4) -> None:
		"""Initializes Blank timetable
		"""
		self._data = {n : [[BLANK]*courseLoad]*SEMESTERS for n in range(0, years)}

	def get_data(self) -> dict:
		"""Getter method for the whole data"""
		return self._data

	def get_year(self, year) -> list:
		"""Getter method for data in year"""
		return self._data[year]

	def __str__(self) -> str:
		"""String representation is each year (two semesters) followed by newlines"""
		return "\n".join(str(val) for val in self._data.values())

		

