import os
from scripture_finder import ScriptureFinder

Finder = ScriptureFinder()

# Look through txt files in the Literature TXTs folder and put all text into a single string variable.
for filename in os.listdir('Literature TXTs'):
    line = []
    if filename.endswith(".txt"):
        with open('Literature TXTs/'+filename, 'r') as file:
            file_lines = file.readlines()
            for l in file_lines:
                line.append(l)
        text = ''.join(line)
        scriptures = Finder.run(text)
        print(filename)
        print(scriptures)

