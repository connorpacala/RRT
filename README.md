# RRT

Rapidly exploring random trees (RRTs) are one method of motion planning that caught my eye and has been used extensively in robotics. Although it wouldn't be useful for the game, the algorithm has multiple levels of complexity, making it an interesting problem to work and iterate on.

The basic idea behind an RRT is you have a start point and you randomly add new points to the area, connecting these points to the closest edge (or point) that already exists. This can be expanded further to avoid obstacles, handle kinematics, or add modifiers so the algorithm is trying to find an end point.
