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
        print("getShortestPath")
        self.dest = destIndex
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.dest]

        while self.results[node.node_id]["prev"] is not None:  # Traverse the graph backwards
            previous_node = self.network.nodes[self.results[node.node_id]['prev']]

            for neighbor in previous_node.neighbors:
                if neighbor.dest is node:
                    total_length = total_length + neighbor.length
                    path_edges.append((neighbor.src.loc, neighbor.dest.loc, '{:.0f}'.format(neighbor.length)))

            node = previous_node

        return {'cost': total_length, 'path':path_edges}

    def computeShortestPaths(self, src_index, use_heap=False):
        print("computeShortestPaths")
        t1 = time.time()

        if use_heap:
            queue = HeapPriorityQueue(self.network, src_index)
        else:
            queue = UnsortedArrayPriorityQueue(self.network, src_index)

        for node in self.network.nodes:
            self.results[node.node_id] = {'dist': math.inf, 'prev': None}

        self.results[src_index]['dist'] = 0

        print("Started queue")
        while queue.is_not_empty():
            print("Queue length: ", len(queue))
            u = queue.delete_min()
            edges = self.network.nodes[u['id']].neighbors
            for edge in edges:
                v = self.results[edge.dest.node_id]
                # v2 = edge.dest
                if v['dist'] > u['dist'] + edge.length:
                    v['dist'] = u['dist'] + edge.length
                    v['prev'] = u['id']
                    queue.decrease_key(edge.dest.node_id)
                    queue.update_node(edge.dest.node_id, v["dist"])
        print("Finished queue")

        t2 = time.time()
        print(t2-t1)
        return t2-t1


class UnsortedArrayPriorityQueue:
    def __init__(self, graph, source_index):
        print("Start init for array pq")
        self.num_nodes = len(graph.nodes)
        self.queue = {}

        for index in range(self.num_nodes):
            if index == source_index:
                self.queue[graph.nodes[index].node_id] = {'dist': 0}
            else:
                self.queue[graph.nodes[index].node_id] = {'dist': math.inf}
        print("Finish init for array pq")

    def delete_min(self):
        print("started delete")
        smallest_index = -1
        smallest_distance = math.inf

        for index, node in self.queue.items():
            if self.queue[index]['dist'] < smallest_distance:
                smallest_distance = self.queue[index]['dist']
                smallest_index = index
        smallest_node = {'id': smallest_index, 'dist': smallest_distance}
        if smallest_index is -1:
            first_node = self.queue.popitem()
            print("Finished delete")
            return {'id': first_node[0], 'dist': first_node[1]['dist']}
        del self.queue[smallest_index]
        print("Finished delete")
        return smallest_node

    def update_node(self, index, distance):
        self.queue[index]['dist'] = distance

    def is_not_empty(self):
        if len(self.queue) > 0:
            return True
        else:
            return False

    def decrease_key(self, foo):
        pass


class HeapPriorityQueue:
    def __init__(self, graph, src_index):
        self.heap = []

        for node in graph.nodes:
            if node.node_id == src_index:
                self.insert_node(node.node_id, 0)
            else:
                self.insert_node(node.node_id, math.inf)


    def __len__(self):
        return len(self.heap) - 1

    def insert_node(self, node_id, distance):
        print("started insert")
        self.heap.append({'id': node_id, 'dist': distance})
        self.percolate_up(len(self))
        print("Finished insert")

    def delete_min(self):
        print("Started delete min")
        return_node = self.heap[0]
        self.heap[0] = self.heap[len(self)]
        self.heap.pop()
        self.percolate_down(0)
        print("Ended delete min")
        return return_node

    def decrease_key(self, node_id):
        self.percolate_up(node_id)

    def percolate_up(self, index):
        if index is 0:
            return

        parent_index = index // 2
        if self.heap[parent_index]['dist'] > self.heap[index]['dist']:
            self.swap_node(index, parent_index)
            self.percolate_up(parent_index)

    def percolate_down(self, parent_index):
        print("started percolate_down")
        if parent_index is len(self):
            return

        while parent_index * 2 <= len(self):
            mc = self.min_child(parent_index)
            if self.heap[parent_index]["dist"] > self.heap[mc]["dist"]:
                self.swap_node(mc, parent_index)
            parent_index = mc
        print("finished percolate_down")

    def min_child(self, index):
        print("started min_child")
        if index * 2 + 1 > len(self):
            print("finished min_child")
            return index * 2

        if self.heap[index * 2]['dist'] < self.heap[index * 2 + 1]["dist"]:
            print("finished min_child")
            return index * 2

        print("finished min_child")
        return index * 2 + 1

    def update_node(self, node_id, distance):  # todo check to see if this is being used
        for node in self.heap:
            if node['id'] is node_id:
                node["dist"] = distance
                break

    def swap_node(self, index_1, index_2):
        node = self.heap[index_1]
        self.heap[index_1] = self.heap[index_2]
        self.heap[index_2] = node

    def is_not_empty(self):
        if len(self) > 0:
            return True
        else:
            return False
