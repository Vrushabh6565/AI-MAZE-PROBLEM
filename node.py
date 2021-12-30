class Node:
    def __init__(self, state, parent=None, action=None, path_cost=1):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        if parent:
            self.path_cost += parent.path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.path_cost < other.path_cost


# generate node of given state
def make_node(state):
    return Node(state)


# return path from start to goal location
def solution(node):
    path = [node.state]
    while node.parent:
        path.append(node.parent.state)
        node = node.parent
    return list(reversed(path))


# Explore the state and return the child nodes
def child_node(problem, node, action):
    return Node(problem.result(node.state, action), node, action)
