from camera import *
from MObject import *
import pygame as py

class Scene:
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
            # per default true, cause its gonna turn false, if one point is inside the FOV
            ObjectOutside = True
            for point in projected_obj.Points:
                if point[0] > self.FOV[0] * 0.5:
                    ObjectOutside &= True
                    continue
                elif point[0] < -self.FOV[0] * 0.5:
                    ObjectOutside &= True
                    continue
                if point[1] > self.FOV[1] * 0.5:
                    ObjectOutside &= True
                    continue
                elif point[1] < -self.FOV[1] * 0.5:
                    ObjectOutside &= True
                    continue
                # if one point is not outside, the entire object needs to be rendered
                ObjectOutside &= False
            if ObjectOutside == False:
                res.append(projected_obj)
        # remember, that at that point, the third coordinate of each point is just a depth information!
        # we keep it as MObjects, to keep information about the connections!
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
                # check which of both points is inside, for cutt offs
                # TODO maybe auslagern...
                first_inside = self.__isInside(obj.Points[conn[0]])
                second_inside = self.__isInside(obj.Points[conn[1]])
                points: list[base] = []
                # sort points, so that the point inside is at index 0
                if (not first_inside) and (not second_inside):
                    # both outside, no connection needed
                    continue
                elif (not first_inside) and second_inside:
                    points = [obj.Points[conn[1]], obj.Points[conn[0]]]
                elif first_inside and (not second_inside):
                    points = [obj.Points[conn[0]], obj.Points[conn[1]]]
                else:
                    # if both are inside take the one with smaller x at index 0
                    if obj.Points[conn[0]][0] <= obj.Points[conn[1]][0]:
                        points = [obj.Points[conn[0]], obj.Points[conn[1]]]
                    else:
                        points = [obj.Points[conn[1]], obj.Points[conn[0]]]

                # rasterize
                diff_x = round(points[1][0] - points[0][0])
                diff_y = round(points[1][1] - points[0][1])
                if abs(diff_x) < 1:
                    # no connection needs to be drawn, jump to next conn
                    continue
                m: float = diff_y / diff_x
                for num in range(1, abs(diff_x)):
                    # num = 0 and num = diff_x are already drawn
                    # negate num, when rasterize from right to left (m is not negated on purpose here!)
                    if diff_x > 0:
                        num = -num
                    x = round(points[0][0] + num)
                    y = round(points[0][1] + num * m)
                    if not self.__isInside(base([x, y])):
                        # no further check are needed, cause if one point is outside its the one at index 1
                        # no chance, that x and y are gonna be inside again, so jump to next conn
                        break

                    self.Screen[
                        round(points[0][0] + num), 
                        round(points[0][1] + num * m)
                    ] = obj.Color
                    
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