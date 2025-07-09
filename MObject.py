from main import *

class MObject:
    def __init__(self):
        pass
    def applyCameraTransform(self, matrix):
        pass
    def project(self, deepest_z):
        pass
    def getZ(self):
        pass

class Triangle(MObject):
    def __init__(self, corners: tuple[Vector3D]):
        if len(corners) != 3:
            raise ValueError("List to initialize triangle has not exactly 3 points")
        self.corners: tuple[Vector3D] = corners
    def applyCameraTransform(self, matrix: matrix):
        transfomed = [ ( Vector3D( *(matrix.use(elem.homogenous()).project() ) ) ) for elem in self.corners ]
        return Triangle(transfomed)
    def project(self, deepest_z) -> tuple[base]:
        return [point.project(deepest_z) for point in self.corners]
    def getZ(self):
        return (n.Z for n in self.corners)