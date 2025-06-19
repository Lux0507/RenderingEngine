from main import * 

class Camera:
    def __init__(self, position: point, orientation: vector, target: point = None):
        # the position as pair of three cartesian coordinates
        self.position_ = position
        # the orientation in tait-bryan angles (yaw, pitch, roll)
        self.orientation_ = orientation
        self.target_ = target
    '''changes the rotation of the camera to watch the given target from its current position'''
    def target(self, target: point):
        self.target_ = target
        direction = self.position_.vectorTo()

