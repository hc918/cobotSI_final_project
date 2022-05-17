from simctl import *
from time import *
from threading import *

sim = env()
sim.finish()
lock = Lock()
robot = False


class Robot:
    ready = None

    def __init__(self):
        lock.acquire()
        self.ready = sim.getintegersignal("RobotReady")
        lock.release()

    def getReadyInfo(self):
        lock.acquire()
        self.ready = sim.getintegersignal("RobotReady")
        lock.release()
        return self.ready


class Fryer:
    doneGram = 0
    doneCount = []

    ready = []
    timer = []
    fryingTime = []
    menu = []
    temp = []

    def __init__(self, fryerNum=1, potNum=1):
        self.fryerNum = fryerNum
        self.potNum = potNum
        if robot:
            for i in range(self.fryerNum):
                self.ready.append([])
                self.timer.append([])
                self.fryingTime.append([])
                self.temp.append([])
                for j in range(self.potNum):
                    self.ready[i].append(0)
                    self.timer[i].append(-1)
                    self.fryingTime[i].append(0)
                    self.menu.append(0)
                    self.temp[i].append(0)
        else:
            for i in range(self.fryerNum):
                self.ready.append([])
                self.timer.append([])
                self.fryingTime.append([])
                for j in range(self.potNum):
                    self.ready[i].append(2)
                    self.timer[i].append(-1)
                    self.fryingTime[i].append(0)
                    self.menu.append(0)

        for i in range(3):
            self.doneCount.append(0)

    def setMenu(self, num, menu):
        if robot:
            pass
        else:
            for i in range(num):
                lock.acquire()
                if sim.getintegersignal("menu") == 0:
                    sim.setintegersignal("menu", menu)
                else:
                    i -= 1
                lock.release()

    def startFrying(self, i, j):
        if robot:
            self.ready[i][j] = 3
        else:
            pass

    def endFrying(self, i, j):
        if robot:
            self.ready[i][j] = -1
        else:
            pass

    def getReadyInfo(self, i, j):
        if robot:
            self.ready[i][j] = 2
        else:
            lock.acquire()
            self.ready[i][j] = sim.getintegersignal(f"pot{j + 1}")
            lock.release()

    def setTimer(self, i, j, value):
        if robot:
            self.fryingTime[i][j] = value
            self.temp[i][j] = time()
        else:
            pass

    def getTimerInfo(self, num1, num2):
        if robot:
            self.timer[num1][num2] = self.fryingTime[num1][num2] - (time() - self.temp[num1][num2])
        else:
            lock.acquire()
            self.timer[num1][num2] = sim.getfloatsignal(f"timer{num2 + 1}")
            self.fryingTime[num1][num2] = sim.getfloatsignal(f"time{num2 + 1}")
            lock.release()

    def getDoneGram(self):
        if robot:
            pass
        else:
            lock.acquire()
            self.doneGram = sim.getintegersignal("count")
            lock.release()
        return self.doneGram

    def get_count(self, num):
        self.doneCount[num - 1] += 1


