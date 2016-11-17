from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import random
from itertools import islice
import time
import sys
import math
from sets import Set

class RRT(object):
    def __init__(self, startX, startY):
        """Initialize the grid and first two points in the RRT"""
        width = 100
        height = 100
        self.pointList = []
        self.coordsSet = Set() #hashtable of already added points (greatly improves runtime)
        
        #initialize the matplotlib graph
        fig = plt.figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(-1, width + 1)
        self.ax.set_ylim(-1, height + 1)
        
        #add the start point and the first connecting endpoint to the tree
        startPoint = Endpoint(width / 2, height / 2, None)
        self.pointList.append(startPoint)
        self.coordsSet.add((startPoint.splitCoords()))
        newPoint = Endpoint(random.randint(0, width), random.randint(0, height), startPoint)
        self.pointList.append(newPoint)
        self.coordsSet.add((newPoint.splitCoords()))
        
        
    def sqDist(self, pointA, pointB):
        """returns squared distance between points. Allows comparison of dist for two
        points without needing to use sqrt to calculate the actual distance.
        """
        return (pointB.x - pointA.x)**2 + (pointB.y - pointA.y)**2
        
    def closestPoint(self, point):
        """calculate the closest point on the tree to the passed point and add a segment between
        the passed point and the calculated point. returns none if the point already exists in the tree
        """
        if (point.splitCoords()) in self.coordsSet:
            return None
        dist = self.sqDist(self.pointList[0].coords, point.coords)
        closestEnd = self.pointList[0]
        intersect = None
        for p in islice(self.pointList, 1, None): #ignore first point as it has no prevPoint
            #find the closest point on the line to the passed point
            line = LineString([p.coords, p.prevPoint.coords])
            tempPoint = line.interpolate(line.project(point.coords))
            tempDist = self.sqDist(tempPoint, point.coords)
            if tempDist < dist:
                dist = tempDist
                closestEnd = p
                intersect = tempPoint
        
        #if point found, add the new point to the list and update prevPoints of endpoints
        if intersect:
            newIntersect = Endpoint(intersect.x, intersect.y, closestEnd.prevPoint)
            self.pointList.append(newIntersect)
            self.coordsSet.add(newIntersect.splitCoords())
            closestEnd.prevPoint = newIntersect
            point.prevPoint = newIntersect
            self.pointList.append(point)
            self.coordsSet.add(point.splitCoords())
        else:
            point.prevPoint = self.pointList[0]
            self.pointList.append(point)
            self.coordsSet.add(point.splitCoords())
                
        return True

    def drawPlot(self):
        """draw the RRT"""
        for p in islice(self.pointList, 1, None):
            epA = p
            epB = epA.prevPoint
            line = LineString([epA.coords, epB.coords])
        
            x, y = line.xy
            self.ax.plot(x, y, color="blue") 
    
        plt.show()
        
    def drawPath(self, targetPoint):
        """draw the RRT with a path from the startPoint to the passed targetPoint"""
        tempPoint = self.pointList[-1]
        plottedPoints = []
        #start at targetPoint and work backwards until starting point found.
        while tempPoint.prevPoint != None:
            plottedPoints.append(tempPoint)
            epA = tempPoint
            epB = epA.prevPoint
            line = LineString([epA.coords, epB.coords])
        
            #draw each line in red
            x, y = line.xy
            self.ax.plot(x, y, color="red") 
        
            tempPoint = tempPoint.prevPoint
            
        for p in islice(self.pointList, 1, None):
            if p not in plottedPoints:
                epA = p
                epB = epA.prevPoint
                line = LineString([epA.coords, epB.coords])
            
                x, y = line.xy
                self.ax.plot(x, y, color="blue") 
    
        plt.show()
        
    
class Endpoint(object):
    def __init__(self, x, y, prevPoint):
        self.coords = Point(x, y)
        self.prevPoint = prevPoint
        
    def splitCoords(self):
        return self.coords.x, self.coords.y


def main():
    random.seed()
    rrt = RRT(50, 50)
    count = 0
    numSteps = int(sys.argv[1]) #BAD, ASSUMES VALUE PASSED
    width = 100
    height = 100
    targetPoint = Endpoint(80, 40, None)
    """
    startPoint = Endpoint(width / 2, height / 2, None)
    rrt.pointList.append(startPoint)
    rrt.coordsSet.add((startPoint.splitCoords()))
    count += 1
    newPoint = Endpoint(random.randint(0, width), random.randint(0, height), startPoint)
    rrt.pointList.append(newPoint)
    rrt.coordsSet.add((newPoint.splitCoords()))
    count += 1
    """
    count = 2
    newPoint = Endpoint(random.randint(0, width), random.randint(0, height), None)
    while count < numSteps:
    #while newPoint.splitCoords() != targetPoint.splitCoords():
        if rrt.closestPoint(newPoint):
            count += 1
        newPoint = Endpoint(random.randint(0, width), random.randint(0, height), None)
            
    rrt.drawPath(targetPoint)
    
    
if __name__ == "__main__":
    main()