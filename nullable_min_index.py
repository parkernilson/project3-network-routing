def find_min(l):
    min_elem = min(filter(lambda x: x is not None, l))
    return l.index(min_elem)