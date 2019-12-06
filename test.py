from utils import get_files_with_extension, read_file
import os.path
tour = ['Soda', 'Dwinelle', 'Campanile', 'Barrows', 'Soda']
dropDict = {"Soda":["Cory"], "Dwinelle": ["Wheeler", "RSF"], "Campanile": ["Campanile"]}
# Soda Dwinelle Campanile Barrows Soda
# 3
# Soda Cory
# Dwinelle Wheeler RSF
# Campanile Campanile
def output(inputFileName, tour, dropDict):
    output = inputFileName.replace(".in", ".out")
    output = output.replace("/Users/panerdavid/Desktop/170/inputs_copy/", "")
    savePath = "/Users/panerdavid/Desktop/170/outputs/"
    completeName = os.path.join(savePath, output)
    print(completeName)
    f = open(completeName, "w+")
    for location in tour:
        f.write(location + " ")
    f.write("\n")
    f.write(str(len(dropDict)) + "\n")
    
    for dropoff in dropDict:
        f.write(dropoff)
        for home in dropDict[dropoff]:
            f.write(" " + home)
        f.write("\n")

    f.close()
files = get_files_with_extension("/Users/panerdavid/Desktop/170/inputs_copy", 'in')
for f in files:
    output(f, tour, dropDict)
