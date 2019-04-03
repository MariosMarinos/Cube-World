from string import ascii_uppercase
from collections import deque
LETTERS = {letter: str(index) for index, letter in enumerate(ascii_uppercase, start=0)}


class Node():

    def __init__(self, state, parent):
        self.state = state  # LIST
        self.parent = parent  # Another object Node as parent


def CheckIfSolution(current_node, goal_node):
    if current_node == goal_node:
        print('SUCCESS')
        return True


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
    print('Moves needed were', len(tempList)-1, 'and are these :', tempList)


def FindChildren(node):
    children = list()
    ClearCubes = findClearCubes(len(node.state), node.state)
    for index, pointer in enumerate(ClearCubes):
        for i in range(len(ClearCubes)):
            copied_state = node.state.copy()
            if i != index:
                copied_state[pointer] = ClearCubes[i]
                temp_node = Node(copied_state, node)
                children.append(temp_node)
            elif node.state[pointer] != -1:
                copied_state[pointer] = -1
                temp_node = Node(copied_state, node)
                children.append(temp_node)
    """
    print('expanded')
    for item in children:
        print(item.state)
    """
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
        if CheckIfSolution(currently_state.state, final_state.state):
            print(i)
            return PathToSolution(currently_state, init_state)
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
        i = i + 1


def findClearCubes(N, state):
    AvailableCubes = list()
    for i in range(0, N):
        if i not in state:
            AvailableCubes.append(i)
    return AvailableCubes


def OpenFile():
    File_list = list()
    fname = input("Enter file name: ")
    with open(fname) as fp:
        for i, line in enumerate(fp):
            if i > 1:
                File_list.append(line)
    return File_list


def process_File():
    FileList = OpenFile()
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


#  defining the start_state of the problem.
def GetInitState(N, list):
    x = list.replace('HANDEMPTY', '')
    fixed = x[7:len(x)-4]  # removing init,handempty and the parenthesis
    # of it to get only the positions of init state.
    fixed2 = fixed.replace('(', '').split(')')
    start_state = [None] * N  # empty list for start_state
    OnTableOn(fixed2, start_state)
    root_node = Node(start_state, None)
    return root_node


def GetGoalState(N, line):
    goal_state = [-1] * N
    fixed2 = line[13:].replace(')', '').split('(')
    OnTableOn(fixed2, goal_state)
    return Node(goal_state, None)


if __name__ == "__main__":
    N, init_state, goal_state = process_File()
    Solution = search('DFS', init_state, goal_state)
    print('init state :', init_state.state, ' goal state :', goal_state.state)
