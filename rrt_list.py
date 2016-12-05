from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import random
from itertools import islice
import sys
import time
import cProfile


def sq_dist(point_a, point_b):
    """returns squared distance between points. Allows comparison of dist for two
    points without needing to use sqrt to calculate the actual distance.
    """
    return (point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2


class RRT(object):
    def __init__(self, start_x, start_y, grid_w, grid_h):
        """Initialize the grid and first two points in the RRT"""
        self.pointList = []
        self.coordsSet = set()  # hashtable of already added points (greatly improves runtime)

        self.width = grid_w
        self.height = grid_h

        # add the start point and the first connecting endpoint to the tree
        start_point = Endpoint(self.width / 2, self.height / 2, None)
        self.pointList.append(start_point)
        self.coordsSet.add((start_point.split_coords()))
        new_point = Endpoint(random.randint(0, self.width), random.randint(0, self.height), start_point)
        self.pointList.append(new_point)
        self.coordsSet.add((new_point.split_coords()))
        
    def closest_point(self, point):
        """calculate the closest point on the tree to the passed point and add a segment between
        the passed point and the calculated point. returns none if the point already exists in the tree
        """
        if (point.split_coords()) in self.coordsSet:
            return None
        dist = sq_dist(self.pointList[0].coords, point.coords)
        closest_end = self.pointList[0]
        intersect = None
        for p in islice(self.pointList, 1, None):   # ignore first point as it has no prevPoint
            # find the closest point on the line to the passed point
            line = LineString([p.coords, p.prevPoint.coords])
            temp_point = line.interpolate(line.project(point.coords))
            temp_dist = sq_dist(temp_point, point.coords)
            if temp_dist < dist:
                dist = temp_dist
                closest_end = p
                intersect = temp_point
        
        # if point found, add the new point to the list and update prevPoints of endpoints
        if intersect:
            new_intersect = Endpoint(intersect.x, intersect.y, closest_end.prevPoint)
            self.pointList.append(new_intersect)
            self.coordsSet.add(new_intersect.split_coords())
            closest_end.prevPoint = new_intersect
            point.prevPoint = new_intersect
            self.pointList.append(point)
            self.coordsSet.add(point.split_coords())
        else:
            point.prevPoint = self.pointList[0]
            self.pointList.append(point)
            self.coordsSet.add(point.split_coords())
                
        return True


class Endpoint(object):
    def __init__(self, x, y, prevPoint):
        self.coords = Point(x, y)
        self.prevPoint = prevPoint
        
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
        line = LineString([ep_a.coords, ep_b.coords])

        x, y = line.xy
        rrt.ax.plot(x, y, color="blue")

    plt.show()


def draw_path(rrt, target_point):
    """draw the RRT with a path from the startPoint to the passed target_point"""

    # initialize the matplotlib graph
    plt.ion()
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-1, rrt.width + 1)
    ax.set_ylim(-1, rrt.height + 1)

    temp_point = rrt.pointList[-1]
    plotted_points = []
    # start at target_point and work backwards until starting point found.
    while temp_point.prevPoint is not None:
        plotted_points.append(temp_point)
        ep_a = temp_point
        ep_b = ep_a.prevPoint
        line = LineString([ep_a.coords, ep_b.coords])

        # draw each line in red
        x, y = line.xy
        ax.plot(x, y, color="red")

        temp_point = temp_point.prevPoint

    for p in islice(rrt.pointList, 1, None):
        if p not in plotted_points:
            ep_a = p
            ep_b = ep_a.prevPoint
            line = LineString([ep_a.coords, ep_b.coords])

            x, y = line.xy
            ax.plot(x, y, color="blue")
            plt.pause(0.001)
            #fig.canvas.draw()


def main():
    start = time.time()
    random.seed()
    count = 0
    num_steps = int(sys.argv[1]) #BAD, ASSUMES VALUE PASSED
    width = 100
    height = 100
    rrt = RRT(50, 50, width, height)
    target_point = Endpoint(80, 40, None)

    """
    startPoint = Endpoint(width / 2, height / 2, None)
    rrt.pointList.append(startPoint)
    rrt.coords_set.add((startPoint.split_coords()))
    count += 1
    new_point = Endpoint(random.randint(0, width), random.randint(0, height), startPoint)
    rrt.pointList.append(new_point)
    rrt.coords_set.add((new_point.split_coords()))
    count += 1
    """

    count = 2
    new_point = Endpoint(random.randint(0, width), random.randint(0, height), None)
    # while new_point.split_coords() != target_point.split_coords():
    while count < num_steps:
        if rrt.closest_point(new_point):
            count += 1
        new_point = Endpoint(random.randint(0, width), random.randint(0, height), None)
            
    # draw_path(rrt, target_point)
    print time.time() - start
    
if __name__ == "__main__":
    cProfile.run('main()')
    # main()
