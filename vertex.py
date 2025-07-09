from main import *

'''storing either a point, a line or a triangle'''
class vertex:
    def __init__(self, point: Vector3D):
        self.Coords: tuple[Vector3D] = (point)
    def __init__(self, start: Vector3D, end: Vector3D):
        self.Coords: tuple[Vector3D] = (start, end)
    def __init__(self, start: Vector3D, turn: Vector3D, end: Vector3D):
        self.Coords: tuple[Vector3D] = (start, turn, end)
    def morph(self):
        return tuple(*self.Coords)
    def applyCameraTransform(self, matrix):
        return vertex(
            (matrix * n.homogenous() for n in self.Coords)
        )    
    def render(self, matrix: matrix):
        res = []
        for elem in self.Coords:
            res.append(matrix * elem)
        return res