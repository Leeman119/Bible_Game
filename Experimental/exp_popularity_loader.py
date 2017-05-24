import os
from exp_scripture_finder import ScriptureFinder

sfind = ScriptureFinder()

# Look through txt files in the Literature TXTs folder and put all text into a single string variable.
for filename in os.listdir('D:/PythonProjects/Bible_Game/Literature TXTs'):
    line = []
    if filename.endswith(".txt"):
        with open('D:/PythonProjects/Bible_Game/Literature TXTs/'+filename, 'r') as file:
            file_lines = file.readlines()
        scriptures = sfind.run(file_lines)
        # print(filename)
        # print(scriptures)

