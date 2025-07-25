from Scene import *

# TODO list:
# - implement and test drawing
# - make sure, that Scene.__InFOV doesn't append empty MObjects to result
# - revise Scene.__InFOV and __GetLineFunc: remove that specialized stuff for diff_x = 0. just return None then
# - initializer fro MObject for Triangles paralelograms...
# - methods add point and add connection for MObject
# - add styling field members to MObject
# - matrix.fromList ensure that no list of lists of non-numerical types are given
# - implement camera reorient methods and test camera.target
# - implement crossproduct
# - implement __rmul__ for matrix
# - implement matrix multiplication for non-square matrices
# - 
# - 
# - 

# region Camera transform Test

def CameraTransformTest():
    cam = Camera(point.create([0, 0, 0]))
    cam.orientation_ = (0, 0, 0)
    a, b, c = 2, 0, 0
    d, e, f = 0, 2, 0
    g, h, i = 0, 0, 2
    obj = MObject((
        Point3D(a, b, c),
        Point3D(d, e, f),
        Point3D(g, h, i)),
        [(0, 1), (1, 2), (0, 2)]
    )
    # test translation
    error: list[tuple[base]] = []
    angleY = 0.0
    angleX = -PI/2
    angleZ = 0.0
    while angleY < 2*PI:
        while angleX < PI:
            while angleZ < 2*PI:
                for z in range(8):
                    for x in range(8):
                        for y in range(8):
                            cam.position_ = base.create([-x, -y, -z])
                            cam.orientation_ = base.create([angleY, angleX, angleZ])
                            exspected_res_points: list[Point3D] = []
                            if angleY == 0:
                                if angleX == -PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, z + b, -(y + c)),
                                            Point3D(x + d, z + e, -(y + f)),
                                            Point3D(x + g, z + h, -(y + i))
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), x + b, -(y + c)),
                                            Point3D(-(z + d), x + e, -(y + f)),
                                            Point3D(-(z + g), x + h, -(y + i))
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), -(z + b), -(y + c)),
                                            Point3D(-(x + d), -(z + e), -(y + f)),
                                            Point3D(-(x + g), -(z + h), -(y + i))
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, -(x + b), -(y + c)),
                                            Point3D(z + d, -(x + e), -(y + f)),
                                            Point3D(z + g, -(x + h), -(y + i))
                                        ]
                                elif angleX == 0:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, y + b, z + c),
                                            Point3D(x + d, y + e, z + f),
                                            Point3D(x + g, y + h, z + i)
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(y + a), x + b, z + c),
                                            Point3D(-(y + d), x + e, z + f),
                                            Point3D(-(y + g), x + h, z + i)
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), -(y + b), z + c),
                                            Point3D(-(x + d), -(y + e), z + f),
                                            Point3D(-(x + g), -(y + h), z + i)
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(y + a, -(x + b), z + c),
                                            Point3D(y + d, -(x + e), z + f),
                                            Point3D(y + g, -(x + h), z + i)
                                        ]
                                elif angleX == PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, -(z + b), y + c),
                                            Point3D(x + d, -(z + e), y + f),
                                            Point3D(x + g, -(z + h), y + i)
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, x + b, y + c),
                                            Point3D(z + d, x + e, y + f),
                                            Point3D(z + g, x + h, y + i)
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), z + b, y + c),
                                            Point3D(-(x + d), z + e, y + f),
                                            Point3D(-(x + g), z + h, y + i)
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), -(x + b), y + c),
                                            Point3D(-(z + d), -(x + e), y + f),
                                            Point3D(-(z + g), -(x + h), y + i)
                                        ]
                            elif angleY == PI/2:
                                if angleX == -PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, -(x + b), -(y + c)),
                                            Point3D(z + d, -(x + e), -(y + f)),
                                            Point3D(z + g, -(x + h), -(y + i))
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, z + b, -(y + c)),
                                            Point3D(x + d, z + e, -(y + f)),
                                            Point3D(x + g, z + h, -(y + i))
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), x + b, -(y + c)),
                                            Point3D(-(z + d), x + e, -(y + f)),
                                            Point3D(-(z + g), x + h, -(y + i))
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), -(z + b), -(y + c)),
                                            Point3D(-(x + d), -(z + e), -(y + f)),
                                            Point3D(-(x + g), -(z + h), -(y + i))
                                        ]
                                elif angleX == 0:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, y + b, -(x + c)),
                                            Point3D(z + d, y + e, -(x + f)),
                                            Point3D(z + g, y + h, -(x + i))
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(y + a), z + b, -(x + c)),
                                            Point3D(-(y + d), z + e, -(x + f)),
                                            Point3D(-(y + g), z + h, -(x + i))
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), -(y + b), -(x + c)),
                                            Point3D(-(z + d), -(y + e), -(x + f)),
                                            Point3D(-(z + g), -(y + h), -(x + i))
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(y + a, -(z + b), -(x + c)),
                                            Point3D(y + d, -(z + e), -(x + f)),
                                            Point3D(y + g, -(z + h), -(x + i))
                                        ]
                                elif angleX == PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, x + b, y + c),
                                            Point3D(z + d, x + e, y + f),
                                            Point3D(z + g, x + h, y + i)
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), z + b, y + c),
                                            Point3D(-(x + d), z + e, y + f),
                                            Point3D(-(x + g), z + h, y + i)
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), -(x + b), y + c),
                                            Point3D(-(z + d), -(x + e), y + f),
                                            Point3D(-(z + g), -(x + h), y + i)
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, -(z + b), y + c),
                                            Point3D(x + d, -(z + e), y + f),
                                            Point3D(x + g, -(z + h), y + i)
                                        ]
                            elif angleY == PI:
                                if angleX == -PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), -(z + b), -(y + c)),
                                            Point3D(-(x + d), -(z + e), -(y + f)),
                                            Point3D(-(x + g), -(z + h), -(y + i))
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, -(x + b), -(y + c)),
                                            Point3D(z + d, -(x + e), -(y + f)),
                                            Point3D(z + g, -(x + h), -(y + i))
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, z + b, -(y + c)),
                                            Point3D(x + d, z + e, -(y + f)),
                                            Point3D(x + g, z + h, -(y + i))
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), x + b, -(y + c)),
                                            Point3D(-(z + d), x + e, -(y + f)),
                                            Point3D(-(z + g), x + h, -(y + i))
                                        ]
                                elif angleX == 0:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), y + b, -(z + c)),
                                            Point3D(-(x + d), y + e, -(z + f)),
                                            Point3D(-(x + g), y + h, -(z + i))
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(y + a), -(x + b), -(z + c)),
                                            Point3D(-(y + d), -(x + e), -(z + f)),
                                            Point3D(-(y + g), -(x + h), -(z + i))
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, -(y + b), -(z + c)),
                                            Point3D(x + d, -(y + e), -(z + f)),
                                            Point3D(x + g, -(y + h), -(z + i))
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(y + a, x + b, -(z + c)),
                                            Point3D(y + d, x + e, -(z + f)),
                                            Point3D(y + g, x + h, -(z + i))
                                        ]
                                elif angleX == PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), z + b, y + c),
                                            Point3D(-(x + d), z + e, y + f),
                                            Point3D(-(x + g), z + h, y + i)
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), -(x + b), y + c),
                                            Point3D(-(z + d), -(x + e), y + f),
                                            Point3D(-(z + g), -(x + h), y + i)
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, -(z + b), y + c),
                                            Point3D(x + d, -(z + e), y + f),
                                            Point3D(x + g, -(z + h), y + i)
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, x + b, y + c),
                                            Point3D(z + d, x + e, y + f),
                                            Point3D(z + g, x + h, y + i)
                                        ]
                            elif angleY == (3*PI)/2:
                                if angleX == -PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), x + b, -(y + c)),
                                            Point3D(-(z + d), x + e, -(y + f)),
                                            Point3D(-(z + g), x + h, -(y + i))
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), -(z + b), -(y + c)),
                                            Point3D(-(x + d), -(z + e), -(y + f)),
                                            Point3D(-(x + g), -(z + h), -(y + i))
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, -(x + b), -(y + c)),
                                            Point3D(z + d, -(x + e), -(y + f)),
                                            Point3D(z + g, -(x + h), -(y + i))
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, z + b, -(y + c)),
                                            Point3D(x + d, z + e, -(y + f)),
                                            Point3D(x + g, z + h, -(y + i))
                                        ]
                                elif angleX == 0:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), y + b, x + c),
                                            Point3D(-(z + d), y + e, x + f),
                                            Point3D(-(z + g), y + h, x + i)
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(y + a), -(z + b), x + c),
                                            Point3D(-(y + d), -(z + e), x + f),
                                            Point3D(-(y + g), -(z + h), x + i)
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, -(y + b), x + c),
                                            Point3D(z + d, -(y + e), x + f),
                                            Point3D(z + g, -(y + h), x + i)
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(y + a, z + b, x + c),
                                            Point3D(y + d, z + e, x + f),
                                            Point3D(y + g, z + h, x + i)
                                        ]
                                elif angleX == PI/2:
                                    if angleZ == 0:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(z + a), -(x + b), y + c),
                                            Point3D(-(z + d), -(x + e), y + f),
                                            Point3D(-(z + g), -(x + h), y + i)
                                        ]
                                    elif angleZ == PI/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(x + a, -(z + b), y + c),
                                            Point3D(x + d, -(z + e), y + f),
                                            Point3D(x + g, -(z + h), y + i)
                                        ]
                                    elif angleZ == PI:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(z + a, x + b, y + c),
                                            Point3D(z + d, x + e, y + f),
                                            Point3D(z + g, x + h, y + i)
                                        ]
                                    elif angleZ == (3*PI)/2:
                                        exspected_res_points = [ # valid, not tested
                                            Point3D(-(x + a), z + b, y + c),
                                            Point3D(-(x + d), z + e, y + f),
                                            Point3D(-(x + g), z + h, y + i)
                                        ]
                            exspectedRes = MObject(exspected_res_points, [(0, 1), (0, 2), (1, 2)])
                            # store each camposition that didn't work
                            if CameraTransformTestOnMObject(obj, cam, exspectedRes):
                                error.append((
                                    base.create([-x, -y, -z]),
                                    base.create([angleY, angleX, angleZ])
                                ))
                angleZ += PI/2
            angleX += PI/2
            angleZ = 0.0
        angleY += PI/2
        angleX = -PI/2
    
    # print out mistakes
    print(f"Es sind {len(error)} Fehler aufgetreten:")
    for elem in error:
        print(f"Fehler bei: Kamera-Position: {elem[0]} und Kamera-Orientierung: {elem[1]}")

    if len(error) == 0: # add other result lists as condition
        print("Es sind keine Fehler aufgetreten")

def CameraTransformTestOnMObject(obj: MObject, camera: Camera, exspected_res: MObject): 
    """test wether camera transform works correctly by applying the camera transform to the given MObject

    Args:
        obj (MObject): The object to apply the camera transform to
        camera (Camera): the camera object
        exspected_res (MObject): the exspected result

    Returns:
        _type_: False if everything works fine
    """
    transformed = obj.applyCameraTransform(camera.getCameraTransformMatrix())
    return not (transformed == exspected_res)

# endregion

# region pinhole project test

def pinholeProjectTest():
    counter = 0
    error: list[tuple] = []
    for z in range(1, 8):
        fov = 1.0
        while fov < 4.5:
            for height in range(9, 17):
                counter += 1
                screen_ratio = (16, height)
                fov_heigth = fov * (height/16)
                scene = Scene(fov=fov, screen_ratio=screen_ratio)
                objs = [
                    MObject([
                        Point3D(1 ,  1, z),
                        Point3D(-1,  1, z),
                        Point3D(1 , -1, z),
                        Point3D(-1, -1, z)
                    ], [(0, 1), (0, 2), (1, 3), (2, 3)])
                ]
                result = Scene.__pinholeProject(scene, objs)
                comparison: bool = False
                if (1/z) > (fov * 0.5) and (1/z) > (fov_heigth * 0.5):
                    exspected_result = [
                        MObject([], [])
                    ]
                    comparison = result == exspected_result
                    if not comparison:
                        error.append((result, exspected_result, fov, z, height))
                elif (1/z) <= (fov * 0.5) and (1/z) > (fov_heigth * 0.5):
                    exspected_result = [
                        MObject([
                            Point3D(1/z ,  1/z, 1.0),
                            Point3D(-1/z, 1/z, 1.0),
                            Point3D(1/z , -1/z, 1.0),
                            Point3D(-1/z, -1/z, 1.0)
                        ], [(0, 2), (1, 3)])
                    ]
                    comparison = result == exspected_result
                    if not comparison:
                        error.append((result, exspected_result, fov, z, height))
                elif 1/z <= (fov * 0.5) and (1/z) <= (fov_heigth * 0.5):
                    exspected_result = [
                        MObject([
                            Point3D(1/z ,  1/z, 1.0),
                            Point3D(-1/z, 1/z, 1.0),
                            Point3D(1/z , -1/z, 1.0),
                            Point3D(-1/z, -1/z, 1.0)
                        ], [(0, 1), (0, 2), (1, 3), (2, 3)])
                    ]
                    comparison = result == exspected_result
                    if not comparison:
                        error.append((result, exspected_result, fov, z, height))
                else:
                    # something went totally wrong
                    error.append((result, exspected_result, fov, z))
                    raise RuntimeError("vertical FOV in butr horizontal not. Hows that possible with an aspect ratio of 16:9")
            fov += 0.5
    print(f"Es wurden Test unter {counter} verschiedenen Inputs durchgeführt.")
    if len(error) > 0:
        # print out mistakes
        print(f"Dabei sind {len(error)} Fehler aufgetreten:")
        for elem in error:
            print(f"Fehler bei z={elem[3]}, fov={elem[2]} und aspect_ratio={(16, elem[4])}: erwartetes Ergebnis: {elem[1]}; erhaltenes Ergebnis: {elem[0]}")
    else:
        print("Dabei sind keine Fehler aufgetreten")

# endregion

# region Scale To Screen Test

def ScaleTest():
    counter = 0
    error = []
    for screen_width in range(600, 1900, 200):
        for height in range(9, 17):
            aspectRatio = (16, height)
            fov = 1.0
            while fov < 4.5:
                counter += 1
                scene = Scene(fov, screen_width=screen_width, screen_ratio=aspectRatio)
                objs = [MObject([
                    Point3D(0.0,   0.0,   0.0),
                    Point3D(fov/4, 0.0,   0.0),
                    Point3D(0.0,   fov/8, 0.0)],
                    [(0, 1), (0, 2), (1, 2)]
                )]
                result = Scene.scaleToScreen(scene, objs)
                fov_v = fov * (height/16)
                exspected_res = [MObject([
                    Point3D(round((fov/2) * (screen_width/fov)),          round((-1 * (fov_v * -0.5)) * (screen_width/fov)),           0.0),
                    Point3D(round((fov/4 + fov/2) * (screen_width/fov)),  round((-1 * (fov_v * -0.5)) * (screen_width/fov)),           0.0),
                    Point3D(round((fov/2) * (screen_width/fov)),          round((-1 * (fov/8 + (fov_v * -0.5))) * (screen_width/fov)), 0.0)],
                    [(0, 1), (0, 2), (1, 2)]
                )]
                comparison = result == exspected_res
                if not comparison:
                    error.append((screen_width, height, fov, exspected_res, result))
                fov += 0.5
    print(f"Es wurden {counter} Tests mit verschiedenen Inputs durchgeführt")
    if len(error) > 0:
        print(f"Dabei sind {len(error)} Fehler aufgetreten:")
        for elem in error:
            print(f"Fehler bei ScreenWidth={elem[0]}, AspectRatio={(16, elem[1])} und fov={elem[2]}")
            print(f"    Erwartetes    Ergebnis: {elem[3]}")
            print(f"    Tatsächliches Ergebnis: {elem[4]}")
    else:
        print("Dabei sind keine Fehler aufgetreten")

# endregion

# region other

def SceneTest():
    myScene = Scene(camera_position=(0, -4, 0))
    myScene.Camera.orientation_ = (PI, PI/2, 0)
    myScene.add(
        MObject(
            (Point3D(0, 2, 2),
            Point3D(2, 2, 0),
            Point3D(-2, 2, 0)),
            [(0, 1), (0, 2), (1, 2)]
        )
    )
    myScene.render()

def SortTest():
    l1 = [                      # abc, acb, bac, bca, cab, cba
        base.create([0, 2, 0]),    # b:  1     1    1    1    1    1
        base.create([0, 0, 2]),    # c:  0     0    0    0    0    0
        base.create([2, 0, 0])     # a:  2     2    2    2    2    2
    ]
    l1.sort()
    print(l1)

# endregion

# ScaleTest()
# pinholeProjectTest()
# SortTest()
# CameraTransformTest()