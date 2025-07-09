import numpy as np
from math import * 


class base:
    def __init__(self, data: list):
        self.dimensions = len(data)
        self.data = np.array(data)
        self.__curr = 0
        self.__end = self.dimensions
    # def __init__(self, data: np.ndarray):
    #     if len(data.shape) != 1:
    #         raise ValueError(
    #             'Unable to create a vector out of an array of shape ' +
    #             data.shape +
    #             ', too much dimensions.'
    #             )
    def __len__(self):
        return len(self.data)
    def __getitem__(self, key: int):
        if len(self.data) <= key:
            return None
        return self.data[key]
    def __setitem__(self, key: int, value):
        if len(self.data) <= key:
            raise IndexError("Can't write out of index")
        self.data[key] = value
    def __iter__(self):
        return self
    def __next__(self):
        if self.__curr >= self.__end:
            raise StopIteration
        result = self.data[self.__curr]
        self.__curr += 1
        return result
    def __neg__(self):
        res = [-elem for elem in self.data]
        return base(res)
    def __add__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError(
                "Can't add two vectors with different dimensions"
            )
        return base(self.data + other.__data)
    def __sub__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError(
                "Can't add two vectors with different dimensions"
            )
        return base(self.data - other.__data)
    def scale(self, factor):
        return base(self.data * factor) # multipliing a list with a scalar
    '''removes one dimension of coordinates by applying pinhole camera projection'''


point = base

class vector(base):
    def __init__(self, data: list):
        super().__init__(data)
    def magnitude(self):
        sum = 0
        for elem in self.data:
            sum += elem ** 2
        return sqrt(sum)
    def __mul__(self, other):
        if type(other) == base:
            return self.crossProd(other)
        else:
            return self.scale(other)
    def normalize(self):
        return self.scale(1/self.magnitude)
    def dotProd(self, other):
        pass
    def crossProd(self, other):
        if (self.dimensions !=3) or (other.dimension != 3):
            raise ValueError(
                "cross product only works on vectors in three dimensions." +\
                "Got vectors with dimensions " + self.dimensions + " and " +\
                other.dimensions
            )

    def angleToVector(self, other):
        return abs(
            acos(
                self.dotProd(other) / \
                (self.magnitude * other.magnitude)
            )
        )
    def apply(self, point):
        if self.dimensions != point.dimensions:
            raise ValueError() # TODO
        return point(point + self)
    def project(self):
        res = []
        for num in range(self.dimensions - 1):
            res.append(
                self.data[num]/self.data[-1]
            )
        return res

class matrix:
    @classmethod
    def fromData(cls, matrix: np.ndarray):
        cls.shape = matrix.shape
        cls.__data = matrix
        cls.__curr = 0
        cls.__end = matrix.shape[0]
    def __init__(self, shape: tuple):
        self.shape: tuple = shape
        self.__data: np.ndarray = np.zeros(shape)
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
    def __mul__(self, other):
        if type(other) != matrix:
            raise TypeError(
                "Can't multiplie matrix with object of type " +
                str(type(other)) + 
                ". For multiplication of matrix and vector use method \'use\'."
            )
        if (self.shape != other.shape) or (self.shape[0] != self.shape[1]):
            raise NotImplementedError("Multiplication of matrices with diferrent shapes or not quadratic matrices isn't implemented yet")
            # TODO
        erg = matrix(self.shape)
        for index1 in range(self.shape[1]):         # iterating throug rows of first matix, using Shape to get count of rows
            for index2 in range(other.shape[0]):    # iterating throug columns of second matrix, using Shape, to get the count of colums
                for pos in range(self.shape[0]):    # iterating throug elems in rows of first natrix and colums of second matix
                    erg[index2, index1] += \
                        self.__data[pos][index1] * \
                        other.__data[index2][pos]
        return erg
    def use(self, other: vector) -> vector:
        input_dim = self.shape[1] # The dimension of the input vector
        if other.dimensions != input_dim:
            raise ValueError(
                'Unable to use a matrix of shape ' + self.shape +
                ' on a vector with ' + other.dimensions + ' dimensions'
            )
        output_dim = self.shape[0] # the dimension of the output vector
        erg = vector([0 for n in range(output_dim)])
        for result_index in range(output_dim):
            for index in range(input_dim):
                erg[result_index] += other[index] * self.__data[result_index][index]
        return vector(erg)
    def getr(self):
        return self.__data

'''creates a vector leading from start to tip'''
def vbp(start: point, tip: point, normalize: bool = False):
    erg = vector(tip - start)
    if normalize:
        return erg.normalize()
    else:
        return erg

def create(vector: base):
    if len(vector) != 3:
        raise ValueError("'Unable to create Vector3D. input vector has wrong amount of dimensions")
    return Vector3D(*vector)

def createRotationMatrixX(angle):
    m = matrix((4, 4))
    s = sin(angle)
    c = cos(angle)
    m[0, 0] = 1
    m[1, 1] = c
    m[1, 2] = -s
    m[2, 1] = s
    m[2, 2] = c
    m[3, 3] = 1
    return m

def createRotationMatrixY(angle):
    m = matrix((4, 4))
    s = sin(angle)
    c = cos(angle)
    m[0, 0] = c
    m[0, 2] = s
    m[1, 1] = 1
    m[2, 0] = -s
    m[2, 2] = c
    m[3, 3] = 1
    return m

def createRotationMatrixZ(angle):
    m = matrix((4, 4))
    s = sin(angle)
    c = cos(angle)
    m[0, 0] = c
    m[0, 1] = -s
    m[1, 0] = s
    m[1, 1] = c
    m[2, 2] = 1
    m[3, 3] = 1
    return m




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
    '''gives the Vector3D in homogenous coordinates'''
    def homogenous(self, last_cord = 1):
        return base([self.X, self.Y, self.Z, last_cord])
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
    def project(self, deepest_z):
        return base(
            [self.X / self.Z, self.Y / self.Z, self.Z / deepest_z]
        )










# class matrix3x3:
#     def __init__(self, matrix: np.ndarray):
#         if matrix.shape != (3, 3):
#             raise ValueError(
#                 'Unable to create a 3x3 matrix out of a array of shape ' + matrix.shape
#                 )
#         self.Shape = (3, 3)
#         self.__data = matrix
#     def __mul__(self, other: vector):
#         if other.Dimensions != 3:
#             raise ValueError('Can\'t use a 3x3 matrix on a vector of ' + other.Dimensions + ' dimensions')
#         erg = [0 for n in range(3)]
#         for result_index in range(3):
#             erg[result_index] = [0 for n in range(3)]
#             for index in range(3):
#                 erg[result_index] += other[index] * self.__data[result_index][index]
#         return vector(erg)