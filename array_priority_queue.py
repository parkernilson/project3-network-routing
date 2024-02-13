from nullable_min_index import find_min

class ArrayPriorityQueue:

    def __init__(self):
        self.vals = []
        self.count = 0

    def insert(self, node, value):
        if self.vals[node] == None:
            self.count += 1
        self.vals[node] = value

    def decrease_key(self, node, value):
        self.vals[node] = value

    def delete_min(self):
        min_index = find_min(self.vals)
        min_val = self.vals[min_index]
        self.vals[min_index] = None
        self.count -= 1
        return min_index, min_val

    @classmethod
    def make_queue(cls, vals: dict[int, int]):
        """
        vals - A dict of structure: { [node]: dist }
        """
        instance = cls()
        instance.vals = [None for _ in vals]
        for node, dist in vals.items():
            instance.vals[node] = dist
        instance.count = len(vals)
        return instance

    def __str__(self):
        return str(self.vals)
