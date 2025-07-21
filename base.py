import numpy as np
from math import * 

PI = radians(180)

class base:
    def __init__(self, data: list):
        self.dimensions = len(data)
        self.__data = np.array(data)
        self.__curr = 0
        self.__end = self.dimensions
    @staticmethod
    def fromNumpy(data: np.ndarray):
        if len(data.shape) != 1:
            raise ValueError(
                'Unable to create a vector out of an array of shape ' +
                data.shape +
                ', too much dimensions.'
                )
        return base(data.tolist())
    def __len__(self):
        return len(self.__data)
    def __getitem__(self, key: int):
        # if key > (len(self.__data) - 1) or key < 0:
        #     raise IndexError("Index out of range")
        # else:
        return self.__data[key]
    def __setitem__(self, key: int, value):
        if len(self.__data) <= key:
            raise IndexError("Can't write out of index")
        self.__data[key] = value
    def __iter__(self):
        return self
    def __next__(self):
        if self.__curr >= self.__end:
            raise StopIteration
        result = self.__data[self.__curr]
        self.__curr += 1
        return result
    def __eq__(self, other):
        if self.dimensions != other.dimensions:
            return False
        else:
            return all([x == y for x, y in zip(self.__data, other.__data)])
    def __lt__(self, other): # overload < operator for list sorting
        for index in range(min(self.dimensions, other.dimensions)):
            if self.__data[index] != other.__data[index]:
                return self.__data[index] < other.__data[index]
        # if each element equals each other
        return False
    def __neg__(self):
        res = [-elem for elem in self.__data]
        return base(res)
    def __add__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError(
                "Can't add two vectors with different dimensions"
            )
        return base(self.__data + other.__data)
    def __sub__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError(
                "Can't add two vectors with different dimensions"
            )
        return base(self.__data - other.__data)
    def __str__(self):
        res = "["
        for index in range(len(self.__data)):
            res += str(self.__data[index])
            if index != len(self.__data) - 1:
                res += ", "
            else:
                res +="]"
        return res
    def __repr__(self):
        res = "base.base("
        res += str(self)
        res += ")"
        return res
    def scale(self, factor, scale_last: bool = True):
        """scale each element of the vector/point by a scalar.
        Can be used to scale each element except the last

        Args:
            factor (_type_): the factor to scale with
            scale_last (bool, optional): wether to apply the scaling onto the last element. Defaults to True.

        Returns:
            _type_: the scaled vector/point
        """
        new_data = self.__data * factor # multipliing a list with a scalar
        if not scale_last:
            new_data[-1] = self.__data[-1]
        return base(new_data) 
    def magnitude(self):
        """considering this element being a vector pointing form the origin to the coordinates defined by this element,
        this funtion computes the length of that vector (distance of the point)

        Returns:
            _type_: the magnitude of this vector
        """
        sum = 0
        for elem in self.__data:
            sum += elem ** 2
        return sqrt(sum)
    def normalize(self):
        """normalizes this vector to a length of 1

        Returns:
            _type_: the normalized vector
        """
        return self.scale(1/self.magnitude)
    def angleToVector(self, other):
        """computes the angle from self to another vector given by other

        Args:
            other (_type_): the other vector defining the angle to compute

        Returns:
            _type_: the angle in radians
        """
        return abs(
            acos(
                self.dotProd(other) / \
                (self.magnitude() * other.magnitude())
            )
        )
    def dotProd(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError("Can't compute dotProduct of vectors of different dimensions")
        else:
            sum = 0
            for index in range(self.dimensions):
                sum += self.__data[index] * other.__data[index]
            return sum
    def crossProd(self, other):
        if (self.dimensions != 3) or (other.dimension != 3):
            raise ValueError(
                "cross product only works on vectors in three dimensions." +\
                "Got vectors with dimensions " + self.dimensions + " and " +\
                other.dimensions
            )
        else:
            # TODO
            pass
    
    def project(self):
        """projects the vector/point onto the plane wich is defined by the equation 'last = 1'
        So for three dimensions, it projects the vector/points onto z = 1

        Returns:
            _type_: the projected vector/point with one less dimension
        """
        res = []
        for num in range(self.dimensions - 1):
            res.append(
                self.__data[num]/self.__data[-1]
            )
        return base(res)
    def homogenous(self, plane = 1):
        """Add one dimension to this point/vector to be able to perform translations by matrix multiplication.

        Args:
            plane (int, optional): The plane of the higher dimension to settle the point. Defaults to 1.

        Returns:
            _type_: The homogenous representation for the point/vector
        """
        new_data = np.append(self.__data, plane)
        return self.fromNumpy(new_data)
    def pinholeProject(self, deepest_z):
        res = []
        for index in range(self.dimensions):
            # for all elements except the last: divide by last element
            if index != self.dimensions - 1:
                res.append(self.__data[index]/self.__data[-1])
            # for the last element: divide by deepest_z and keep depth information
            else:
                res.append(self.__data[index]/deepest_z)
        return base(res)

point = base
vector = base

class matrix:
    """gives a huge UI for creating, storing and computing with 2x2 matrices
    """
    def __init__(self, shape: tuple):
        self.shape: tuple = shape
        self.__data: np.ndarray = np.zeros(shape)
    @staticmethod
    def unitMatrix(shape: tuple):
        m = matrix(shape)
        for num in range(min(shape[0], shape[1])): # for non-square matrices
            m[num, num] = 1
        return m
    @staticmethod
    def fromList(matrix: list):
        amRows = len(matrix)
        if type(matrix[0]) == type(list):
            amColums = len(matrix[0])
        for rowVector in matrix:
            if not (type(rowVector) == type(list)):
                raise ValueError("Can't build matrix from one-dimensional list")
            if not (len(rowVector) == amColums):
                raise ValueError("Can't build matrix from list containing lists of different lengths")
            # TODO iterate throug rowvector and check content
        m = matrix((amRows, amColums))
        for row in amRows:
            for column in amColums:
                m[row, column] = matrix[row][column]
        return m
    @staticmethod
    def fromData(matrix_: np.ndarray):
        m = matrix(matrix_.shape)
        m.__data = matrix_
        return m
    def __getitem__(self, index):
        if type(index) != tuple: # No tuple as argument
            raise TypeError(
                "Can't index with obejct of type " + \
                str(type(index)) + \
                " in matrix"
            )
        if (len(index) != 2):   # tuple has not correct amount of coordinates
            raise ValueError(
                "Exspected two values inside of tuple to index in matrix. Got " + \
                str(len(index)) + " instead."
            )
        if (type(index[0]) != int) or (type(index[1]) != int): # tuple has no integers
            raise ValueError(
                "exspected indexing tuple to hold integers. Got " + \
                str(type(index[0])) + " and " + str(type(index[1])) + \
                "instead."
            )
        return self.__data[index[0]][index[1]]
    def __setitem__(self, index: tuple, value = 0):
        if (type(index) != tuple):
            raise TypeError(
                "Can't index with obejct of type " + \
                str(type(index)) + \
                " in matrix"
            )
        self.__data[index[0]][index[1]] = value
    def __iter__(self):
        return self
    def __next__(self):
        if self.__curr >= self.__end:
            raise StopIteration
        result = self.__data[self.__curr]
        self.__curr += 1
        return result
    def __str__(self):
        res = ""
        for rowindex in range(self.shape[0]):
            if rowindex == 0:
                res += "⌈"
            elif rowindex == self.shape[0] - 1:
                res += "⌊"
            else:
                res += "|"
            for columnindex in range(self.shape[1]):
                res += str(self.__data[rowindex, columnindex])
                if columnindex != self.shape[1] - 1:
                    res += ", "
                else:
                    if rowindex == 0:
                        res += "⌉"
                    elif rowindex == self.shape[0] - 1:
                        res += "⌋"
                    else:
                        res += "|"
            res += "\n"
        return res
    def __repr__(self):
        erg = "matrix.fromList(["
        for row in range(self.shape[0]):
            erg += "["
            for column in range(self.shape[1]):
                erg += str(self.__data[row][column])
                # if not last elem
                if not (column == (self.shape[1] - 1)):
                    erg += ", "
            erg += "]"
            if not (row == (self.shape[0] - 1)):
                erg += ", "
        erg += "])"
        return erg
    def __mul__(self, other):
        if type(other) != matrix:
            raise TypeError(
                "Can't multiplie matrix with object of type " +
                str(type(other)) + 
                ". For multiplication of matrix and vector use method \'use\'."
            )
        if (self.shape != other.shape) or (self.shape[0] != self.shape[1]):
            raise NotImplementedError("Multiplication of matrices with diferrent shapes or not quadratic matrices isn't implemented yet")
            # TODO self.shape[1] == other.shape[0]
        erg = matrix(self.shape)
        for index1 in range(other.shape[1]):         # iterating throug colums of right matix, using Shape to get count of colums
            for index2 in range(self.shape[0]):    # iterating throug rows of left matrix, using Shape, to get the count of rows
                for pos in range(other.shape[0]):    # iterating throug elems in colums of right natrix and rows of left matix
                    erg[index2, index1] += \
                        self.__data[index2][pos] * \
                        other.__data[pos][index1]
        return erg
    def __rmul__(self, other):
        # TODO
        pass
    def use(self, other: base) -> base:
        input_dim = self.shape[1] # The dimension of the input vector
        if other.dimensions != input_dim:
            raise ValueError(
                'Unable to use a matrix of shape ' + self.shape +
                ' on a vector with ' + other.dimensions + ' dimensions'
            )
        output_dim = self.shape[0] # the dimension of the output vector
        erg = base([0.0 for n in range(output_dim)])
        for result_index in range(output_dim):
            for index in range(input_dim):
                erg[result_index] += other[index] * self.__data[result_index][index]
        return base(erg)
    def getr(self):
        return self.__data

def vbp(start: point, tip: point, normalize: bool = False):
    """creates a vector between points

    Args:
        start (point): the point where the vector should start
        tip (point): the point where the vector should end
        normalize (bool, optional): Wether the vector to return should be normalized. Defaults to False.

    Returns:
        _type_: a vector pointing from start into the direction of end, either normalized or not
    """
    erg = vector(tip - start)
    if normalize:
        return erg.normalize()
    else:
        return erg

def createRotationMatrixX(angle):
    """generates a 4x4 matrix, that rotates each point in a left-handed coordinate system
    by angle (in radians) counterclockwise (when facing the origin from positive x-axis) around the x-axis

    Args:
        angle (_type_): the angle to rotate by in radians

    Returns:
        _type_: the rotation matrix
    """
    m = matrix.unitMatrix((4, 4))
    s = sin(angle)
    if isclose(s, 0.0, abs_tol=1e-12):
        s = 0.0
    if isclose(s, 1.0, abs_tol=1e-12):
        s = 1.0
    if isclose(s, -1., abs_tol=1e-12):
        s = -1.0
    c = cos(angle)
    if isclose(c, 0.0, abs_tol=1e-12):
        c = 0.0
    if isclose(c, 1.0, abs_tol=1e-12):
        c = 1.0
    if isclose(c, -1., abs_tol=1e-12):
        c = -1.0
    m[1, 1] = c
    m[1, 2] = s
    m[2, 1] = -s
    m[2, 2] = c
    return m

def createRotationMatrixY(angle):
    """generates a 4x4 matrix, that rotates each point in a left-handed coordinate system
    by angle (in radians) counterclockwise (when facing the origin from positive y-axis) around the y-axis
    

    Args:
        angle (_type_): the angle to rotate by in radians

    Returns:
        _type_: the rotation matrix
    """
    # switched -sin and sin -> left handed 
    m = matrix.unitMatrix((4, 4))
    s = sin(angle)
    if isclose(s, 0.0, abs_tol=1e-12):
        s = 0.0
    if isclose(s, 1.0, abs_tol=1e-12):
        s = 1.0
    if isclose(s, -1., abs_tol=1e-12):
        s = -1.0
    c = cos(angle)
    if isclose(c, 0.0, abs_tol=1e-12):
        c = 0.0
    if isclose(c, 1.0, abs_tol=1e-12):
        c = 1.0
    if isclose(c, -1., abs_tol=1e-12):
        c = -1.0
    m[0, 0] = c
    m[0, 2] = -s
    m[2, 0] = s
    m[2, 2] = c
    return m

def createRotationMatrixZ(angle):
    """generates a 4x4 matrix, that rotates each point in a left-handed coordinate system
    by angle (in radians) counterclockwise (when facing the origin from positive z-axis) around the z-axis

    Args:
        angle (_type_): the angle to rotate by in radians

    Returns:
        _type_: the rotation matrix
    """
    m = matrix.unitMatrix((4, 4))
    s = sin(angle)
    if isclose(s, 0.0, abs_tol=1e-12):
        s = 0.0
    if isclose(s, 1.0, abs_tol=1e-12):
        s = 1.0
    if isclose(s, -1., abs_tol=1e-12):
        s = -1.0
    c = cos(angle)
    if isclose(c, 0.0, abs_tol=1e-12):
        c = 0.0
    if isclose(c, 1.0, abs_tol=1e-12):
        c = 1.0
    if isclose(c, -1., abs_tol=1e-12):
        c = -1.0
    m[0, 0] = c
    m[0, 1] = s
    m[1, 0] = -s
    m[1, 1] = c
    return m

def round(num: float) -> int:
    """rounds the given decimal number to an integer.

    Args:
        num (float): the decimal number to round

    Returns:
        int: the rounded decimal as integer 
    """
    decimal_places = num - int(num)
    if decimal_places < 0.5:
        return int(num)
    else:
        return int(num) + 1


class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.Dimensions = 3
        self.X = x
        self.Y = y
        self.Z = z
    def __add__(self, other):
        x = self.X + other.X
        y = self.Y + other.Y
        z = self.Z + other.Z
        return Vector3D(x, y, z)
    def __sub__(self, other):
        x = self.X - other.X
        y = self.Y - other.Y
        z = self.Z - other.Z
        return Vector3D(x, y, z)
    '''Morphes the Vector3D into a base element'''
    def morph(self):
        return base([self.X, self.Y, self.Z])
    def scale(self, scalar: float):
        x = self.X * scalar
        y = self.Y * scalar
        z = self.Z * scalar
        return Vector3D(x, y, z)
    def crossProd(self, other):
        x = self.Y * other.Z - self.Z * other.Y
        y = self.Z * other.X - self.X * other.Z
        z = self.X * other.Y - self.Y - other.X
        return Vector3D(x, y, z)
    def scalarProd(self, other) -> float:
        erg = self.X * other.X + self.Y * other.Y + self.Z - other.Z
        return erg

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.X = x
        self.Y = y
        self.Z = z
    def __str__(self):
        return f"({self.X}, {self.Y}, {self.Z})"
    def __repr__(self):
        return "Point3D.Point3D" + str(self)
    def get(self) -> tuple[float]:
        """returns the coordinates of the Point3D as a tuple of (x, y, z)

        Returns:
            tuple[float]: the tuple (x, y, z)
        """
        # used in constructor of MObject
        return (self.X, self.Y, self.Z)

