class HeapPriorityQueue:
    def __init__(self):
        self.pointers = []
        """
        an array where each index i contains the index of node i in the tree array
        """
        self.tree: list[tuple[int, int]] = []
        """
        an array that represents a tree where each entry is (node, value)
        where node is a 1-based node id
        """
        self.count = 0
        """
        The count of how many nodes are in the tree
        """

    def percolate_up(self, index):
        """
        index - 1-based index in the tree array. The value of the pointers array at 1-based index
        which corresponds to node id is the index to find that node in the tree
        """
        if index > 1:
            node, value = self.tree[index]

            parent_index = index // 2
            parent_node, parent_value = self.tree[parent_index]

            if parent_value > value:
                self.swap_nodes_at_indices(index, parent_index)
                self.percolate_up(parent_index)

    def swap_nodes_at_indices(self, node_1_index, node_2_index):
        """
        node_1_index and node_2_index are 1-based indices of nodes in the tree array
        """
        node_1, node_1_value = self.tree[node_1_index]
        node_2, node_2_value = self.tree[node_2_index]
        self.tree[node_2_index] = (node_1, node_1_value)
        self.tree[node_1_index] = (node_2, node_2_value)
        self.pointers[node_1] = node_2_index
        self.pointers[node_2] = node_1_index

    def percolate_down(self, index):
        """
        index - 1-based index of node in tree array
        """
        if index > self.count:
            return

        left = index * 2
        right = left + 1

        cur_node, cur_value = self.tree[index]

        if left <= self.count:
            left_node, left_value = self.tree[left]
            if right <= self.count:
                right_node, right_value = self.tree[right]

                if right_value < cur_value and right_value < left_value:
                    # percolate down to the right
                    self.swap_nodes_at_indices(index, right)
                    return self.percolate_down(right)

            if left_value < cur_value:
                # percolate down to the left
                self.swap_nodes_at_indices(index, left)
                return self.percolate_down(left)

    def insert(self, node, value):
        """
        node - 0-based id of the node
        """
        # insert at the end of the tree
        index = self.count + 1
        self.count += 1
        self.pointers[node + 1] = index
        self.tree[index] = (node + 1, value)

        self.percolate_up(index)

    def delete_min(self):
        """
        Returns a 0-based id of the min node and its value
        """
        min_node, min_value = self.tree[1]
        self.pointers[min_node] = None
        
        last_node, last_value = self.tree[self.count]
        self.tree[self.count] = None
        self.pointers[last_node] = 1
        self.count -= 1
        self.tree[1] = (last_node, last_value)

        self.percolate_down(1)

        return min_node - 1, min_value

    def decrease_key(self, node, value):
        """
        node - 0-based id of the node
        """
        index = self.pointers[node + 1]
        self.tree[index] = (node + 1, value)
        self.percolate_up(index)

    @classmethod
    def make_queue(cls, node_dists):
        """
        vals - A dict of structure: { [node]: dist }
        where node is a 0-based id
        """
        instance = cls()

        instance.pointers = [None for _ in range(len(node_dists) + 1)]
        instance.tree = [None for _ in range(len(node_dists) + 1)]
        for node, dist in node_dists.items():
            instance.insert(node, dist)

        return instance

    def __str__(self):
        return f"""
        Pointers:
        {str(self.pointers)}
        Tree:
        {str(self.tree)}
        """
