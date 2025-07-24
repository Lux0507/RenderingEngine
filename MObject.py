from base import *

class MObject:
    def __init__(self, points: list[Point3D] = (), connections: list[tuple[float]] = [],
                 color: tuple[int] = (255, 255, 255), stroke_width: int = 1):
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
        for point in points:
            self.Points.append( base.create(point.get()) )
        MObject.__ConnsValidation(self.Points, connections)
        self.Conns = connections
        # style
        self.Color = color
        self.StrokeWidth = stroke_width
        # TODO fill, stroke_width, opacity of fill...
    @staticmethod
    def fromRawData(points: list[base], connections: list[tuple[float]]):
        obj = MObject()
        obj.Points = points
        MObject.__ConnsValidation(points, connections)
        obj.Conns = connections
        return obj
    def __str__(self):
        res = "points: ["
        for index in range(len(self.Points)):
            res += str(index + 1) + ": "
            res += str(self.Points[index])
            if index != len(self.Points) - 1:
                res += ",  "
            else:
                res += "]"
        res += "; conns: ["
        for index in range(len(self.Conns)):
            tp = (self.Conns[index][0] + 1, self.Conns[index][1] + 1)
            res += str(tp)
            if index != len(self.Conns) - 1:
                res += ", "
            else:
                res += "]"
        res += "; color: " + str(self.Color)
        return res
        # TODO: add other elements
    def __repr__(self):
        res = "MObject.MObject(["
        for index in range(len(self.Points)):
            res += f"Point3D({self.Points[index][0]}, {self.Points[index][1]}, {self.Points[index][2]})"
            if index != len(self.Points) - 1:
                res += ", "
            else:
                res += "]"
        res += f", connections={self.Conns}, color={self.Color}, stroke_width={self.StrokeWidth}"
        return res
    def __eq__(self, other):
        # check points 
        l = [x == y for x, y in zip(sorted(self.Points), sorted(other.Points))]
        # TODO find a __lt__ that doesn't ignores elements with same magnitude (as now)
        if not all(l):
            return False
        
        #check amount of connections
        if len(self.Conns) != len(other.Conns):
            return False
        
        #check connections
        res = True
        for first_index in range(len(self.Points)):
            #finding the matching elem in other
            second_index = 0
            while second_index < len(other.Points):
                if self.Points[first_index] == other.Points[second_index]:
                    break
                else:
                    second_index += 1

            # collect all connections of both points
            first_connected_to: list[base] = []
            second_connected_to: list[base] = []
            for first, second in zip(self.Conns, other.Conns):
                if first[0] == first_index:
                    first_connected_to.append(self.Points[first[1]])
                if first[1] == first_index:
                    first_connected_to.append(self.Points[first[0]])
                if second[0] == second_index:
                    second_connected_to.append(other.Points[second[1]])
                if second[1] == second_index:
                    second_connected_to.append(other.Points[second[0]])
            # sort lists to compare
            first_connected_to.sort()
            second_connected_to.sort()
            # compare
            res &= all([x == y for x, y in zip(first_connected_to, second_connected_to)]) # turns False if only one connected point is not equal
        return res
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
        projected_points = [matrix.use(point.homogenous()).project() for point in self.Points]
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