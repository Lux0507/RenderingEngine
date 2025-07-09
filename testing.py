from Scene import *


myScene = Scene(camera_position=(0, 0, -2))

triangle = Triangle(
    (
        Vector3D(0, 0, 0),
        Vector3D(2, 0, 0),
        Vector3D(0, 2, 0)
    )
)
myScene.add(triangle)
myScene.render()