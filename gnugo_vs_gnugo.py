#!/usr/bin/env python

from subprocess import Popen, PIPE
import time
import datetime
from gtp import parse_vertex, gtp_move, gtp_color
from gtp import BLACK, WHITE, PASS


class GTPSubProcess(object):

    def __init__(self, label, args):
        self.label = label
        self.subprocess = Popen(args, stdin=PIPE, stdout=PIPE)
        time.sleep(8)
        print("===================FAN============={} subprocess created".format(label))

    def send(self, data):
        print("sending {}: {}".format(self.label, data))
        self.subprocess.stdin.write(data)
        result = ""
        while True:
            data = self.subprocess.stdout.readline()
            print("=====the data is {}======".format(data))
            if not data.strip():
                break
            result += data
        print("got: {}".format(result))
        return result

    def send1(self, data):
        print("sending {}: {}".format(self.label, data))
        self.subprocess.stdin.write(data)
        data = self.subprocess.stdout.readline()
        print("=====the data is {}======".format(data))
        return data

    def waitUntilEnd(self):
        while True:
            oneline = self.subprocess.stdout.readline()
            if not oneline.strip():
                break

    def close(self):
        print("quitting {} subprocess".format(self.label))
        self.subprocess.communicate("quit\n")


class GTPFacade(object):

    def __init__(self, label, args):
        self.label = label
        self.moves = []
        self.gtp_subprocess = GTPSubProcess(label, args)

    def name(self):
        self.gtp_subprocess.send("name\n")

    def version(self):
        self.gtp_subprocess.send("version\n")

    def boardsize(self, boardsize):
        self.gtp_subprocess.send("boardsize {}\n".format(boardsize))

    def komi(self, komi):
        self.gtp_subprocess.send("komi {}\n".format(komi))

    def clear_board(self):
        self.gtp_subprocess.send("clear_board\n")

    def genmove(self, color):
        self.gtp_subprocess.send(
            "genmove {}\n".format(gtp_color(color)))
        # while True:
        #     isRunning = self.gtp_subprocess.send("check_running\n")
        #     print("=====================The running result is {}===========".format(isRunning))
        #     if not isRunning:
        #         print("============get out!!!!================")
        #         break
        # message = self.gtp_subprocess.send("lastmove\n")

        # print("genmove result is {}".format(message))
        # assert message[0] == "="
        # return parse_vertex(message[1:].strip())

    def genmove1(self, color):
        self.gtp_subprocess.send1(
            "genmove {}\n".format(gtp_color(color)))
        # while True:
        #     isRunning = self.gtp_subprocess.send("check_running\n")
        #     print("=====================The running result is {}===========".format(isRunning))
        #     if not isRunning:
        #         print("============get out!!!!================")
        #         break
        # message = self.gtp_subprocess.send("lastmove\n")

        # print("genmove result is {}".format(message))
        # assert message[0] == "="
        # return parse_vertex(message[1:].strip())

    def checkRunning(self):
        isRunning = self.gtp_subprocess.send("check_running\n")
        return isRunning

    def getLastMove(self):
        lastMove = self.gtp_subprocess.send1("lastmove\n")
        return lastMove.strip()

    def printSgf(self):
        return self.gtp_subprocess.send("printsgf\n")

    def showboard(self):
        print("========================show board========================")
        self.gtp_subprocess.send("showboard\n")

    def play(self, color, vertex):
        self.gtp_subprocess.send("play {}\n".format(gtp_move(color, vertex)))

    def final_score(self):
        self.gtp_subprocess.send("final_score\n")

    def close(self):
        self.gtp_subprocess.close()

    def waitUntilEnd(self):
        self.gtp_subprocess.waitUntilEnd()

def saveSGF(str,winner):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    with open(timestamp+"W="+winner+".sgf", "w") as file:
        file.write(str)

RAYGO = ["/home/fan/GoProjects/Ray/ray", "--playout", "4000","--size","13"]
LEELAZ_NORMAL = ["/home/fan/GoProjects/leelaz13_normal/build/leelaz", "--gtp", "-w", "/home/fan/GoProjects/13x13.txt","-p","1600", "--noponder"]
LEELAZ_tekake = ["/home/fan/GoProjects/leelaz13/build/leelaz13_c_param25_cp_10", "--gtp", "-w", "/home/fan/GoProjects/13x13.txt","-p","1600","--noponder"]
GNUGO_MONTE_CARLO = ["gnugo", "--mode", "gtp", "--monte-carlo"]
LEELAZ = ["/home/fan/GoProjects/leelaz13/build/leelaz", "--gtp", "-w", "/home/fan/GoProjects/13x13.txt","-p","1600","--noponder"]

#
# black = GTPFacade("black", LEELAZ_tekake)
# # white = GTPFacade("white", GNUGO_LEVEL_ONE)
# white = GTPFacade("white", RAYGO)

# make sure black is ready
# black.waitUntilEnd()

# print("=======black is ready!!!==============")


white = GTPFacade("white", LEELAZ)
# white = GTPFacade("white", GNUGO_LEVEL_ONE)
black = GTPFacade("black", RAYGO)

firstPass = False
whiteLastMove = ""

while True:
    black.genmove1(BLACK)
    time.sleep(5)

    lastBlackMove = black.getLastMove()

    if "resign" in lastBlackMove or "pass" in lastBlackMove or "illegal" in lastBlackMove:
        saveSGF(white.printSgf(), "W")
        break

    # if lastBlackMove == "pass":
    #     if not firstPass:
    #         firstPass = True
    #     else:
    #         saveSGF(black.printSgf())
    #         break

    white.play(BLACK, lastBlackMove)
    # white.showboard()
    white.genmove(WHITE)
    # time.sleep(5)

    lastWhiteMove = white.getLastMove()

    if lastWhiteMove == whiteLastMove:
        saveSGF(white.printSgf(), "B")
        break

    if lastWhiteMove == "" or "resign" in lastWhiteMove or "pass" in lastWhiteMove or "illegal" in lastWhiteMove:
        saveSGF(white.printSgf(), "B")
        break

    # if lastWhiteMove == "pass":
    #     if not firstPass:
    #         firstPass = True
    #     else:
    #         saveSGF(black.printSgf())
    #         break
    black.play(WHITE, lastWhiteMove)
    whiteLastMove = lastWhiteMove
    black.showboard()

    # time.sleep(3)
#
#
#
# white.waitUntilEnd()

# print("=======white is ready!!!==============")


# black.name()
# black.version()
#
# white.name()
# white.version()
#
# black.boardsize(9)
# white.boardsize(9)
#
# black.komi(5.5)
# white.komi(5.5)
#
# black.clear_board()
# white.clear_board()
#
# first_pass = False
#

# black.showboard()
#
# while True:
#     vertex = black.genmove(BLACK)
#
#     if vertex == PASS:
#         if first_pass:
#             break
#         else:
#             first_pass = True
#     else:
#         first_pass = False
#
#     black.showboard()
#
#
#     white.play(BLACK, vertex)
#     white.showboard()
#
#     vertex = white.genmove(WHITE)
#     if vertex == PASS:
#         if first_pass:
#             break
#         else:
#             first_pass = True
#     else:
#         first_pass = False
#
#     white.showboard()
#
#     black.play(WHITE, vertex)
#     black.showboard()
#
# black.final_score()
# white.final_score()
#
# black.close()
# white.close()
