
def OpenFile() :
    fname = input("Enter file name: ")
    with open(fname) as fp:
        for i, line in enumerate(fp):
            if i >1: #2nd line
                    


if __name__ == "__main__" :
