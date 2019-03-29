
def OpenFile() :
    fname = input("Enter file name: ")
    with open(fname) as fp:
        for i ,line in enumerate(fp):
            if i>1 :
                print (line)


if __name__ == "__main__" :
    OpenFile()
