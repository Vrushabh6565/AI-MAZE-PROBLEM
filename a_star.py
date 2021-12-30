from node import *
from problem import *
import math
import heapq
import random
NODES_COUNT = 0


# A* search is similar to best first search with f = g + h (f = path cost + heuristic)
def a_star(problem, h=None):
    global NODES_COUNT
    NODES_COUNT = 0
    return best_first_search(problem, lambda n: n.path_cost + h(n, problem.goal))


# for bfs f = g and for A* f = g + h
def best_first_search(problem, f):
    global NODES_COUNT
    node = Node(problem.initial_state)
    frontier = PriorityQueue(f)
    explored = set()
    frontier.append(node)
    while len(frontier) > 0:
        node = frontier.get()
        explored.add(repr(node.state))
        if problem.goal_test(node.state):
            print("Solution was reached in {} steps".format(node.depth + 1))
            return solution(node), NODES_COUNT
        else:
            for action in problem.actions(node.state):
                child = child_node(problem, node, action)
                if repr(child.state) not in explored:
                    NODES_COUNT += 1
                    if child in frontier:
                        frontier_node = frontier[child]
                        if f(frontier_node) > f(child):
                            frontier.remove(frontier_node)
                            frontier.append(child)
                    else:
                        frontier.append(child)
    return 'failure', NODES_COUNT


# this heuristic simply return 0 so its used for BFS
def heuristic_1(node=None, goal=None):
    return 0


# this heuristic returns random number for h (0 <= h <= 99)
def heuristic_2(node=None, goal=None):
    return random.randint(0, 99)


# h = manhattan distance
def heuristic_3(node, goal):
    x_diff = abs(goal[0] - node.state.current_row)
    y_diff = abs(goal[1] - node.state.current_column)
    return x_diff + y_diff


# h = euclidean distance
def heuristic_4(node, goal):
    x_diff = (goal[0] - node.state.current_row)
    y_diff = (goal[1] - node.state.current_column)
    euclidean_value = (x_diff ** 2) + (y_diff ** 2)
    euclidean_value = math.sqrt(euclidean_value)
    return euclidean_value


# Chebychev Distance
def heuristic_5(node, goal):
    x_diff = abs(goal[0] - node.state.current_row)
    y_diff = abs(goal[1] - node.state.current_column)
    h = max(x_diff, y_diff)
    return h


# hamming distance
def heuristic_6(node, goal):
    h = 0
    x_diff = abs(goal[0] - node.state.current_row)
    y_diff = abs(goal[1] - node.state.current_column)
    for i in range(31, -1, -1):
        b1 = x_diff >> i & 1
        b2 = y_diff >> i & 1
        h += not(b1 == b2)
    return h


# MINKOWSKI DISTANCE (generalization of manhattan and euclidean distance)
def heuristic_7(node, goal):
    h = 0
    x_diff = abs(goal[0] - node.state.current_row)
    y_diff = abs(goal[1] - node.state.current_column)
    '''lambda set as 5'''
    h = ((x_diff ** 5) + (y_diff ** 5)) ** (1/5)
    return h

# Priority queue
class PriorityQueue:
    def __init__(self, f=lambda g: g):
        self.heap = []
        heapq.heapify(self.heap)
        self.f = f

    def append(self, node):
        heapq.heappush(self.heap, (self.f(node), node))

    def get(self):
        return heapq.heappop(self.heap)[1]

    def remove(self, node):
        for h in self.heap:
            if h[1] == node:
                self.heap.remove((h[0], node))
                heapq.heapify(self.heap)

    def __contains__(self, node):
        for h in self.heap:
            if h[1] == node:
                return True
        return False

    def __getitem__(self, node):
        for h in self.heap:
            if h[1] == node:
                return h[1]

    def __len__(self):
        return len(self.heap)
