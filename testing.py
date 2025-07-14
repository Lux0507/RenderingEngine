from Scene import *

myScene = Scene(camera_position=(0, 0, 4))
myScene.Camera.orientation_ = (PI, 0, 0)
# TODO: pitch does not work, yaw and roll work fine
myScene.add(
    MObject(
        (Point3D(0, 0, 0),
         Point3D(1, 1, 0),
         Point3D(-1, 1, 0)),
        [(0, 1), (0, 2), (1, 2)]
    )
)
myScene.render()


# py.init()

# screen = py.PixelArray(py.display.set_mode((1600, 900)))
# screen[0:10, 0:10] = (255, 255, 255)
# running = True

# while running:
#     for event in py.event.get():
#         if event.type == py.QUIT:
#             running = False
#     # rendering
    

#     py.display.flip()
# py.quit()