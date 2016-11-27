from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import random
from itertools import islice
import sys
from quadtree import quadNode, AABB

class RRT(object):
    def __init__(self, startX, startY, gridW, gridH):
        """Initialize the grid and first two points in the RRT"""
        self.coordsSet = set()  # hashtable of already added points (greatly improves runtime)

        self.width = gridW
        self.height = gridH

        # initialize quadtree to middle of space
        self.quadTree = quadNode((self.width / 2, self.height / 2), max(self.width, self.height) / 2)

        # add the start point and the first connecting endpoint to the tree
        currPoint = Endpoint(self.width / 2, self.height / 2, None)
        self.addPoint(currPoint)
        currPoint = Endpoint(random.randint(0, self.width), random.randint(0, self.height), startPoint)
        self.addPoint(currPoint)

    def addPoint(self, point):
        self.quadTree.addPoint(point)
        self.coordsSet.add(point)

    def sqDist(self, pointA, pointB):
        """returns squared distance between points. Allows comparison of dist for two
        points without needing to use sqrt to calculate the actual distance.
        """
        return (pointB.x - pointA.x) ** 2 + (pointB.y - pointA.y) ** 2

    def closestPoint(self, point):
        """calculate the closest point on the tree to the passed point and add a segment between
        the passed point and the calculated point. returns none if the point already exists in the tree
        """


class Endpoint(object):
    def __init__(self, x, y, prevPoint):
        self.coords = Point(x, y)
        self.prevPoint = prevPoint

    def splitCoords(self):
        return self.coords.x, self.coords.y


def drawPlot(rrt):
    """draw the RRT"""
    # initialize the matplotlib graph
    fig = plt.figure()
    rrt.ax = fig.add_subplot(111)
    rrt.ax.set_xlim(-1, rrt.width + 1)
    rrt.ax.set_ylim(-1, rrt.height + 1)

    for p in islice(rrt.pointList, 1, None):
        epA = p
        epB = epA.prevPoint
        line = LineString([epA.coords, epB.coords])

        x, y = line.xy
        rrt.ax.plot(x, y, color="blue")

    plt.show()


def drawPath(rrt, targetPoint):
    """draw the RRT with a path from the startPoint to the passed targetPoint"""

    # initialize the matplotlib graph
    fig = plt.figure()
    rrt.ax = fig.add_subplot(111)
    rrt.ax.set_xlim(-1, rrt.width + 1)
    rrt.ax.set_ylim(-1, rrt.height + 1)

    tempPoint = rrt.pointList[-1]
    plottedPoints = []
    # start at targetPoint and work backwards until starting point found.
    while tempPoint.prevPoint != None:
        plottedPoints.append(tempPoint)
        epA = tempPoint
        epB = epA.prevPoint
        line = LineString([epA.coords, epB.coords])

        # draw each line in red
        x, y = line.xy
        rrt.ax.plot(x, y, color="red")

        tempPoint = tempPoint.prevPoint

    for p in islice(rrt.pointList, 1, None):
        if p not in plottedPoints:
            epA = p
            epB = epA.prevPoint
            line = LineString([epA.coords, epB.coords])

            x, y = line.xy
            rrt.ax.plot(x, y, color="blue")

    plt.show()


def main():
    random.seed()
    count = 0
    numSteps = int(sys.argv[1])  # BAD, ASSUMES VALUE PASSED
    width = 100
    height = 100
    rrt = RRT(50, 50, width, height)



if __name__ == "__main__":
    main()