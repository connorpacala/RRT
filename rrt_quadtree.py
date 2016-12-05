from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import random
from itertools import islice
import sys
from quadtree import QuadNode, AABB
import math
import time
import cProfile

fig = plt.figure()
ax = fig.add_subplot(111)


def sq_dist(point_a, point_b):
    """returns squared distance between points. Allows comparison of dist for two
    points without needing to use sqrt to calculate the actual distance.
    """
    return (point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2


class RRT(object):
    def __init__(self, start_x, start_y, grid_w, grid_h, max_dist):
        """Initialize the grid and first two points in the RRT"""
        self.coords_set = set()  # hashtable of already added points (greatly improves runtime)

        self.max_dist = max_dist  # maximum distance between points. smaller = more memory but faster runtime

        self.width = grid_w
        self.height = grid_h

        # initialize quadtree to middle of space
        self.quad_tree = QuadNode((self.width / 2, self.height / 2), max(self.width, self.height) / 2)

        # add the start point and the first connecting endpoint to the tree
        start_point = Endpoint(self.width / 2, self.height / 2, None)
        self.add_point(start_point)
        curr_point = Endpoint(random.random() * self.width, random.random() * self.height, start_point)
        self.add_line(curr_point)

    def add_point(self, point):
        """Add points to quadtree and hashtable"""
        self.quad_tree.add_point(point)
        self.coords_set.add(point.coords)

    def add_line(self, point):
        """split line between point and point.prevPoint into segments of max_dist length and add them to the tree"""
        #BAD, MIXING IN ANIMATION CODE TO GET ANIMATING IN REAL TIME
        line = LineString([Point(point.coords), Point(point.prevPoint.coords)])
        x, y = line.xy
        ax.plot(x, y, color="blue")

        # add the start and endpoints to the tree before adding midpoints
        self.add_point(point)
        self.add_point(point.prevPoint)

        # get number of segments to split line into
        curr_point = point
        prev_point = point.prevPoint
        line = LineString([Point(curr_point.coords), Point(prev_point.coords)])
        num_segments = int(math.ceil(math.sqrt(sq_dist(curr_point.coords, prev_point.coords)) / self.max_dist))

        # use interpolate to find points max_dist along line
        for i in range(1, num_segments):
            s_point = line.interpolate(i * self.max_dist)
            new_point = Endpoint(s_point.x, s_point.y, prev_point)
            curr_point.prevPoint = new_point
            curr_point = new_point
            self.add_point(new_point)

    def closest_point(self, point):
        """calculate the closest point on the tree to the passed point and add a segment between
        the passed point and the calculated point. returns none if the point already exists in the tree
        """
        if point in self.coords_set:
            return None

        # find the node the point belongs to
        curr_node = self.quad_tree.get_point_node(point)
        if curr_node is None:
            return None

        closest_point = None
        # search current node for points
        if len(curr_node.pointList) > 0:
            for p in curr_node.pointList:
                # only use points that are not start point (causes bug when creating line as prevPoint is None)
                if p.prevPoint is not None:
                    closest_point = p
                    break
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

        if closest_point is None:  # something went wrong, there should be a point in the node or its siblings
            return None

        # find the closest point on the line to the passed point
        line = LineString([Point(closest_point.coords), Point(closest_point.prevPoint.coords)])
        temp_point = line.interpolate(line.project(Point(point)))
        closest_coords = (temp_point.x, temp_point.y)

        min_dist = sq_dist(closest_coords, point)

        # calculate bb_size to guarantee finding closest line segment based on max_dist between points
        bb_size = math.sqrt(self.max_dist ** 2 + min_dist ** 2)
        search_aabb = AABB(point, bb_size)  # create bounding box centered on point with dimensions bb_size * 2
        points = self.quad_tree.get_points_aabb(search_aabb)  # find all points in tree that are within bounding box

        if points:
            # find the closest point to the target point
            for p in islice(points, 0, None):
                if p.prevPoint is not None:  # ignore start point
                    line = LineString([Point(p.coords), Point(p.prevPoint.coords)])
                    temp_point = line.interpolate(line.project(Point(point)))
                    temp_dist = sq_dist((temp_point.x, temp_point.y), point)

                    if temp_dist < min_dist:
                        min_dist = temp_dist
                        closest_coords = (temp_point.x, temp_point.y)
                        closest_point = p
        else:
            return None

        if closest_coords not in self.coords_set:  # if interpolated point is not an endpoint, add new orthogonal line
            new_end = Endpoint(closest_coords[0], closest_coords[1], closest_point.prevPoint)
            closest_point.prevPoint = new_end
            new_point = Endpoint(point[0], point[1], new_end)
            self.add_line(new_point)
            return new_point
        else:  # interpolated point is endpoint, connect to existing endpoint
            new_point = Endpoint(point[0], point[1], closest_point)
            self.add_line(new_point)
            return new_point


class Endpoint(object):
    def __init__(self, x, y, prev_point):
        self.coords = (x, y)
        self.prevPoint = prev_point

    def split_coords(self):
        return self.coords.x, self.coords.y


def main():
    start = time.time()
    random.seed()
    num_steps = int(sys.argv[1])  # BAD, ASSUMES VALUE PASSED
    width = 10
    height = 10

    # initialize the matplotlib graph
    plt.ion()
    plt.show()

    ax.set_xlim(-1, width + 1)
    ax.set_ylim(-1, height + 1)

    rrt = RRT(50, 50, width, height, 1)

    for p in islice(rrt.quad_tree.pointList, None):
        if p.prevPoint is not None:
            epA = p
            epB = epA.prevPoint
            line = LineString([Point(epA.coords), Point(epB.coords)])

            x, y = line.xy
            ax.plot(x, y, color="blue")
            plt.pause(0.001)

    count = 2
    new_point = (random.random() * width, random.random() * height)
    target_point = Endpoint(80, 40, None)

    while count < num_steps:
        # while new_point.split_coords() != target_point.split_coords():
        temp_point = rrt.closest_point(new_point)
        if temp_point:
            count += 1
            #line = LineString([Point(temp_point.coords), Point(temp_point.prevPoint.coords)])
            #x, y = line.xy
            #ax.plot(x, y, color="blue")
            plt.pause(0.001)
        new_point = (random.random() * width, random.random() * height)

    #draw_path(rrt, target_point)

    plt.ioff()
    plt.show()
    print time.time() - start

if __name__ == "__main__":
    #cProfile.run('main()')
    main()