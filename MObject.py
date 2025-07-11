from main import *

class MObject:
    def __init__(self, points: tuple[Point3D] = (), connections: list[tuple[float]] = []):
        """Creates an highly custumizable Object in 3d Space

        Args:
            points (tuple[Point3D]): the points, that the Object consists of.
            e. g. the three corners for a triangle
            connections (list[tuple[float]]): For objects with more than three points,
            specify wich points in the first argument should be connected by a tuple of the indexes of the points to connect

        Raises:
            ValueError: When index in connections argument out of range
        """
        self.Points: list[base] = []
        self.Am_Points = len(points)
        for point in points:
            self.Points.append( base(point.get()) )
        MObject.__ConnsValidation(self.Points, connections)
        self.Conns = connections
    @staticmethod
    def fromRawData(points: list[base], connections: list[tuple[float]]):
        obj = MObject()
        obj.Points = points
        MObject.__ConnsValidation(points, connections)
        obj.Conns = connections
        return obj
    @staticmethod
    def __ConnsValidation(points: list[base], conns: list[tuple[float]]):
        Am_Points = len(points)
        result = False
        for conn in conns:
            if len(conn) != 2:
                result = True
                raise ValueError("Connections in MObjects can only be made between exactly two points")
            if conn[0] > Am_Points or conn[1] > Am_Points or conn[0] < 0 or conn[1] < 0:
                result = True
                raise ValueError("Connection Index out of range. Can't create connection to point out of range")
        return result
    def applyCameraTransform(self, matrix: matrix):
        # use the matrix on each point of self.Points, therefore morph points into homogenous coordinates,
        # cause camera transformation includes a translation that can be performed by using 4 dimensions
        # after translating, project points back onto three dimensions
        projected_points = [matrix.use(point.homogenous).project() for point in self.Points]
        return MObject.fromRawData(projected_points, self.Conns)
    def applyCameraProjection(self, deepest_z):
        projected_points = [point.pinholeProject(deepest_z) for point in self.Points]
        return MObject.fromRawData(projected_points, self.Conns)
    def getZ(self):
        """returns a list of all the z-values of the points of the MObject, for finding the deepest point

        Returns:
            _type_: the list with z-values
        """
        return [n[-1] for n in self.Points]