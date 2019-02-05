#!/usr/bin/env python3
import sgf
import matplotlib.pyplot as pyplot
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def parseWinrate(filePath):
    winrates = []
    with open(filePath) as f:
        collection = sgf.parse(f.read())
        children = collection.children
        gameTree = children[0]
        for node in gameTree.nodes:
            for property in node.properties:
                if property == 'C':
                    comments = node.properties[property]
                    _comments = ''.join(comments)
                    if _comments.strip() != '':
                        winrate = _comments.split('::')[0]
                        winrates.append(winrate)
        f.close()
    ii = []
    winrates.pop(0)
    for _ in winrates:
        ff = float(_)
        ii.append(ff)
    return ii

# FATHER_FILE = '/home/fan/GoProjects/gtp/ex1/'

# names = [FATHER_FILE + name for name in os.listdir(FATHER_FILE)
#         if os.path.isfile(os.path.join(FATHER_FILE, name)) and 'W=B' in name]

# print('B' in '/home/fan/GoProjects/gtp/ex1/20190124215804W=B.sgf')

# totalWinrates = []

# totalLength = 0

# maxLength = 0

# for name in names:
#     wr = parseWinrate(name)
#     totalWinrates.append(wr)
#     if len(wr)>maxLength:
#         maxLength = len(wr)

averageWR = parseWinrate('/home/fan/GoProjects/gtp/livsleela.sgf')

# print(totalWinrates)    

# averageWR = []

# for index in range(0,maxLength):
#     somelength = 0
#     averageOne = 0
#     for winrate in totalWinrates:
#         if len(winrate)>index:
#             averageOne+=winrate[index]
#             somelength+=1
#     av = averageOne/somelength
#     averageWR.append(av)

# print(averageWR)            

# print('the average length of match is:'+ str(totalLength/len(names)))    

#
x = range(1, len(averageWR)+1)
pyplot.plot(x, averageWR , 's-', color='g')
pyplot.show()


