class Node():
    def __init__(self, list):
        self.list = list()


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
    x = FileList[0].split()
    N = len(x)-2  # defines the number of cubes by splitting and
    # leaving out the last and first element.
    print(FileList[1])
    print(N)
    return N


if __name__ == "__main__":
    process_File()
