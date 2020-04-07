import pickle

PICKLE_FILE = "mapasgraph.pickle"


def main():

    with open(PICKLE_FILE, "rb") as inpFile,\
            open("mapasgraph.txt", "w") as outFile:
        try:
            while True:
                outFile.write(str(pickle.load(inpFile)))
        except EOFError:
            pass


if __name__ == "__main__":
    main()
