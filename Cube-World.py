
def OpenFile() :
    fname = input("Enter file name: ")
    try:
        fh = open(fname)
    except Exception as e:
        print ('Sorry your file cannot be opened ')
        quit()


if __name__ == "__main__" :
