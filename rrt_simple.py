#!/usr/bin/env python

# Connor Pacala
# 10/2016
#
# rrt_simple.py
# Creates a simple rapidly exploring random tree.
# Only finds

import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import cProfile


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Obstacle(object):
    def __init__(self, left, right, bottom, top):
        """initialize rectangle obstacle with 2 points"""
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        
    def is_collision(self, point):
        """returns true if a point is within the rectangular object's bounding box"""
        return self.left < point.x < self.right and self.bottom < point.y < self.top


def sq_dist(point_a, point_b):
    """returns squared distance between points. Allows comparison of dist for two
    points without needing to use sqrt to calculate the actual distance.
    """
    return (point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2


def main():
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    # add obstacles to avoid
    obstacles = []
    #obstacles.append(Obstacle(50, 90, 20, 60))
    #obstacles.append(Obstacle(10, 50, 70, 100))
    #obstacles.append(Obstacle(120, 130, 50, 100))
    
    # draw obstacles
    for o in obstacles:
        plt.gca().add_patch(Rectangle((o.left, o.bottom), o.right - o.left, o.top - o.bottom, facecolor="red"))
    
    num_steps = 5000  # number of points to add to the tree
    width = 800       # width of the tree
    height = 600      # height of the tree
    start_point = Point(100, 50)
    points = np.zeros((num_steps,), dtype=np.object)
    points[0] = start_point
    count = 1
    
    # loop until num_steps points added to tree (or tree is filled)
    while count < num_steps and count < width * height:
        new_point = Point(random.randint(0, width), random.randint(0, height))
        collision = False
        
        # reject point if point is inside obstacle
        for o in obstacles:
            collision = o.is_collision(new_point)
            if collision:
                break
        
        # if point not inside obstacle, find closest endpoint in tree to new point
        if not collision:
            dist = sq_dist(new_point, start_point)
            closest = start_point
            found = True
            
            for i in range(count + 1):
                if not points[i]:   # all stored points checked
                    break
                new_dist = sq_dist(new_point, points[i])
                if new_dist == 0:  # point already stored, ignore
                    found = False
                    break
                if new_dist < dist:  # find shortest distance between two points
                    dist = new_dist
                    closest = points[i]
            
            # draw line segments
            #line = plt.Line2D((new_point.x, closest.x), (new_point.y, closest.y))
            #plt.gca().add_line(line)
            
            # add new point to list
            if found:
                points[count] = new_point
                count += 1
        
    #ax.set_xlim(-1, width + 1)
    #ax.set_ylim(-1, height + 1)

    #plt.show()

if __name__ == "__main__":
    cProfile.run('main()')
