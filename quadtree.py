
class quadNode(object):
    def __init__(self, center, halfDim):
        """Initialize the quadNode with center tuple (x, y) and halfDim being 1/2 of side length"""
        self.NODE_CAPACITY = 4
        self.area = AABB(center, halfDim)
        self.pointList = []
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = None

    def addPoint(self, point):
        """Adds point to Quadtree, creating new nodes as needed."""
        # check if point intersects bounding box
        if not self.area.intersectsPoint(point):
            return False

        # if node has children, try to add point to children.
        if self.topLeft != None:
            self.addPointChildren(point)

        # if space in node, add point to pointlist
        if len(self.pointList) < self.NODE_CAPACITY:
            self.pointList.append(point)
            return True

        # otherwise node is at capacity, create children and try to add point to children
        offset = self.area.halfDim / 2
        x = self.area.center[0]
        y = self.area.center[1]
        self.topLeft = quadNode((x - offset, y + offset), offset)
        self.topRight = quadNode((x + offset, y + offset), offset)
        self.bottomLeft = quadNode((x - offset, y - offset), offset)
        self.bottomRight = quadNode((x + offset, y - offset), offset)

        return self.addPointChildren(point)   # returns true if point added, false if point not added

    def addPointChildren(self, point):
        """Tries to add passed point to the node's child. Returns true if point added, false otherwise"""
        if self.topLeft.addPoint(point):
            return True
        if self.topRight.addPoint(point):
            return True
        if self.bottomLeft.addPoint(point):
            return True
        if self.bottomRight.addPoint(point):
            return True

        return False


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


class Quadtree(object):
    def __init__(self, center, halfDim):
        """Initialize the Quadtree with center tuple of (x, y) and halfDim representing 1/2 of the side length"""
        self.startNode = quadNode(center, halfDim)


