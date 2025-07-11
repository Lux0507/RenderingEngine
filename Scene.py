from camera import *
from MObject import *
import pygame as py

class Scene:
    def __init__(self, fov = 1.0, camera_position = (0, 0, 0), screen_width = 1600, screen_ratio = (16, 9)):
        self.ScreenSize = (screen_width, screen_width * (screen_ratio[1] / screen_ratio[0]))
        self.ScreenRatio = screen_ratio
        self.Screen = py.Surface(self.ScreenSize)
        self.Camera = Camera(position=point(camera_position))
        # width of plane to project onto
        self.FOV = 1.0
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
    def __pinholeProject(self, objs: list[MObject], FOV: float, aspect_ratio: tuple[float]):
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
                if point[0] > self.FOV * 0.5:
                    ObjectOutside &= True
                    continue
                elif point[0] < -self.FOV * 0.5:
                    ObjectOutside &= True
                    continue
                verticalFOV = self.FOV * (self.ScreenRatio[1] / self.ScreenRatio[0])
                if point[1] > verticalFOV * 0.5:
                    ObjectOutside &= True
                    continue
                elif point[1] < -verticalFOV * 0.5:
                    ObjectOutside &= True
                    continue
                # if one point is not outside, the entire object needs to be rendered
                ObjectOutside &= False
            if ObjectOutside == False:
                res.append(projected_obj)
        # remember, that at that point, the third coordinate of each point is just a depth information!
        # we keep it as MObjects, to keep information about the connections!
        return res
    
    
    
    
    def render(self):
        # camera transformation^
        cameraTransformed = self.__cameraTransform(self.Objects)
        pinhole_projected = self.__pinholeProject(cameraTransformed, self.FOV, self.ScreenRatio)
        
        # TODO: res contains transformed and projected objects (list of tuples of coordinates).
        # now scale and move that stuff, to fit onto self.Screen
        pass
