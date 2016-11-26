
class quadNode(object):
    def __init__(self, center, halfDim):
        """Initialize the quadNode with center tuple (x, y) and halfDim being 1/2 of side length"""
        self.NODE_CAPACITY = 4
        self.area = AABB(center, halfDim)
        self.pointList = []
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = None

    def addPoint(self, point):
        """Adds point to Quadtree, creating new nodes as needed."""
        #check if point intersects bounding box
        if not self.area.intersectsPoint(point):
            return False

        #check if node is at capacity and create children if it is
        if len(self.pointList) >= self.NODE_CAPACITY:
            offset = self.area.halfDim / 2
            x = self.area.center[0]
            y = self.area.center[1]
            self.topLeft = quadNode((x - offset, y + offset), offset)
            self.topRight = quadNode((x + offset, y + offset), offset)
            self.bottomLeft = quadNode((x - offset, y - offset), offset)
            self.bottomRight = quadNode((x + offset, y - offset), offset)
            #resize
            return True

        #otherwise add point to pointlist
        self.pointList.append(point)
        return True


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


