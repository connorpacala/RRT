from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import random
from itertools import islice
import sys
from quadtree import QuadNode, AABB
import math
import time
import cProfile


def sq_dist(point_a, point_b):
    """returns squared distance between points. Allows comparison of dist for two
    points without needing to use sqrt to calculate the actual distance.
    """
    return (point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2


class RRT(object):
    def __init__(self, start_x, start_y, grid_w, grid_h):
        """Initialize the grid and first two points in the RRT"""
        self.coordsSet = set()  # hashtable of already added points (greatly improves runtime)

        self.width = grid_w
        self.height = grid_h

        # initialize quadtree to middle of space
        self.quadTree = QuadNode((self.width / 2, self.height / 2), max(self.width, self.height) / 2)

        # add the start point and the first connecting endpoint to the tree
        start_point = Endpoint(self.width / 2, self.height / 2, None)
        self.add_point(start_point)
        curr_point = Endpoint(random.randint(0, self.width), random.randint(0, self.height), start_point)
        self.add_point(curr_point)

    def add_point(self, point):
        self.quadTree.add_point(point)
        self.coordsSet.add(point.coords)

    def closest_point(self, point):
        """calculate the closest point on the tree to the passed point and add a segment between
        the passed point and the calculated point. returns none if the point already exists in the tree
        """
        if point in self.coordsSet:
            return None

        # find the node the point belongs to
        curr_node = self.quadTree.get_point_node(point)
        if not curr_node:
            return None

        closest_point = None
        # search current node for points
        if len(curr_node.pointList) > 0:
            closest_point = curr_node.pointList[0]
        else:  # search sibling nodes for points
            parent_node = curr_node.parent
            if curr_node is not parent_node.topLeft and len(parent_node.topLeft.pointList) > 0:
                closest_point = parent_node.topLeft.pointList[0]
            elif curr_node is not parent_node.topRight and len(parent_node.topRight.pointList) > 0:
                closest_point = parent_node.topRight.pointList[0]
            elif curr_node is not parent_node.bottomLeft and len(parent_node.bottomLeft.pointList) > 0:
                closest_point = parent_node.bottomLeft.pointList[0]
            elif curr_node is not parent_node.bottomRight and len(parent_node.bottomRight.pointList) > 0:
                closest_point = parent_node.bottomRight.pointList[0]

        if closest_point is None:
            return None

        min_dist = sq_dist(closest_point.coords, point)
        bb_size = math.sqrt(min_dist)  # calculate actual distance for AABB creation
        search_aabb = AABB(point, bb_size)  # create bounding box centered on point with dimensions bb_size * 2

        points = self.quadTree.get_points_aabb(search_aabb)  # find all points in tree that are within bounding box

        if points:
            # find the closest point to the target point
            for p in islice(points, 0, None):
                temp_dist = sq_dist(p.coords, point)
                if temp_dist < min_dist:
                    min_dist = temp_dist
                    closest_point = p

        new_point = Endpoint(point[0], point[1], closest_point)
        self.add_point(new_point)
        return new_point


class Endpoint(object):
    def __init__(self, x, y, prev_point):
        self.coords = (x, y)
        self.prevPoint = prev_point

    def split_coords(self):
        return self.coords.x, self.coords.y


def draw_plot(rrt):
    """draw the RRT"""
    # initialize the matplotlib graph
    fig = plt.figure()
    rrt.ax = fig.add_subplot(111)
    rrt.ax.set_xlim(-1, rrt.width + 1)
    rrt.ax.set_ylim(-1, rrt.height + 1)

    for p in islice(rrt.pointList, 1, None):
        ep_a = p
        ep_b = ep_a.prevPoint
        line = LineString([Point(ep_a.coords), Point(ep_b.coords)])

        x, y = line.xy
        rrt.ax.plot(x, y, color="blue")

    plt.show()


def draw_path(rrt, target_point):
    """draw the RRT with a path from the startPoint to the passed target_point"""
    search_area = AABB((rrt.width / 2, rrt.height / 2), max(rrt.width, rrt.height) / 2)
    point_list = rrt.quadTree.get_points_aabb(search_area)  # get all points in quadtree

    # initialize the matplotlib graph
    plt.ion()
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-1, rrt.width + 1)
    ax.set_ylim(-1, rrt.height + 1)

    temp_point = point_list[-1]
    plotted_points = []
    # start at target_point and work backwards until starting point found.
    while temp_point.prevPoint is not None:
        plotted_points.append(temp_point)
        ep_a = temp_point
        ep_b = ep_a.prevPoint
        line = LineString([Point(ep_a.coords), Point(ep_b.coords)])

        # draw each line in red
        x, y = line.xy
        rrt.ax.plot(x, y, color="red")

        temp_point = temp_point.prevPoint

    for p in islice(point_list, None):
        if p not in plotted_points and p.prevPoint is not None:
            ep_a = p
            ep_b = ep_a.prevPoint
            line = LineString([Point(ep_a.coords), Point(ep_b.coords)])

            x, y = line.xy
            rrt.ax.plot(x, y, color="blue")

    plt.show()


def main():
    start = time.time()
    random.seed()
    num_steps = int(sys.argv[1])  # BAD, ASSUMES VALUE PASSED
    width = 400
    height = 400

    # initialize the matplotlib graph
    #plt.ion()
    #plt.show()
#
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_xlim(-1, width + 1)
    #ax.set_ylim(-1, height + 1)

    rrt = RRT(50, 50, width, height)

    #for p in islice(rrt.quadTree.pointList, None):
    #    if p.prevPoint is not None:
    #        epA = p
    #        epB = epA.prevPoint
    #        line = LineString([Point(epA.coords), Point(epB.coords)])
#
    #        x, y = line.xy
    #        ax.plot(x, y, color="blue")
    #        plt.pause(0.001)

    count = 2
    new_point = (random.randint(0, width), random.randint(0, height))
    target_point = Endpoint(80, 40, None)

    while count < num_steps:
        # while new_point.split_coords() != target_point.split_coords():
        temp_point = rrt.closest_point(new_point)
        if temp_point:
            count += 1
            #line = LineString([Point(temp_point.coords), Point(temp_point.prevPoint.coords)])
            #x, y = line.xy
            #ax.plot(x, y, color="blue")
            #plt.pause(0.001)
        new_point = (random.randint(0, width), random.randint(0, height))

    #draw_path(rrt, target_point)

    #plt.ioff()
    #plt.show()
    print time.time() - start

if __name__ == "__main__":
    cProfile.run('main()')