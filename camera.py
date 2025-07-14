from base import *

class Camera:
    def __init__(self, position: point = point([0, 0, 0]), orientation: vector = vector([0, 0, 0]), target: point = None):
        # the position as pair of three cartesian coordinates
        self.position_: point = position
        # the orientation in tait-bryan angles (yaw, pitch, roll)
        self.orientation_: vector = orientation
        self.target_: point = target
    '''changes the rotation of the camera to watch the given target from its current position'''
    def target(self, target: point): # roll is not affected by that
        self.target_ = target
        direction = vbp(self.orientation_, target, True)
        yaw = atan(direction[0]/direction[2]) # = atan(x/z)
        # TODO: Test wether it works with z = 0. if not, if condition testing wether z = 0
        # and raising an error then (camera inside of target)
        direction_in_x_z_plane = vector(        # the vector pointing into the direction of direction 
            [direction[0], 0, direction[2]]
        ).normalize()
        pitch = direction.angleToVector(direction_in_x_z_plane)
        if direction[2] < 0:    # add orientation, cause angleToVector always returns positive values
            pitch = -pitch
        self.orientation_[0] = yaw
        self.orientation_[1] = pitch
    def getCameraTransformMatrix(self):
        # my yaw pitch and roll is an intrinsic rotation by y-axis, x-axis, z-axis
        translation = matrix((4, 4))
        translation[0, 0] = 1
        translation[1, 1] = 1
        translation[2, 2] = 1
        translation[3, 3] = 1
        for index, val in zip(range(4), -self.position_):
            translation[index, 3] = val
        result = (( translation * \
                    createRotationMatrixZ(self.orientation_[2])) * \
                    createRotationMatrixX(self.orientation_[1])) * \
                    createRotationMatrixY(self.orientation_[0])
        return result