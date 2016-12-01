import numpy
from itertools import islice


class QuadNode(object):
    def __init__(self, center, half_dim, parent=None):
        """Initialize the QuadNode with center tuple (x, y) and half_dim being 1/2 of side length"""
        self.NODE_CAPACITY = 4
        self.area = AABB(center, half_dim)
        self.pointList = []
        self.parent = parent
        self.topLeft = None
        self.topRight = None
        self.bottomLeft = None
        self.bottomRight = None

    def add_point(self, point):
        """Adds point to Quadtree, creating new nodes as needed."""
        # check if point intersects bounding box
        if not self.area.intersects_point(point.coords):
            return False

        # if node has children, try to add point to children.
        if self.topLeft is not None:
            child_node = self.get_point_node(point.coords)
            return child_node.add_point(point)

        # if space in node, add point to pointlist
        if len(self.pointList) < self.NODE_CAPACITY:
            self.pointList.append(point)
            return True

        # node is at capacity, create children and try to add point to children
        offset = self.area.halfDim / 2.0
        x = self.area.center[0]
        y = self.area.center[1]
        self.topLeft = QuadNode((x - offset, y + offset), offset, self)
        self.topRight = QuadNode((x + offset, y + offset), offset, self)
        self.bottomLeft = QuadNode((x - offset, y - offset), offset, self)
        self.bottomRight = QuadNode((x + offset, y - offset), offset, self)

        child_node = self.get_point_node(point.coords)  # get the child node to add the point to
        if child_node is None:
            return False
        return child_node.add_point(point)   # returns true if point added, false if point not added

    # def addPointChildren(self, point):
    #    """Tries to add passed point to the node's child. Returns true if point added, false otherwise"""
    #    if self.topLeft.add_point(point):
    #        return True
    #    if self.topRight.add_point(point):
    #        return True
    #    if self.bottomLeft.add_point(point):
    #        return True
    #    if self.bottomRight.add_point(point):
    #        return True
    #    return False

    # def get_point_node(self, point):
    #    """Returns the node that would hold the passed point"""
    #    if self.area.intersects_point(point):  # Point is part of this node
    #        return self.getChildDir(point)  # returns correct child node or self if node has no children
    #    return None  # return None if the point is not in this node
    def get_points_aabb(self, aabb):
        """returns a list of all points in quadtree that are also in aabb"""
        points = []
        if not self.area.intersects_aabb(aabb):  # two bounding boxes don't intersect. Return False
            return points

        for p in islice(self.pointList, 0, None):
            if aabb.intersects_point(p.coords):
                points.append(p)

        if self.topLeft is None:
            return points  # if node has no children, return node's points

        # append any points from child nodes to points and return all points
        points.extend(self.topLeft.get_points_aabb(aabb))
        points.extend(self.topRight.get_points_aabb(aabb))
        points.extend(self.bottomLeft.get_points_aabb(aabb))
        points.extend(self.bottomRight.get_points_aabb(aabb))

        return points

    def get_point_node(self, point):
        """Get the correct child of node that contains passed point. Returns child node or self if node has no
            children. Returns None if point is not in node's area
        """
        if not self.area.intersects_point(point):
            return None

        if self.topLeft is None:  # base case, return node if node has no children
            return self

        offset = tuple(numpy.subtract(point, self.area.center))
        if offset[0] < 0:  # negative x
            if offset[1] > 0:  # positive y
                return self.topLeft.get_point_node(point)  # negative x, positive y from center = top left child
            return self.bottomLeft.get_point_node(point)  # negative x, negative y from center = bottom left child
        if offset[1] > 0:  # positive y
            return self.topRight.get_point_node(point)  # positive x, positive y from center = top right child
        return self.bottomRight.get_point_node(point)  # positive x, negative y from center =  bottom right child


class AABB(object):
    def __init__(self, center, half_dim):
        """Axis-aligned Bounding Box with center tuple (x, y) and half_dim being 1/2 of side length"""
        self.center = center
        self.halfDim = half_dim

    def intersects_point(self, point):
        """Checks if passed point is within the AABB and returns true if it is (false otherwise)"""
        xbound = self.center[0] - self.halfDim < point[0] < self.center[0] + self.halfDim
        ybound = self.center[1] - self.halfDim < point[1] < self.center[1] + self.halfDim
        return xbound and ybound

    def intersects_aabb(self, bb):
        """checks if passed bounding box intersects with this bounding box. Returns true if there is an intersection"""
        if self.center[0] - self.halfDim > bb.center[0] + bb.halfDim:  # bb left of bounding box (self)
            return False
        if self.center[0] + self.halfDim < bb.center[0] - bb.halfDim:  # bb right of bounding box (self)
            return False
        if self.center[1] - self.halfDim > bb.center[1] + bb.halfDim:  # bb below bounding box (self)
            return False
        if self.center[1] + self.halfDim < bb.center[1] - bb.halfDim:  # bb above bounding box (self)
            return False

        return True  # if we get here, boxes intersect


class Quadtree(object):
    def __init__(self, center, half_dim):
        """Initialize the Quadtree with center tuple of (x, y) and half_dim representing 1/2 of the side length"""
        self.startNode = QuadNode(center, half_dim)
