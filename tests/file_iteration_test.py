# Python imports

# Third party imports

# Local imports

# Declarations
text = """
Slope:                   1.0            Intercept:          0.0
COV Limit:               1.0            


                                     - 373 -
"""
DUMMY_FILE = './dummy-text.txt'

#%%
with open(DUMMY_FILE, 'wt', encoding='UTF-8') as file:
    file.write(text)

with open(DUMMY_FILE, 'rt', encoding='UTF-8') as file:
    start = file.seek(0, 0) # start
    stop = file.seek(0, 2) # stop
    file.seek(0, 0)

    while file.tell() < stop:
        print("Before position: ", file.tell())
        line = file.readline()
        print("After position: ", file.tell())
        if file.tell() > stop:
            print(line.encode('UTF-8'))

with open(DUMMY_FILE, 'rb') as file:
    start = file.seek(0, 0) # start
    stop = file.seek(0, 2) # stop
    file.seek(0, 0)

    while file.tell() < stop:
        print("Before position: ", file.tell())
        line = file.readline()
        print("After position: ", file.tell())
        if file.tell() > stop:
            print(line.encode('UTF-8'))