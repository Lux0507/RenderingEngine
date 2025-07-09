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
        self.Objects: list = []
    def add(self, object):
        self.Objects.append(object)
    def render(self):
        # camera transformation
        cameraTransform = self.Camera.getCameraTransformMatrix()
        cameraTransformed: list = []
        for elem in self.Objects:
            cameraTransformed.append(
                elem.applyCameraTransform(cameraTransform)
            )
        deepest_point = 0
        for elem in cameraTransformed:
            deepest_point_Object = max(elem.getZ())
            if deepest_point_Object > deepest_point:
                deepest_point = deepest_point_Object
        res = []
        for elem in cameraTransformed:
            # check wether object is in front of camera
            if max(elem.getZ()) > 0:
                object = elem.project(deepest_point)

                # check wether projection is inside of FOV
                ObjectOutside = True
                for point in object:
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
                    res.append(object)
        # TODO: res contains transformed and projected objects (list of tuples of coordinates).
        # now scale and move that stuff, to fit onto self.Screen
        pass
