from string import ascii_uppercase
from collections import deque
LETTERS = {letter: str(index) for index, letter in enumerate(ascii_uppercase, start=0)}


class Node():
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent


def CheckIfSolution(state, final_state):
    if state == final_state:
        return True


def FindChildren(state):
    children = list()
    copied_state = state.copy()
    ClearCubes = findClearCubes(len(state), state)
    print(ClearCubes)
    for index, pointer in enumerate(ClearCubes):
        print(index, pointer)
        for item in ClearCubes:
            





def BFS(init_state, final_state):
    OldStates = {}
    children = list()
    Frontier = deque()
    Frontier.append(init_state)
    # while Frontier:
    currently_state = Frontier.popleft()
    # if (currently_state in OldStates):
    if CheckIfSolution(currently_state, final_state):
        return 1
    children = FindChildren(currently_state)
    print(currently_state)


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
    return start_state


def GetGoalState(N, line):
    goal_state = [-1] * N
    fixed2 = line[13:].replace(')', '').split('(')
    OnTableOn(fixed2, goal_state)
    return goal_state


if __name__ == "__main__":
    N, init_state, goal_state = process_File()
    print(init_state, goal_state)
    BFS(init_state, goal_state)
