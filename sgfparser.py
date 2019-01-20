#!/usr/bin/env python3

import sgf
import matplotlib.pyplot as pyplot

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

winrates = []

with open("/home/fan/GoProjects/gtp/20190120200851W=B.sgf") as f:
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

#
x = range(1, len(winrates)+1)
pyplot.plot(x, ii , 's-', color='r')
pyplot.show()


