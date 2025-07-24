from Scene import *
# TODO: Test for pinhole project

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

#region pinhole project test

def pinholeProjectTest():
    error: list[tuple] = []
    for z in range(1, 8):
        fov = 1.0
        while fov < 4.5:
            # for fov = 2.0 the connection is right on the edge of the screen. What ist GetLine going to compute then
            scene = Scene(fov=fov)
            objs = [
                MObject([
                    Point3D(1 ,  1, z),
                    Point3D(-1,  1, z),
                    Point3D(1 , -1, z),
                    Point3D(-1, -1, z)
                ], [(0, 1), (0, 2), (1, 3), (2, 3)])
            ]
            result = Scene.pinholeProject(scene, objs)[0]
            comparison: bool = False
            if fov < 2.0:
                exspected_result = MObject([
                        Point3D(1/z ,  1/z, 1.0),
                        Point3D(-1/z, 1/z, 1.0),
                        Point3D(1/z , -1/z, 1.0),
                        Point3D(-1/z, -1/z, 1.0)
                    ], [])
                comparison = result == exspected_result
                if not comparison:
                    error.append((result, exspected_result, fov, z))
            elif fov < 4.0:
                # horizontal conns are outside
                exspected_result = MObject([
                        Point3D(1/z ,  1/z, 1.0),
                        Point3D(-1/z,  1/z, 1.0),
                        Point3D(1/z , -1/z, 1.0),
                        Point3D(-1/z, -1/z, 1.0)
                    ], [(0, 2), (1, 3)])
                comparison = result == exspected_result
                if not comparison:
                    error.append((result, exspected_result, fov, z))
            else:
                exspected_result = MObject([
                        Point3D(1/z ,  1/z, 1.0),
                        Point3D(-1/z,  1/z, 1.0),
                        Point3D(1/z , -1/z, 1.0),
                        Point3D(-1/z, -1/z, 1.0)
                    ], [(0, 1), (0, 2), (1, 3), (2, 3)])
                comparison = result == exspected_result
                if not comparison:
                    error.append((result, exspected_result, fov, z))
            fov += 0.5
    if len(error) > 0:
        # print out mistakes
        print(f"Es sind {len(error)} Fehler aufgetreten:")
        for elem in error:
            print(f"Fehler bei z={error[3]} und fov={error[2]}: erwartetes Ergebnis: {elem[1]}; erhaltenes Ergebnis: {elem[0]}")

# endregion

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

pinholeProjectTest()
# SortTest()
# CameraTransformTest()