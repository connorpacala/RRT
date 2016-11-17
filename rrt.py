from shapely.geometry import Point, LineString
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
#import numpy as np

class Endpoint(object):
    def __init__(self, x, y, prevPoint = None):
        self.x, self.y = x, y
        self.prevPoint = prevPoint

def sqDist(pointA, pointB):
    """returns squared distance between points. Allows comparison of dist for two
    points without needing to use sqrt to calculate the actual distance.
    """
    return (pointB.x - pointA.x)**2 + (pointB.y - pointA.y)**2

def main():
    random.seed(900)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    width = 800
    height = 600
    startPoint = Endpoint(width / 2, height / 2)
    numSteps = 500 #number of points to add to the tree
    points = [] #np.zeros((numSteps,), dtype=np.object)
    points.append(startPoint)
    newPoint = Endpoint(random.randint(0, width), random.randint(0, height), startPoint)
    points.append(newPoint)
    count = 2 #number of points added to tree (1 as we added a start point)
    
    
    
    while count < numSteps:
        newPoint = Endpoint(random.randint(0, width), random.randint(0, height))
        intersect = None
        
        collision = False
        #for o in obstacles:
        #    collision = o.isCollision(newPoint)
        #    if collision:
        #        break
        if not collision:
            dist = sqDist(newPoint, startPoint)
            closest = startPoint
            closeIntersect = startPoint
            found = True
            
            for p in points:
                epA = p
                
                if epA == points[0]:
                    continue
                
                #point already in tree, calculate new point
                if epA.x == newPoint.x and epA.y == newPoint.y:
                    found = False
                    break

                epB = epA.prevPoint
                #print epA.x, epA.y, epB.x, epB.y
                line = LineString([(epA.x, epA.y), (epB.x, epB.y)])
                
                #calculate closest point on any line segment to new point
                tempPoint = line.interpolate(line.project(Point(newPoint.x, newPoint.y)))
                intersect = Endpoint(tempPoint.x, tempPoint.y)
                newDist = sqDist(intersect, newPoint)
                if newDist < dist: #find shortest distance between two points
                    dist = newDist
                    closest = p
                    closeIntersect = intersect
                    
            
            #line = plt.Line2D((newPoint.x, closest.x), (newPoint.y, closest.y))
            #plt.gca().add_line(line)
            
            if found:
                if round(closeIntersect.x) == closest.x and round(closeIntersect.y) == closest.y:
                    points.append(Endpoint(newPoint.x, newPoint.y, closest))
                elif round(closeIntersect.x) == closest.prevPoint.x and round(closeIntersect.y) == closest.prevPoint.y:
                    points.append(Endpoint(newPoint.x, newPoint.y, closest.prevPoint))
                else:
                    closeIntersect.prevPoint = closest.prevPoint
                    closest.prevPoint = closeIntersect
                    points.append(closeIntersect)
                    points.append(Endpoint(newPoint.x, newPoint.y, closeIntersect))
                    count += 1
        
   
    for i in range(1, count):
        epA = points[i]
        epB = epA.prevPoint
        line = LineString([(epA.x, epA.y), (epB.x, epB.y)])
    
        x, y = line.xy
        ax.plot(x, y) 
    
    ax.set_xlim(-1, width + 1)
    ax.set_ylim(-1, height + 1)

    plt.show()
    

        
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class RRT(object):
    def __init__(self, width, height, maxPoints, startPoint):
        self.width, self.height = width, height
        self.maxPoints = maxPoints
        self.pointList = []
        x, y = startPoint.getCoords()
        self.pointList.append(startPoint)
        
        
    def pointInGrid(self, point):
        """returns true if the point is within the width, height values of the RRT"""
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        return False
        
    
    def addPoint(self, point):
        endA, endB = nearestSegment(point)
        
        
    def nearestSegment(self, point):
        """finds the nearest line segment to the passed point"""
        #if no points to compare to, return false to indicate error
        if len(self.pointList) < 2:
            return None, None