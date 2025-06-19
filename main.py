import numpy as np



class base:
    def __init__(self, data: list):
        self.dimensions = len(data)
        self.__data = np.ndarray(data)
    def __init__(self, data: np.ndarray):
        if len(data.shape) != 1:
            raise ValueError(
                'Unable to create a vector out of an array of shape ' +
                data.shape +
                ', too much dimensions.'
                )
    def __getitem__(self, key: int):
        if len(self.__data) <= key:
            return None
        return self.__data[key]
    def __add__(self, other):
        return base(self.__data + other.__data)

class vector(base):
    def __init__(self, data):
        super().__init__(data)
    def apply(self, point):
        if self.dimensions != point.dimensions:
            raise ValueError() # TODO
        return point(point + self)
    
class point(base):
    def __init__(self, data):
        super().__init__(data)
    '''creates a vector pointing from self to the given tip'''
    def vectorto(self, tip):
        return vector(tip - self)
    def vectorfrom(self, start): 
        return vector(self - start)

'''creates a vector leading from start to tip'''
def vbp(start: base, tip: base):
    return base(tip - start)


class matrix:
    def __init__(self, matrix: np.ndarray):
        self.Shape = matrix.shape
        self.__data = matrix
    def __init__(self, shape: tuple):
        self.Shape: tuple = shape
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
    def __mul__(self, other):
        if type(other) != matrix:
            raise TypeError(
                "Can't multiplie matrix with object of type " +
                str(type(other)) + 
                ". For multiplication of matrix and vector use method \'use\'."
            )
        if (self.Shape != other.Shape) or (self.Shape[0] != self.Shape[1]):
            raise NotImplementedError("Multiplication of matrices with diferrent shapes or not quadratic matrices isn't implemented yet")
            # TODO
        erg = np.zeros(self.Shape)
        for index1 in range(self.Shape[1]):         # iterating throug rows of first matix, using Shape to get count of rows
            for index2 in range(other.Shape[0]):    # iterating throug columns of second matrix, using Shape, to get the count of colums
                for pos in range(self.Shape[0]):    # iterating throug elems in rows of first natrix and colums of second matix
                    erg[index2][index1] += \
                        self.__data[pos][index1] * \
                        other.__data[index2][pos]
        return erg
    def use(self, other: vector) -> vector:
        input_dim = self.Shape[1] # The dimension of the input vector
        if other.dimensions != input_dim:
            raise ValueError(
                'Unable to use a matrix of shape ' + self.Shape +
                ' on a vector with ' + other.dimensions + ' dimensions'
            )
        output_dim = self.Shape[0] # the dimension of the output vector
        erg = [0 for n in range(output_dim)]
        for result_index in range(output_dim):
            erg[result_index] = [0 for n in range(input_dim)]
            for index in range(input_dim):
                erg[result_index] += other[index] * self.__data[result_index][index]
        return vector(erg)
    def getr(self):
        return self.__data


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
    def morph(self):
        return Vector([self.X, self.Y, self.Z])
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