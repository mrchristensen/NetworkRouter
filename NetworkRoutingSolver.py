#!/usr/bin/python3


from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network
        self.results = {}

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.dest]

        while self.results[node.node_id]["prev"] is not None:  # Traverse the graph backwards
            previous_node = self.network.nodes[self.results[node.node_id]['prev']]

            # if self.results[node.node_id]["prev"] is None:
            #     path_edges = []
            #     total_length = math.inf
            #     break
            #
            #
            for neighbor in previous_node.neighbors:
                if neighbor.dest is node:
                    total_length = total_length + neighbor.length
                    path_edges.append((neighbor.src.loc, neighbor.dest.loc, '{:.0f}'.format(neighbor.length)))

            node = previous_node

        return {'cost': total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False):
        t1 = time.time()

        if use_heap:
            queue = HeapPriorityQueue(self.network)
        else:
            queue = UnsortedArrayPriorityQueue(self.network)

        queue.update_key(srcIndex, 0)

        # RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        for node in self.network.nodes:
            self.results[node.node_id] = {'dist': math.inf, 'prev': None}

        self.results[srcIndex]['dist'] = 0

        while queue.is_not_empty():
            u = queue.delete_min()
            edges = self.network.nodes[u['id']].neighbors
            for edge in edges:
                v = self.results[edge.dest.node_id]
                if v['dist'] > u['dist'] + edge.length:
                    v['dist'] = u['dist'] + edge.length
                    v['prev'] = u['id']
                    queue.update_key(edge.dest.node_id, v["dist"])

        t2 = time.time()
        return t2-t1


class UnsortedArrayPriorityQueue:
    def __init__(self, graph):
        self.num_nodes = len(graph.nodes)
        self.queue = {}

        for index in range(self.num_nodes):
            self.queue[graph.nodes[index].node_id] = {'dist': math.inf}

    def delete_min(self):
        smallest_index = -1
        smallest_distance = math.inf

        for index, node in self.queue.items():
            if self.queue[index]['dist'] < smallest_distance:
                smallest_distance = self.queue[index]['dist']
                smallest_index = index
        smallest_node = {'id': smallest_index, 'dist': smallest_distance}
        if smallest_index is -1:
            first_node = self.queue.popitem()
            return {'id': first_node[0], 'dist': first_node[1]['dist']}
        del self.queue[smallest_index]
        return smallest_node

    def update_key(self, index, distance):
        self.queue[index]['dist'] = distance

    def is_not_empty(self):
        if len(self.queue) > 0:
            return True
        else:
            return False


class HeapPriorityQueue():
    def __init__(self, graph):
        self.num_nodes = len(graph.nodes)
        self.queue = {}

        for index in range(self.num_nodes):
            self.queue[graph.nodes[index].node_id] = {'dist': math.inf}

    def delete_min(self):
        smallest_index = -1
        smallest_distance = math.inf

        for index, node in self.queue.items():
            if self.queue[index]['dist'] < smallest_distance:
                smallest_distance = self.queue[index]['dist']
                smallest_index = index
        smallest_node = {'id': smallest_index, 'dist': smallest_distance}
        if smallest_index is -1:
            first_node = self.queue.popitem()
            return {'id': first_node[0], 'dist': first_node[1]['dist']}
        del self.queue[smallest_index]
        return smallest_node

    def update_key(self, index, distance):
        self.queue[index]['dist'] = distance

    def is_not_empty(self):
        if len(self.queue) > 0:
            return True
        else:
            return False
