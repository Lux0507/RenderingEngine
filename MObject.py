from main import *
from vertex import *

class MObject:
    def __init__(self):
        pass
    def applyCameraTransform(self, matrix):
        pass

class Triangle(MObject):
    def __init__(self, corners: tuple[Vector3D]):
        if len(corners) != 3:
            raise ValueError("List to initialize triangle has not exactly 3 points")
        self.vertexes: tuple[vertex] = (vertex(*corners))
    def applyCameraTransfomr(self, matrix):
        return Triangle(
            (n.applyCameraTransform(matrix).morph() for n in self.vertexes)
        )


