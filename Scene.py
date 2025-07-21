from camera import *
from MObject import *
import pygame as py

# TODO
# - rasterization for abs(diff_x) < 1
# - rasterization for both points being outside
# - maybe render everything, even though its outside, connections still might be in. (except stuff behind camera)

class Scene:
    # left handed coordinate system!
    def __init__(self, fov = 1.0, camera_position = (0, 0, 0), screen_width = 1600, screen_ratio = (16, 9)):
        self.ScreenSize: tuple[int] = (screen_width, screen_width * (screen_ratio[1] / screen_ratio[0]))
        self.ScreenRatio = screen_ratio
        self.Screen = py.PixelArray(py.Surface(self.ScreenSize))
        self.Camera = Camera(position=point(camera_position))
        # width of plane to project onto
        self.FOV = (fov, fov * (screen_ratio[1] / screen_ratio[0]))
        self.Objects: list[MObject] = []
        # TODO maybe muss der Hint weg, damit es für Triangles etc. die überschriebene methode nimmt
    def add(self, object):
        self.Objects.append(object)
    
    
    def __cameraTransform(self, objs: list[MObject]):
        cameraTransform = self.Camera.getCameraTransformMatrix()
        transformed: list[MObject] = []
        # TODO maybe muss der Hint weg, damit es für Triangles etc. die überschriebene methode nimmt
        for obj in objs:
            transformed.append(
                obj.applyCameraTransform(cameraTransform)
            )
        return transformed
    def __pinholeProject(self, objs: list[MObject]):
        res: list[MObject] = []
        # finding deepest point in image (biggest z value)
        deepest_point = 0
        for obj in objs:
            deepest_point_Object = max(obj.getZ())
            if deepest_point_Object > deepest_point:
                deepest_point = deepest_point_Object
            # remove objects behind the camera from render list (z < 0)
            if deepest_point_Object < 0:
                objs.remove(obj)
        
        # pinholeProject objects
        for obj in objs:
            projected_obj = obj.applyCameraProjection(deepest_point)
            # check wether projection is inside of FOV.
            # The FOV is a rectangle at z = 1 with its center right at (0, 0, 1)
            # everything on that size-adjustable rectangle is gonna be in the field of view
            res.append(self.__InFOV(projected_obj))
        # remember, that at that point, the third coordinate of each point is just a depth information!
        # we keep it as MObjects, to keep information about the connections, but the MObjects do not represent three dimensional point!
        return res
    def __scaleToScreen(self, objs: list[MObject]):
        res: list[MObject] = []
        outer_corner = base([self.FOV[0] * 0.5, self.FOV[1] * -0.5, 0])
        # the outer corner (positive x and positive y) of the plane where everything got projected onto
        # by adding this to each point, we move the origin to the top left and everything else to the first quadrant
        # the minus for the y-coordinate is on purpose: its for flipping the screen.
        scalar = self.ScreenSize[0] / self.FOV[0]
        for obj in objs:
            points: list[base] = []
            for point in obj.Points:
                new_point = (point + outer_corner).scale(scalar, False)
                # round the decimals of, complete y-inversion of coords by negating y-coordinate
                new_point[0] = round(new_point[0])
                new_point[1] = round(-new_point[1])
                points.append(new_point)
            res.append(MObject.fromRawData(points, obj.Conns))
        return res
    def __drawAndRasterize(self, objs: list[MObject]):
        for obj in objs:
            # draw points
            for point in obj.Points:
                self.Screen[
                    round(point[0] - obj.StrokeWidth) : round(point[0] + obj.StrokeWidth + 1), 
                    round(point[1] - obj.StrokeWidth) : round(point[1] + obj.StrokeWidth + 1)
                ] = obj.Color
                # apply stroke_width; stop is exclusive, thats why + 1 is necessary
            
            # rasterize
            for conn in obj.Conns:
                points = self.__SortConn(obj.Points[conn[0]], obj.Points[conn[1]])
                if len(points) == 0:
                    # need to check wether line is inside at some point!
                    continue
                
                diff_x = round(points[1][0] - points[0][0])
                diff_y = round(points[1][1] - points[0][1])
                
                
                if abs(diff_x) < 1:
                    if abs(diff_y) < 1:
                        # no connection needs to be drawn, jump to next conn
                        continue
                    else:
                        # TODO: rasterization when diff_x < 1
                        continue
                m: float = diff_y / diff_x
                for num in range(1, abs(diff_x)):
                    # num = 0 and num = diff_x are already drawn
                    # negate num, when rasterize from right to left (m is not negated on purpose here!)
                    if diff_x < 0:
                        num = -num
                    x = round(points[0][0] + num)
                    y = round(points[0][1] + num * m)
                    if not self.__isInside(base([x, y])):
                        # no further check are needed, cause if one point is outside its the one at index 1
                        # no chance, that x and y are gonna be inside again, so jump to next conn
                        break

                    self.Screen[x, y] = obj.Color
                    
                    #TODO apply stoke_Width
                    # TODO very steep lines (diff_x = 0 or 1, but diff_y = 800)
    def __isInside(self, point: base):
        """Check wether a projected and scaled point is inside of the screen.
        Needed to check for cutt offs

        Args:
            point (base): The 2d point to check 

        Returns:
            _type_: boolean representing the result
        """
        result = True
        # x outside?
        if point[0] >= self.ScreenSize[0] or point[0] < 0:
            result &= False
        # y outside?
        if point[1] >= self.ScreenSize[1] or point[1] < 0:
            result &= False
        return result
    def __InFOV(self, obj: MObject):
        """removes the parts of an MObject, that aren't depicted on the screen, cause they are outside,
        by cheking each (extended) connection to touch the outer edges of the FOV.
        Each connection that touches two edges is being kept, as well as the points, that the connection consists of.
        Each connection that touches no edge is being removed, but the points my be kept for other connections that are inside

        Args:
            obj (MObject): the MObject to work on.

        Returns:
            _type_: Another MObject, with only the points and connections that are necessary for drawing
        """
        # TODO: make that it returns the MObject with only the conns that need to be drawn
        # (also remove points, that have no connection then)
        x_zero = 0.5 * self.FOV[0]
        y_zero = 0.5 * self.FOV[1]
        result_points: list[base] = []
        result_conns: list[tuple[int]] = []
        for conn in obj.Conns:
            results: list[bool] = []
            func = self.__GetLineFunction(obj.Points[conn[0]], obj.Points[conn[1]], False)
            func_inverse = self.__GetLineFunction(obj.Points[conn[0]], obj.Points[conn[1]], True)
            vertical_edges = (func(-x_zero), func(x_zero))
            horizontal_edges = (func_inverse(-y_zero), func_inverse(y_zero))
            # test vertical edges
            results.append((-y_zero <= vertical_edges[0]) & (vertical_edges[0] <= y_zero)) # left
            results.append((-y_zero <= vertical_edges[1]) & (vertical_edges[1] <= y_zero)) # right
            # test horizontal edges:
            results.append((-x_zero <= horizontal_edges[0]) & (horizontal_edges[0] <= x_zero)) # bottom
            results.append((-x_zero <= horizontal_edges[1]) & (horizontal_edges[1] <= x_zero)) # up
            # check wether there was at least one point on edges
            if any(results):
                # append points to new point list, if not already in
                if obj.Points[conn[0]] not in result_points:
                    result_points.append(obj.Points[conn[0]])
                if obj.Points[conn[1]] not in result_points:
                    result_points.append(obj.Points[conn[1]])
                # find changed conn indexes and append those to result_conns
                new_conn = (result_points.index(obj.Points[conn[0]]), result_points.index(obj.Points[conn[1]]))
                result_conns.append(new_conn)
        return MObject.fromRawData(result_points, result_conns)
    def __SortConn(self, first: base, second: base):
        """sorts the two projected points of a connection, 
        so that the one being outside of the fov is placed at index 1.
        That helps with the cutt offs during rasterization.
        if both points are inside, the point with smaller x-value is placed at index 0
        if both points are outside it returns an empty tuple

        Args:
            first (base): the first point of the connection
            second (base): the second point of the connection

        Returns:
            _type_: a tuple of two point with the one being outside at index 1. empty, when both points are outside
        """
        firstInside = self.__isInside(first)
        secondInside = self.__isInside(second)
        if (not firstInside) and (not secondInside):
            return ()
        elif firstInside and (not secondInside):
            return (first, second)
        elif (not firstInside) and secondInside:
            return (second, first)
        else:
            # if both inside place point with smaller x at index 0
            if first[0] <= second[0]:
                return (first, second)
            else:
                return (second, first)
    @staticmethod
    def __GetLineFunction(point1: base, point2: base, inverse: bool = False):
        """computes the linear function that connects point1 to point2 in 2d space
        Can handle 2.5 dimensional points (2d points with a depth information as third coordinate)

        Args:
            point1 (base): one point on the linear function
            point2 (base): another point on the linear function
            inverse (bool): wether to return the function with respect to x or to y.
            False returns linear function with respect to x (f(x)). Defaults to False

        Raises:
            ValueError: if input points are not 2dimensional

        Returns:
            _type_: the function as lambda, that takes in one x or y value and computes its y or x value.
        """
        if point1.dimensions < 2 or point2.dimensions < 2:
            raise ValueError("Method Scene.__PointOnLine() can only operate on 2d points")
        if not inverse:
            m_ = (point2[1] - point1[1]) / (point2[0] - point2[0])
            c_ = point1[1] - m_ * point1[0]
            return lambda x, m = m_, c = c_ : m * x + c
        else:
            m_ = (point2[0] - point1[0]) / (point2[1] - point1[1])
            c_ = point1[0] - m_ * point1[1]
            return lambda y, m = m_, c = c_ : m * y + c

    def render(self):
        py.init()
        self.Screen = py.PixelArray(py.display.set_mode((self.ScreenSize)))

        # camera transformation
        cameraTransformed = self.__cameraTransform(self.Objects)
        # camera projection
        pinhole_projected = self.__pinholeProject(cameraTransformed)
        # scaling
        scaledOnScreen = self.__scaleToScreen(pinhole_projected)
        # draw and rasterize
        self.__drawAndRasterize(scaledOnScreen)
        # display changes
        py.display.flip()

        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
        py.quit()