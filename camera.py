from base import *

class Camera:
    def __init__(self, position: point = point.create([0, 0, 0]), orientation: vector = vector.create([0, 0, 0]), target: point = None):
        # the position as pair of three cartesian coordinates
        self.position_: base = position
        # the orientation in tait-bryan angles (yaw, pitch, roll)
        self.orientation_: base = orientation
        self.target_: base = target
    def absOrient(self, yaw: float, pitch: float, roll: float):
        self.orientation_ = base([yaw, pitch, roll])
    def relOrient(self, quaternion):
        pass
    def yaw(yaw):
        pass
    def pitch(pitch):
        pass
    def roll(roll):
        pass
    def target(self, target: point): # roll is not affected by that
        """changes the orientation of the camera to wathc the given target from its current position

        Args:
            target (point): the target to face
        """
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
        translation = matrix.unitMatrix((4, 4))
        for index, val in zip(range(4), -self.position_):
            translation[index, 3] = val
        # yaw pitch and roll is an extrinsic rotation around y-x'-z''
        # converted to an intrinsic rotation, the camera is plaed in space by rotations around z-x-y axes in that order
        # to convert from world space to camera space apply the positionig of the camera in the world space in reverse order, with inverted angles.
        # So first move space, so that the camera is positioned at the origin
        # then apply rotations around y-z-x axes in that order. (remember: matrix multiplication is read from left to right)
        result =    createRotationMatrixZ(-self.orientation_[2]) * \
                    (createRotationMatrixX(-self.orientation_[1]) * \
                    (createRotationMatrixY(-self.orientation_[0]) * \
                    translation))
        return result