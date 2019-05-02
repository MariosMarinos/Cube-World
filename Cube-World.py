from string import ascii_uppercase
from collections import deque
import sys
import time
import itertools
import heapq
LETTERS = {letter: str(index) for index, letter in enumerate(ascii_uppercase, start=0)}
PERIOD_OF_TIME = 600  # after 10 mins the program stops.


class Node():

    def __init__(self, state, parent, h, g):
        self.state = state  # LIST
        self.parent = parent  # Another object Node as parent
        self.h = h  # heuristic value for this Node
        self.g = g  # the depth of this node


def CheckIfSolution(current_node, goal_node):
    if current_node == goal_node:
        print('SUCCESS')
        return True


def convertValueToKey(index):
    return list(LETTERS.keys())[list(LETTERS.values()).index(str(index))]
    # converting the number to letter. (0 to A, 1 to B, GetNumberOfCubes)
    pass


def convertListsToMoves(currently_state, next_state):
    i = 0
    index = -1  # index of the changing element
    while i < len(currently_state):
        # cheking each one of the elements in state
        if currently_state[i] != next_state[i]:
            # finding the position of changing element.
            index = i
            break
        i += 1
    # getting the Letter for first parameter
    temp = convertValueToKey(index)
    # getting the begging position of the cube.
    if currently_state[index] == -1:
        # if its -1 its on table.
        temp1 = 'table'
    else:
        tempnum = currently_state[index]
        # helping variable for current position and then convert it.
        temp1 = convertValueToKey(tempnum)
    # getting the final position of the cube with the same way as the begging.
    if next_state[index] == -1:
        temp2 = 'table'
    else:
        tempnum = next_state[index]  # helping variable
        temp2 = convertValueToKey(tempnum)
    print('Move(', temp, ',', temp1, ',', temp2, ')')


def PathToSolution(node, init_state):
    tempNode = node  # currently state (solution)
    Moves = list()  # empty list for saving the moves.
    while True:
        Moves.append(tempNode.state)
        if tempNode.state == init_state.state:
            break  # append till solution becomes init state.
        else:
            tempNode = tempNode.parent
            # if the currently state isnt the init go to his parent
    tempList = list(reversed(Moves))
    # when it ends reverse the moves to find the path from begging to end
    # because we have the path from end to begging
    for index, item in enumerate(tempList):
        # for each one of the Moves in tempList convert it to Moves(A,B,C) for example.
        if index == len(tempList) - 1:
            # if it has reached the end stop it.
            break
        convertListsToMoves(tempList[index], tempList[index+1])
    return len(tempList) - 1


def getHeuristic():
    pass


def FindChildren(node, OldStates):
    children = list()  # empty list for the children
    ClearCubes = findClearCubes(len(node.state), node.state)  # find the clear cubes.
    # for index, pointer in enumerate(ClearCubes):
    #     for i in range(len(ClearCubes)):
    # for each clear cube
    # index is for which cube and pointer is
    for (index, pointer), i in itertools.product(enumerate(ClearCubes), range(len(ClearCubes))):
        copied_state = node.state.copy()  # copy the state
        if i != index:
            copied_state[pointer] = ClearCubes[i]
            if tuple(copied_state) in OldStates:
                # if state is already used dont make the child.
                continue
            # creating the kid.
            temp_node = Node(copied_state, node, getHeuristic(), node.g+1)
            # if the kid has parent and is not the same as the parent append it.
            if node.parent is not None:
                if temp_node.state != node.parent.state:
                    children.append(temp_node)
            else:
                children.append(temp_node)  # is just for the first state.
        elif node.state[pointer] != -1:  # if it's not on the table it can go on the table.
            copied_state[pointer] = -1
            # the else are  same as before.
            if tuple(copied_state) in OldStates:
                continue
            temp_node = Node(copied_state, node, getHeuristic(), node.g+1)
            if node.parent is not None:
                if temp_node.state != node.parent.state:
                    children.append(temp_node)
            else:
                children.append(temp_node)
    return children


def search(Algorithm, init_state, final_state):
    start = time.time()  # begging time of search algorithm
    OldStates = set()  # set for already tested nodes
    children = list()  # list with childrens filled from FindChildren
    length = 0
    Frontier = deque()  # Frontier
    Frontier.append(init_state)  # Frontier Append the init state.
    i = 0  # How many iterations were need(Nodes tested)
    while Frontier:
        if (time.time() > start + PERIOD_OF_TIME):
            return 0, 0, 0  # if the given time expires stop the program.
        currently_state = Frontier.pop()  # popping currently state on deque.
        if tuple(currently_state.state) in OldStates:
            # converting the list state into tuple to have it in set.
            continue
        i += 1  # increase the iterations if the node is going to be tested.
        if CheckIfSolution(currently_state.state, final_state.state):
            # if it is solution stop and return the path, iterations, and time needed
            print("childrens :", length)
            print(len(Frontier))
            return PathToSolution(currently_state, init_state), i, time.time()-start
        children = FindChildren(currently_state, OldStates)  # find the children.
        length = length + len(children)
        if Algorithm == 'BFS':  # if BFS append from left in Frontier.
            for item in children:
                Frontier.appendleft(item)
        elif Algorithm == 'DFS':  # if DFS just append in Frontier.
            tempchild = list((children))
            for item in tempchild:
                Frontier.append(item)
        print(len(Frontier))
        OldStates.add(tuple(currently_state.state))


def search_heuristic(Algorithm, init_state, final_state):
    start = time.time()  # begging time of search algorithm
    OldStates = set()  # set for already tested nodes
    children = list()  # list with childrens filled from FindChildren
    length = 0
    Frontier = list()  # Frontier
    heapq.heapify(Frontier)
    heapq.heappush(Frontier, init_state)   # Frontier Append the init state.
    i = 0  # How many iterations were need(Nodes tested)
    while Frontier:
        if (time.time() > start + PERIOD_OF_TIME):
            return 0, 0, 0  # if the given time expires stop the program.
        currently_state = heapq.heappop(Frontier)  # popping currently state on deque.
        if tuple(currently_state.state) in OldStates:
            # converting the list state into tuple to have it in set.
            continue
        i += 1  # increase the iterations if the node is going to be tested.
        if CheckIfSolution(currently_state.state, final_state.state):
            # if it is solution stop and return the path, iterations, and time needed
            print("childrens :", length)
            print(len(Frontier))
            return PathToSolution(currently_state, init_state), i, time.time()-start
        children = FindChildren(currently_state, OldStates)  # find the children.
        length = length + len(children)
        if Algorithm == 'BFS':
            for item in children:
                heapq.heappush(Frontier, item)
    pass


def findClearCubes(N, state):
    AvailableCubes = list()  # list for AvailableCubes
    # when the cube doesn't appear in state it means that it's clear.
    # example : [1,-1,-1] means that 2(C cube) and 0(A cube) are free.
    for i in range(0, N):
        if i not in state:
            AvailableCubes.append(i)
    return AvailableCubes


def OpenFile(fileName):
    File_list = list()
    with open(fileName) as fp:
        for i, line in enumerate(fp):
            if i > 1:
                File_list.append(line)
    return File_list


def process_File(FileName):
    FileList = OpenFile(FileName)
    N = GetNumberOfCubes(FileList[0])
    return N, GetInitState(N, FileList[1]), GetGoalState(N, FileList[2])
    # you need to combine the init state
    #  in one line and goal state otherwise it won't WORK!


def OnTableOn(list, state):
    for element in list:
        if "CLEAR" in element:
            continue
        elif "ONTABLE" in element:
            temp = element.replace(' ', '').replace('ONTABLE', '')
            # removing whitespaces and ontable so i have only the cube left
            tempnum = int(LETTERS.get(temp))  # converting string to init
            state[tempnum] = -1  # -1 for on table status
        elif "ON" in element:
            temp = element.replace(' ', '').replace('ON', '')
            # temp will contain 2 letters A B for example and that
            # means A cube is on top of B cube
            tempnum_ontop = int(LETTERS.get(temp[0]))  # get A cube as integer
            tempnum_bottom = int(LETTERS.get(temp[1]))  # get B cube as integer
            state[tempnum_ontop] = tempnum_bottom
    return state


def GetNumberOfCubes(line):
    x = line.split()
    return len(x)-2
    # defines the number of cubes by splitting and
    # leaving out the last and first element.


# defining the start_state of the problem.
def GetInitState(N, list):
    x = list.replace('HANDEMPTY', '')
    fixed = x[7:len(x)-4]  # removing init,handempty and the parenthesis
    # of it to get only the positions of init state.
    fixed2 = fixed.replace('(', '').split(')')
    start_state = [None] * N  # empty list for start_state
    OnTableOn(fixed2, start_state)
    root_node = Node(start_state, None, 0, 0)
    return root_node


# definging the goal_state of the problem.
def GetGoalState(N, line):
    goal_state = [-1] * N
    fixed2 = line[13:].replace(')', '').split('(')
    OnTableOn(fixed2, goal_state)
    return Node(goal_state, None, 0, 0)


if __name__ == "__main__":
    N, init_state, goal_state = process_File(sys.argv[2])
    print('init state :', init_state.state, ' goal state :', goal_state.state)
    MovesMade, NodesTested, Time = search(sys.argv[1], init_state, goal_state)
    print('Nodes Tested were :', NodesTested)
    print('Moves were made :', MovesMade)
    print('Time needed was :', Time, 'seconds.')
