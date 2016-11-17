#!/usr/bin/env python

# Connor Pacala
# 10/2016
#
# rrtSimple.py
# Creates a simple rapidly exploring random tree.
# Only finds

import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Obstacle(object):
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        
    def isCollision(self, point):
        """returns true if a point is within the rectangular object's bounding box"""
        return point.x > self.left and point.x < self.right and point.y > self.bottom and point.y < self.top
        
def sqDist(pointA, pointB):
    """returns squared distance between points. Allows comparison of dist for two
    points without needing to use sqrt to calculate the actual distance.
    """
    return (pointB.x - pointA.x)**2 + (pointB.y - pointA.y)**2


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #add obstacles to avoid
    obstacles = []
    #obstacles.append(Obstacle(50, 90, 20, 60))
    #obstacles.append(Obstacle(10, 50, 70, 100))
    #obstacles.append(Obstacle(120, 130, 50, 100))
    
    for o in obstacles:
        plt.gca().add_patch(Rectangle((o.left, o.bottom), o.right - o.left, o.top - o.bottom, facecolor="red"))
    
    numSteps = 10000 #number of points to add to the tree
    width = 800 #width of the tree
    height = 600 #height of the tree
    startPoint = Point(100, 50)
    points = np.zeros((numSteps,), dtype=np.object)
    points[0] = startPoint
    count = 1
    
    while count < numSteps:
        newPoint = Point(random.randint(0, width), random.randint(0, height))
        collision = False
        for o in obstacles:
            collision = o.isCollision(newPoint)
            if collision:
                break
        if not collision:
            dist = sqDist(newPoint, startPoint)
            closest = startPoint
            found = True
            
            for i in range(count + 1):
                if not points[i]:   #all stored points checked
                    break
                newDist = sqDist(newPoint, points[i])
                if newDist == 0: #point already stored, ignore
                    found = False
                    break
                if newDist < dist: #find shortest distance between two points
                    dist = newDist
                    closest = points[i]
            
            line = plt.Line2D((newPoint.x, closest.x), (newPoint.y, closest.y))
            plt.gca().add_line(line)
            
            if found:
                points[count] = newPoint
                count += 1
        
    ax.set_xlim(-1, width + 1)
    ax.set_ylim(-1, height + 1)

    plt.show()

if __name__ == "__main__":
    main()