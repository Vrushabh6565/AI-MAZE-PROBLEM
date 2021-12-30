from ids import *
from a_star import *
import copy
import sys
from turtle_maze import *
from colorama import Fore,Style
import time

# defining of maze problem
class Problem:
    def __init__(self, initial_state, maze, goal=None):
        self.initial_state = initial_state
        self.maze = maze
        self.action_list = [self.go_up, self.go_right, self.go_down, self.go_left]
        self.goal = goal

    def __repr__(self):
        return '{} -> {}'.format(self.initial_state, self.goal)

    # this function will take current state as a input and and calculate the possible possible actions it can take next
    # returns the list of possible actions
    def actions(self, state):
        state_actions = []

        # check if its possible to go up
        # step 1 => in this first we check if row number is > 0
        # step 2 => then we go into same column of previous row and check if it is 0
        # step 3 => if it is zero then we check if it is previously visited or not
        # step 4 => if not visited then add it into possible actions list
        if(state.current_row > 0):
            if(self.maze[state.current_row - 1][state.current_column] == '0'):
                if(not state.is_visited(state.current_row - 1, state.current_column)):
                    state_actions.append(self.action_list[0])

        # lly for go right we follow 4 steps
        if(state.current_column < len(self.maze[0]) - 1):
            if(self.maze[state.current_row][state.current_column + 1] == '0'):
                if(not state.is_visited(state.current_row, state.current_column + 1)):
                    state_actions.append(self.action_list[1])

        # lly for go down we follow 4 steps
        if(state.current_row < len(self.maze) - 1):
            if(self.maze[state.current_row + 1][state.current_column] == '0'):
                if(not state.is_visited(state.current_row + 1, state.current_column)):
                    state_actions.append(self.action_list[2])

        # lly for go left we follow 4 steps
        if (state.current_column > 0):
            if(self.maze[state.current_row][state.current_column - 1] == '0'):
                if(not state.is_visited(state.current_row, state.current_column - 1)):
                    state_actions.append(self.action_list[3])
        return state_actions

    # this will call the action function and return the possible states returned by action()
    def result(self, state, action):
        new_state = action(state)
        return new_state

        # move one state up and return new state
    def go_up(self, state):

        return MazeState(state.current_row - 1, state.current_column)

        # move one state right and return new state
    def go_right(self, state):
        return MazeState(state.current_row, state.current_column + 1)

        # move one step down and return new state
    def go_down(self, state):
        return MazeState(state.current_row + 1, state.current_column)

    # move one state left and return new state
    def go_left(self, state):
        # visited = copy.deepcopy(state.visited)
        # visited.append((state.current_column, state.current_row))
        return MazeState(state.current_row, state.current_column - 1)

    # this function do goal_test on state given in argument
    # return 1 if given state is goal state goal else return 0
    def goal_test(self, state):
        if(self.goal[0] == state.current_row and self.goal[1] == state.current_column):
            return 1
        else:
            return 0

    # print solution on terminal
    # here our solution path is given as input
    # solution path is marked with *
    def show_path(self, path):
        if type(path) is list:
            solution = copy.deepcopy(self.maze)
            for p in path:
                solution[p.current_row][p.current_column] = 'X'
            for row in solution:
                print(row)
            return solution
        else:
            print(f'{Fore.RED}{Style.BRIGHT}NOT ABLE TO FIND ANY SOLUTION{Style.RESET_ALL}')
            return None


# this class is create an instance for each state in the maze
# it store row_number, column_number and is stated visited or not
class MazeState:
    def __init__(self, current_row, current_column, visited=[]):
        self.visited = visited
        self.current_row = current_row
        self.current_column = current_column

    def __repr__(self):
        return '({}, {})'.format(self.current_row, self.current_column)

    def __eq__(self, other):
        return repr(self) == repr(other)

    # check if state at given (row, column) is visited or not
    def is_visited(self, row, column):
        if((row, column) in self.visited):
            return 1
        else:
            return 0


def formulate_maze_problem(file):
    with open(file, "r") as file:
        parsed_list = [line.strip().split() for line in file.readlines()]
    maze = parsed_list
    # Set starting point
    start_row, start_column = set_starting_point(maze)

    # If starting point is an obstacle, return none
    if(start_row is None and start_column is None):
        return None
    # Mark the starting point as X
    maze[start_row][start_column] = 'X'
    goal_row, goal_column = set_goal(maze)

    # If goal coordinates has an obstacle, return none
    if goal_row is None and goal_column is None:
        return None

    p = Problem(MazeState(start_row, start_column), maze, [goal_row, goal_column])
    return p

def set_starting_point(maze):
    print("according to file | ROW: {0} | COLUMNS: {1} |".format(len(maze), len(maze[0])))
    input_row = int(input("Enter start state row : "))
    input_col = int(input("Enter start state column : "))
    row, column = None, None
    if(input_row < len(maze) and input_col < len(maze[0])):
        row = input_row
        column = input_col
    else:
        print("specified row,column is out of range of maze provided")
        return row, column
    if maze[row][column] == '0':
        print("STARTING POINT SET TO ({0},{1})".format(row,column))
    else:
        print("unable to enter into the maze from given location")
    return row, column


def set_goal(maze):
    input_row = int(input("Enter goal state row : "))
    input_col = int(input("Enter goal state column : "))
    row, column = None, None
    if (input_row < len(maze) and input_col < len(maze[0])):
        row = input_row
        column = input_col
    else:
        print("specified row,column is out of range of maze provided")
        return row, column
    if maze[row][column] == '0':
        print("GOAL POINT SET TO ({0},{1})".format(row, column))
    else:
        print("unable to find reachable goal location")
    return row, column


def main(argv):
    problem = formulate_maze_problem(argv[1])
    print("1. NO HEURISTIC (BFS)")
    print("2. RANDOM NUMBER AS HEURISTIC")
    print("3. MANHATTAN DISTANCE")
    print("4. EUCLIDEAN DISTANCE")
    print("5. CHEBYCHEV DISTANCE")
    print("6. HAMMING DISTANCE")
    print("7. MINKOWSKI DISTANCE")
    print("8. IDS")
    choice = int(input("select Heuristic : "))
    if problem:
        if(choice == 1):
            start = time.time()
            path1, nodes_count1 = a_star(problem, heuristic_1)
            if path1 and nodes_count1 and (choice == 1):
                print("\nA* search with Heuristic 1: h(n) = 0")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count1)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count1) / len(path1)))
                solution1 = problem.show_path(path1)
                end = time.time()
                print("TIME = ", end-start)
                if solution1:
                    draw_maze(solution1)

        elif(choice == 2):
            start = time.time()
            path2, nodes_count2 = a_star(problem, heuristic_2)
            if path2 and nodes_count2 and (choice == 2):
                print("\nA* search with Heuristic 2: Random num from 0 till 99")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count2)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count2) / len(path2)))
                solution2 = problem.show_path(path2)
                end = time.time()
                print("TIME = ", end - start)
                if solution2:
                    draw_maze(solution2)

        elif(choice == 3):
            start = time.time()
            path3, nodes_count3 = a_star(problem, heuristic_3)
            if path3 and nodes_count3 and (choice == 3):
                print("\nA* search with Heuristic 3: Manhattan distance")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count3)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count3) / len(path3)))
                solution3 = problem.show_path(path3)
                end = time.time()
                print("TIME = ", end - start)
                if solution3:
                    draw_maze(solution3)

        elif(choice == 4):
            start = time.time()
            path4, nodes_count4 = a_star(problem, heuristic_4)
            if path4 and nodes_count4:
                print("\nA* search with Heuristic 4: Euclidean distance")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count4)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count4) / len(path4)))
                solution4 = problem.show_path(path4)
                end = time.time()
                print("TIME = ", end - start)
                if solution4:
                    draw_maze(solution4)

        elif(choice == 5):
            start = time.time()
            path5, nodes_count5 = a_star(problem, heuristic_5)
            if path5 and nodes_count5:
                print("\nA* search with Heuristic 5: Chebychev distance")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count5)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count5) / len(path5)))
                solution5 = problem.show_path(path5)
                end = time.time()
                print("TIME = ", end - start)
                if solution5:
                    draw_maze(solution5)

        elif (choice == 6):
            start = time.time()
            path6, nodes_count6 = a_star(problem, heuristic_6)
            if path6 and nodes_count6:
                print("\nA* search with Heuristic 6: HAMMING DISTANCE")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count6)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count6) / len(path6)))
                solution6 = problem.show_path(path6)
                end = time.time()
                print("TIME = ", end - start)
                if solution6:
                    draw_maze(solution6)

        elif (choice == 7):
            start = time.time()
            path7, nodes_count7 = a_star(problem, heuristic_7)
            if path7 and nodes_count7:
                print("\nA* search with Heuristic 7: MINKOWSKI DISTANCE")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count7)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count7) / len(path7)))
                solution7 = problem.show_path(path7)
                end = time.time()
                print("TIME = ", end - start)
                if solution7:
                    draw_maze(solution7)

        elif(choice == 8):
            start = time.time()
            path_ids, nodes_count_ids = ids(problem)
            if path_ids and nodes_count_ids:
                print("IDS - Depth currently on is displayed for reference")
                # Effective branching factor calculation
                print("No of nodes generated : ", nodes_count_ids)
                print("Effective branching factor is : ", math.exp(math.log(nodes_count_ids) / len(path_ids)))
                solution = problem.show_path(path_ids)
                end = time.time()
                print("TIME = ", end - start)
                if solution:
                    draw_maze(solution)
        else:
            print("wrong choice")

    else:
        print('No Solution')


if __name__ == '__main__':
    main(sys.argv)
