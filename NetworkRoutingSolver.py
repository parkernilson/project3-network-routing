#!/usr/bin/python3


from CS312Graph import *
import time

from array_priority_queue import ArrayPriorityQueue
from heap_priority_queue import HeapPriorityQueue


class NetworkRoutingSolver:
    def __init__(self):
        self.dists: dict[int, int] = dict()
        """
        A dictionary of structure: { node_id: dist }
        where node_id is a 0-based node id
        """
        self.prev_edge: dict[int, CS312GraphEdge] = dict()
        """
        A dictionary of structure: { node_id: prev_node }
        where prev_node is the previous node in the shortest path to the specified node
        """

    def initializeNetwork(self, network):
        assert type(network) == CS312Graph
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex

        path_edges = []
        total_length = 0
        nodes = self.network.getNodes()
        dest_node = nodes[destIndex]
        prev_edge = self.prev_edge[dest_node.node_id]
        
        while prev_edge != None:
            path_edges.append((prev_edge.src.loc, prev_edge.dest.loc, "{:.0f}".format(prev_edge.length)))
            total_length += prev_edge.length
            prev_edge = self.prev_edge[prev_edge.src.node_id]

        return {"cost": total_length, "path": path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        nodes = self.network.getNodes()
        self.dists = {node.node_id: float("inf") for node in nodes}
        self.prev_edge = {node.node_id: None for node in nodes}

        q = (
            HeapPriorityQueue.make_queue(self.dists)
            if use_heap
            else ArrayPriorityQueue.make_queue(self.dists)
        )
        start_node = nodes[srcIndex]
        self.dists[start_node.node_id] = 0
        q.decrease_key(start_node.node_id, 0)

        while q.count > 0:
            node_id, dist = q.delete_min()
            node = nodes[node_id]

            # for all the neighbors, if the path through this node
            #   is shorter, add it to the queue with the new dist (use decrease key)
            # update the dist in the dists map
            # set this node as the "prev" node to the neighbor
            for edge in node.neighbors:

                # Don't go backwards (only go forward)
                if edge.dest == node:
                    continue

                neighbor_node = edge.dest
                path_weight = edge.length
                
                neighbor_dist = self.dists[neighbor_node.node_id]
                new_potential_dist = dist + path_weight
                if new_potential_dist < neighbor_dist:
                    self.dists[neighbor_node.node_id] = new_potential_dist
                    self.prev_edge[neighbor_node.node_id] = edge
                    q.decrease_key(neighbor_node.node_id, new_potential_dist)

        t2 = time.time()
        return t2 - t1
