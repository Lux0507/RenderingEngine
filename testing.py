from Scene import *


def CameraTransformTest():
    cam = Camera(point([0, 0, 0]))
    cam.orientation_ = (0, 0, 0)
    obj = MObject((
        Point3D(0, 2, 0),
        Point3D(0, 0, 2)),
        [(0, 1)]
    )
    matrix = cam.getCameraTransformMatrix()
    print(matrix)
    transformed = obj.applyCameraTransform(matrix)
    for p in transformed.Points:
        print(p)


def SceneTest():
    myScene = Scene(camera_position=(0, -4, 0))
    myScene.Camera.orientation_ = (PI, PI/2, 0)
    # TODO: pitch does not work, yaw and roll work fine
    myScene.add(
        MObject(
            (Point3D(0, 2, 2),
            Point3D(2, 2, 0),
            Point3D(-2, 2, 0)),
            [(0, 1), (0, 2), (1, 2)]
        )
    )
    myScene.render()

# CameraTransformTest()