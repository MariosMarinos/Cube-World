from string import ascii_uppercase
from collections import deque
import sys
LETTERS = {letter: str(index) for index, letter in enumerate(ascii_uppercase, start=0)}


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
    pass


def convertListsToMoves(list1, list2):
    i = 0
    index = -1  # index of the changing element
    while i < len(list1):
        if list1[i] != list2[i]:
            index = i
            break
        i += 1
    temp = convertValueToKey(index)
    if list1[index] == -1:
        temp1 = 'table'
    else:
        tempnum = list1[index]  # helping variable
        temp1 = convertValueToKey(tempnum)
        pass
    if list2[index] == -1:
        temp2 = 'table'
    else:
        tempnum = list2[index]  # helping variable
        temp2 = convertValueToKey(tempnum)
    print('Move(', temp, ',', temp1, ',', temp2, ')')


def PathToSolution(node, init_state):
    tempNode = node
    Moves = list()
    while True:
        Moves.append(tempNode.state)
        if tempNode.state == init_state.state:
            break
        else:
            tempNode = tempNode.parent
    tempList = list(reversed(Moves))
    for index, item in enumerate(tempList):
        if index == len(tempList) - 1:
            break
        convertListsToMoves(tempList[index], tempList[index+1])
    return len(tempList) - 1


def getHeuristic():
    pass


def FindChildren(node):
    children = list()
    ClearCubes = findClearCubes(len(node.state), node.state)
    for index, pointer in enumerate(ClearCubes):
        for i in range(len(ClearCubes)):
            copied_state = node.state.copy()
            if i != index:
                copied_state[pointer] = ClearCubes[i]
                temp_node = Node(copied_state, node, getHeuristic(), node.g+1)
                if node.parent is not None:
                    if temp_node.state != node.parent.state:
                        children.append(temp_node)
                else:
                    children.append(temp_node)
            elif node.state[pointer] != -1:
                copied_state[pointer] = -1
                temp_node = Node(copied_state, node, getHeuristic(), node.g+1)
                if node.parent is not None:
                    if temp_node.state != node.parent.state:
                        children.append(temp_node)
                else:
                    children.append(temp_node)
    return children


def search(Algorithm, init_state, final_state):
    OldStates = list()
    children = list()
    Frontier = deque()
    Frontier.append(init_state)
    i = 0
    while Frontier:
        currently_state = Frontier.pop()
        if currently_state.state in OldStates:
            continue
        print('currently_state : ', currently_state.state, 'and depth is :', currently_state.g)
        i += 1
        if CheckIfSolution(currently_state.state, final_state.state):
            return PathToSolution(currently_state, init_state), i
        children = FindChildren(currently_state)
        if Algorithm == 'BFS':
            for item in children:
                Frontier.appendleft(item)
        elif Algorithm == 'DFS':
            tempchild = list(reversed(children))
            for item in tempchild:
                Frontier.append(item)
        if currently_state.state not in OldStates:
            OldStates.append(currently_state.state)


def findClearCubes(N, state):
    AvailableCubes = list()
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
    MovesMade, NodesTested = search(sys.argv[1], init_state, goal_state)
    print('Nodes Tested were :', NodesTested)
    print('Moves were made :', MovesMade)
