from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import random
from itertools import islice
import sys
from quadtree import quadNode, AABB
import math

class RRT(object):
    def __init__(self, startX, startY, gridW, gridH):
        """Initialize the grid and first two points in the RRT"""
        self.coordsSet = set()  # hashtable of already added points (greatly improves runtime)

        self.width = gridW
        self.height = gridH

        # initialize quadtree to middle of space
        self.quadTree = quadNode((self.width / 2, self.height / 2), max(self.width, self.height) / 2)

        # add the start point and the first connecting endpoint to the tree
        startPoint = Endpoint(self.width / 2, self.height / 2, None)
        self.addPoint(startPoint)
        currPoint = Endpoint(random.randint(0, self.width), random.randint(0, self.height), startPoint)
        self.addPoint(currPoint)

    def addPoint(self, point):
        self.quadTree.addPoint(point)
        self.coordsSet.add(point)

    def sqDist(self, pointA, pointB):
        """returns squared distance between points. Allows comparison of dist for two
        points without needing to use sqrt to calculate the actual distance.
        """
        return (pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2

    def closestPoint(self, point):
        """calculate the closest point on the tree to the passed point and add a segment between
        the passed point and the calculated point. returns none if the point already exists in the tree
        """
        if point in self.coordsSet:
            return None

        # find the node the point belongs to
        currNode = self.quadTree.getPointNode(point)
        if not currNode:
            return None

        closestPoint = None
        # search current node for points
        if len(currNode.pointList) > 0:
            closestPoint = currNode.pointList[0]
        else:  # search sibling nodes for points
            parentNode = currNode.parent
            if currNode is not parentNode.topLeft and len(parentNode.topLeft.pointList) > 0:
                closestPoint = parentNode.topLeft.pointList[0]
            elif currNode is not parentNode.topRight and len(parentNode.topRight.pointList) > 0:
                closestPoint = parentNode.topRight.pointList[0]
            elif currNode is not parentNode.bottomLeft and len(parentNode.bottomLeft.pointList) > 0:
                closestPoint = parentNode.bottomLeft.pointList[0]
            elif currNode is not parentNode.bottomRight and len(parentNode.bottomRight.pointList) > 0:
                closestPoint = parentNode.bottomRight.pointList[0]

        if closestPoint is None:
            return None

        minDist = self.sqDist(closestPoint.coords, point)
        bbSize = math.sqrt(minDist)  # calculate actual distance for AABB creation
        searchAABB = AABB(point, bbSize)  # create bounding box centered on point with dimensions bbSize * 2

        points = self.quadTree.getPointsAABB(searchAABB)  # find all points in tree that are within bounding box

        if points:
            # find the closest point to the target point
            for p in islice(points, 0, None):
                tempDist = self.sqDist(p.coords, point)
                if tempDist < minDist:
                    minDist = tempDist
                    closestPoint = p

        newPoint = Endpoint(point[0], point[1], closestPoint)
        self.addPoint(newPoint)
        return newPoint

class Endpoint(object):
    def __init__(self, x, y, prevPoint):
        self.coords = (x, y)
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
        line = LineString([Point(epA.coords), Point(epB.coords)])

        x, y = line.xy
        rrt.ax.plot(x, y, color="blue")

    plt.show()


def drawPath(rrt, targetPoint):
    """draw the RRT with a path from the startPoint to the passed targetPoint"""
    searchArea = AABB((rrt.width / 2, rrt.height / 2), max(rrt.width, rrt.height) / 2)
    pointList = rrt.quadTree.getPointsAABB(searchArea)  # get all points in quadtree

    # initialize the matplotlib graph
    plt.ion()
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-1, rrt.width + 1)
    ax.set_ylim(-1, rrt.height + 1)

    tempPoint = pointList[-1]
    plottedPoints = []
    # start at targetPoint and work backwards until starting point found.
    while tempPoint.prevPoint != None:
        plottedPoints.append(tempPoint)
        epA = tempPoint
        epB = epA.prevPoint
        line = LineString([Point(epA.coords), Point(epB.coords)])

        # draw each line in red
        x, y = line.xy
        rrt.ax.plot(x, y, color="red")

        tempPoint = tempPoint.prevPoint

    for p in islice(pointList, None):
        if p not in plottedPoints and p.prevPoint is not None:
            epA = p
            epB = epA.prevPoint
            line = LineString([Point(epA.coords), Point(epB.coords)])

            x, y = line.xy
            rrt.ax.plot(x, y, color="blue")

    plt.show()


def main():
    random.seed()
    numSteps = int(sys.argv[1])  # BAD, ASSUMES VALUE PASSED
    width = 100
    height = 100

    # initialize the matplotlib graph
    plt.ion()
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-1, width + 1)
    ax.set_ylim(-1, height + 1)

    #searchArea = AABB((rrt.width / 2, rrt.height / 2), max(rrt.width, rrt.height) / 2)
    #pointList = rrt.quadTree.getPointsAABB(searchArea)  # get all points in quadtree




    rrt = RRT(50, 50, width, height)

    for p in islice(rrt.quadTree.pointList, None):
        if p.prevPoint is not None:
            epA = p
            epB = epA.prevPoint
            line = LineString([Point(epA.coords), Point(epB.coords)])

            x, y = line.xy
            ax.plot(x, y, color="blue")
            plt.pause(0.001)


    count = 2
    newPoint = (random.randint(0, width), random.randint(0, height))
    targetPoint = Endpoint(80, 40, None)

    while count < numSteps:
        # while newPoint.splitCoords() != targetPoint.splitCoords():
        tempPoint = rrt.closestPoint(newPoint)
        if tempPoint:
            count += 1
            line = LineString([Point(tempPoint.coords), Point(tempPoint.prevPoint.coords)])
            x, y = line.xy
            ax.plot(x, y, color="blue")
            plt.pause(0.001)
        newPoint = (random.randint(0, width), random.randint(0, height))

    #drawPath(rrt, targetPoint)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()