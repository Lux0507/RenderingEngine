from camera import *
from MObject import *
import pygame as py

class Scene:
    def __init__(self, screen_width = 1600, screen_ratio = (16, 9)):
        self.Screen_Size = (screen_width, screen_width * (screen_ratio[1] * screen_ratio[0]))
        self.Screen = py.Surface(self.Screen_Size)
        self.Camera = Camera((5, 5, 5))
        self.Objects: list[MObject] = []
    def add(self, object: MObject):
        self.Objects.append(object)
    def render(self):
        # camera transformation
        cameraTransform = self.Camera.getCameraTransformMatrix()
        cameraTransformed: list[MObject] = []
        for elem in self.Objects:
            cameraTransformed.append(
                elem.applyCameraTransform(cameraTransform)
            )
        for elem in cameraTransformed:
            for 