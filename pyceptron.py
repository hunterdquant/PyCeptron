import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from numpy import linalg as lin

import random
import sys

class SamplePoint:
    def __init__(self, point, label):
        self.x = np.array(point)
        self.y = label

    def tounit(self):
        self.x = np.multiply(self.x, 1/lin.norm(self.x))

def getweights(sample):
    astar = np.zeros(len(sample[0].x))
    point = exists(sample, astar)
    while point != None:
        tmp = SamplePoint(point.x, point.y)
        tmp.tounit()
        astar = np.add(astar, np.multiply(tmp.y, tmp.x))
        point = exists(sample, astar)

    return astar

def exists(sample, astar):
    for point in sample:
        coord = point.x
        label = point.y
        if sign(np.inner(astar, coord)) != label:
            return point
    return None

def classify(weights, point):
    return sign(np.inner(weights, point))

def sign(val):
    return 1 if val >= 0 else -1

def samplegen(num):
    points = []
    sep = np.random.rand(1, 2)
    for i in range(num):
        xp, yp = [random.uniform(-1, 1) for i in range(2)]
        vec = np.array([xp, yp])
        label = sign(sep.dot(vec))
        point = SamplePoint([xp, yp, 1], label)
        points.append(point)
    return points

sample = []

def readPoints(fname):
    fin = open(fname, 'r')
    for line in fin:
        row = line.split(',')
        point = []
        for i in range(0, len(row)-1):
            point.append(float(row[i].strip()))
        point.append(1)
        label = int(row[len(row)-1])
        sp = SamplePoint(point, label)
        sample.append(sp)

def main():
    global sample
    if (len(sys.argv) == 3):
        if (sys.argv[1] == '-nd'):
            readPoints(sys.argv[2])
            print getweights(sample)
            return
        elif (sys.argv[1] == '-d'):
            readPoints(sys.argv[2])
    elif (len(sys.argv) == 2):
        readPoints(sys.argv[1])

    fig = plt.figure(figsize=(5, 5))
    fig.canvas.mpl_connect('button_release_event', onclick)
    plt.interactive = True
    update()

def update():
    global sample
    plt.clf()
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    if len(sample) >= 2:
        weight = getweights(sample)
        if weight[1] != 1:
            yInt1 = (-(weight[0]*-1.5) - weight[2])/weight[1]
            yInt2 = (-(weight[0]*1.5) - weight[2])/weight[1]
            ax = plt.gca()
            ax.add_line(lines.Line2D([-1.5, 1.5], [yInt1, yInt2]))

    for s in sample:

        plt.plot(s.x[0], s.x[1], 'bo' if s.y == 1 else 'ro')
    plt.draw()
    plt.show()

def onclick(event):
    global sample
    if event.button == 1:
        sample.append(SamplePoint([event.xdata, event.ydata, 1], 1))
    elif event.button == 3:
        sample.append(SamplePoint([event.xdata, event.ydata, 1], -1))
    update()

if __name__ == "__main__":
    main()

