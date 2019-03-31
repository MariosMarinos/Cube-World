from string import ascii_uppercase
LETTERS = {letter: str(index) for index, letter in enumerate(ascii_uppercase, start=0)}


def findClearCubes(N, state):
    AvailableCubes = list()
    for i in range(0, N):
        if i not in state:
            AvailableCubes.append(i)
    print(AvailableCubes)


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
    GetInitState(N, FileList[1])
    GetGoalState(N, FileList[2])
    # you need to combine the init state
    #  in one line and goal state as well otherwise it won't WORK!


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
    print(OnTableOn(fixed2, start_state))
    x = findClearCubes(N, start_state)
    print(x)

def GetGoalState(N, line):
    goal_state = [-1] * N
    fixed2 = line[13:].replace(')', '').split('(')
    print(OnTableOn(fixed2, goal_state))
    return goal_state


if __name__ == "__main__":
    process_File()
