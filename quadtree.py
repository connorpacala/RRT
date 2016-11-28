import numpy

class quadNode(object):
    def __init__(self, center, halfDim, parent = None):
        """Initialize the quadNode with center tuple (x, y) and halfDim being 1/2 of side length"""
        self.NODE_CAPACITY = 4
        self.area = AABB(center, halfDim)
        self.pointList = []
        self.parent = parent
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = None

    def addPoint(self, point):
        """Adds point to Quadtree, creating new nodes as needed."""
        # check if point intersects bounding box
        if not self.area.intersectsPoint(point):
            return False

        # if node has children, try to add point to children.
        if self.topLeft is not None:
            childNode = self.getPointNode(point)
            return childNode.addPoint(point)

        # if space in node, add point to pointlist
        if len(self.pointList) < self.NODE_CAPACITY:
            self.pointList.append(point)
            return True

        # node is at capacity, create children and try to add point to children
        offset = self.area.halfDim / 2
        x = self.area.center[0]
        y = self.area.center[1]
        self.topLeft = quadNode((x - offset, y + offset), offset)
        self.topRight = quadNode((x + offset, y + offset), offset)
        self.bottomLeft = quadNode((x - offset, y - offset), offset)
        self.bottomRight = quadNode((x + offset, y - offset), offset)

        childNode = self.getPointNode(point)  # get the child node to add the point to
        return childNode.addPoint(point)   # returns true if point added, false if point not added

    #def addPointChildren(self, point):
    #    """Tries to add passed point to the node's child. Returns true if point added, false otherwise"""
    #    if self.topLeft.addPoint(point):
    #        return True
    #    if self.topRight.addPoint(point):
    #        return True
    #    if self.bottomLeft.addPoint(point):
    #        return True
    #    if self.bottomRight.addPoint(point):
    #        return True
    #    return False

    #def getPointNode(self, point):
    #    """Returns the node that would hold the passed point"""
    #    if self.area.intersectsPoint(point):  # Point is part of this node
    #        return self.getChildDir(point)  # returns correct child node or self if node has no children
    #    return None  # return None if the point is not in this node

    def getPointNode(self, point):
        """Get the correct child of node that contains passed point. Returns child node or self if node has no
            children. Returns None if point is not in node's area
        """
        if not self.area.intersectsPoint(point):
            return None

        if self.topLeft is None:  # base case, return node if node has no children
            return self

        offset = tuple(numpy.subtract(point, self.area.center))
        if offset[0] < 0:  # negative x
            if offset[1] > 0:  # positive y
                return self.topLeft.getPointNode(point)  # negative x, positive y from center = top left child
            return self.bottomLeft.getPointNode(point)  # negative x, negative y from center = bottom left child
        if offset[1] > 0:  # positive y
            return self.topRight.getPointNode(point)  # positive x, positive y from center = top right child
        return self.bottomRight.getPointNode(point)  # positive x, negative y from center =  bottom right child


class AABB(object):
    def __init__(self, center, halfDim):
        """Axis-aligned Bounding Box with center tuple (x, y) and halfDim being 1/2 of side length"""
        self.center = center
        self.halfDim = halfDim

    def intersectsPoint(self, point):
        """Checks if passed point is within the AABB and returns true if it is (false otherwise)"""
        xbound = self.center[0] - self.halfDim < point[0] < self.center[0] + self.halfDim
        ybound = self.center[1] - self.halfDim < point[1] < self.center[1] + self.halfDim
        return xbound and ybound

    def intersectsAABB(self, bb):
        """checks if passed bounding box intersects with this bounding box. Returns true if there is an intersection"""
        if self.center[0] - self.halfDim > bb.center[0] + bb.halfDim:  # bb left of bounding box (self)
            return False
        if self.center[0] + self.halfDim < bb.center[0] - bb.halfDim:  # bb right of bounding box (self)
            return False
        if self.center[1] - self.halfDim > bb.center[1] + bb.halfDim:  # bb below bounding box (self)
            return False
        if self.center[1] + self.halfDim > bb.center[1] - bb.halfDim:  # bb above bounding box (self)
            return False

        return True  # if we get here, boxes intersect


class Quadtree(object):
    def __init__(self, center, halfDim):
        """Initialize the Quadtree with center tuple of (x, y) and halfDim representing 1/2 of the side length"""
        self.startNode = quadNode(center, halfDim)


