

lists = [[6], [3, 4], [], [1, 2]]

rules = {9: {"no": [2], "yes": [(3, 5), 4]}, 2: {
    'no': [(9)], 'yes': [(3, 1), 4]}}


def check_no(value, sem):
    for check in lists[:sem-1]:
        if not set(rules[value]['no']).isdisjoint(set(check)):
            return False
    return True


def check_yes(value, sem):
    checkers = rules[value]['yes']
    for index, val in enumerate(checkers):
        if isinstance(val, tuple):
            for check in lists[:sem-1]:
                boold = not set(val).isdisjoint(set(check))
                if boold:
                    checkers.pop(index)
                    break
        else:
            print(checkers)
            upto = set()
            for check in lists[:sem-1]:
                upto = upto.union(set(check))
            print(checkers)
            checkers[index] = set(val).intersection(upto) == upto
    return False not in checkers


def place(value, place):
    if all([check_no(value, place), check_yes(value, place)]):
        lists[place-1].append(value)
    print(lists)


place(9, 3)
