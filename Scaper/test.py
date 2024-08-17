def split(s: str) -> list:
		if '(' in s or ')' in s:
			s = ''.join(c for c in s if c not in '()')
		if (" AND " in s) or (" OR " in s):
			if 0 <= s.find(" AND ") <= s.find(" OR ") or s.find(" OR ") < 0:
				sep = " AND "
			else:
				sep = " OR "
			print(s, sep)
			a, b = s.split(sep, maxsplit= 1)
			
			if sep == " AND ":
				return [a, split(b)]
			else:
				return [(a, split(b))]
		return s